import os
import json
from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import requests as pyrequests

load_dotenv()

# Use Groq API key for speech-to-text
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GROQ_WHISPER_URL = 'https://api.groq.com/openai/v1/audio/transcriptions'

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load catalog once at startup
with open(os.path.join(os.path.dirname(__file__), 'catalog.json')) as f:
    CATALOG = json.load(f)

class CartRequest(BaseModel):
    transcription: str

def match_product(item_name):
    item_name = item_name.lower()
    for product in CATALOG:
        if item_name in [a.lower() for a in product['aliases']]:
            return product
        if item_name in product['title'].lower():
            return product
    return None

def convert_units(qty, from_unit, to_unit):
    # Simple conversion for g <-> kg, ml <-> l, pcs stays same
    if from_unit == to_unit:
        return qty
    if from_unit == 'g' and to_unit == 'kg':
        return qty / 1000
    if from_unit == 'kg' and to_unit == 'g':
        return qty * 1000
    if from_unit == 'ml' and to_unit == 'l':
        return qty / 1000
    if from_unit == 'l' and to_unit == 'ml':
        return qty * 1000
    return qty  # fallback, no conversion

def extract_structured_items_gpt(transcription):
    # Create a simplified version of catalog for the prompt
    catalog_summary = []
    for product in CATALOG:
        catalog_summary.append({
            'jpin': product['jpin'],
            'title': product['title'],
            'aliases': product['aliases'],
            'mrp': product['mrp'],
            'sp': product['sp']
        })
    
    # Print the transcription and catalog for debugging
    print("Transcription:", transcription)
    print("Catalog summary:", json.dumps(catalog_summary, indent=2))
    
    prompt = f"""
You are an intelligent billing assistant. Your task is to:
1. Extract products, quantities, and units from the given text
2. Match them with the provided catalog data
3. Return a JSON array of matched products with their details

Available products in catalog:
{json.dumps(catalog_summary, indent=2)}

Rules:
- Only return products that exist in the catalog
- Use the exact title and aliases from the catalog for matching
- Convert quantities to standard units (g, kg, pcs)
- Include all relevant product details in the response
- If a product is mentioned but not found in catalog, skip it
- If no products are found, return an empty array []
- Be flexible with product names - check both title and aliases
- For quantities like "one piece", convert to 1 pcs
- For quantities like "half kg", convert to 0.5 kg

Example input: "one piece muskmelon, half kg mango"
Example output: [
  {{
    "name": "muskmelon",
    "quantity": 1,
    "unit": "pcs",
    "matched_product": {{
      "jpin": "123456",
      "title": "Muskmelon (Honey Dew)",
      "mrp": 100,
      "sp": 90
    }}
  }},
  {{
    "name": "mango",
    "quantity": 0.5,
    "unit": "kg",
    "matched_product": {{
      "jpin": "789012",
      "title": "Mango, 1Kg",
      "mrp": 100,
      "sp": 90
    }}
  }}
]

Input text: {transcription}
Output:
"""
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        "model": "gpt-4.1",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500,
        "temperature": 0.1
    }
    
    # Print the prompt for debugging
    # print("Sending prompt to GPT-4:", prompt)
    
    response = pyrequests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    if response.status_code == 200:
        try:
            content = response.json()['choices'][0]['message']['content']
            # Print the raw response for debugging
            print("GPT-4 raw response:", content)
            
            # Try to extract JSON array from the response
            start = content.find('[')
            end = content.rfind(']')
            if start != -1 and end != -1:
                json_str = content[start:end+1]
                result = json.loads(json_str)
                # Print the parsed result for debugging
                print("Parsed result:", json.dumps(result, indent=2))
                return result
        except Exception as e:
            print("GPT extraction error:", e)
    else:
        print("GPT API error:", response.text)
    return []

@app.post('/cart')
async def cart(cart_req: CartRequest):
    transcription = cart_req.transcription
    if not transcription:
        raise HTTPException(status_code=400, detail='No transcription provided')
    structured_items = extract_structured_items_gpt(transcription)
    if not structured_items:
        raise HTTPException(status_code=400, detail='No structured items extracted')
    cart = []
    for item in structured_items:
        if 'matched_product' in item:
            product = item['matched_product']
            req_qty = item['quantity']
            req_unit = item['unit']
            
            # Calculate price based on quantity and unit
            price = req_qty * product['sp']  # Simplified price calculation
            
            cart.append({
                'title': product['title'],
                'requested_quantity': req_qty,
                'unit': req_unit,
                'calculated_price': round(price, 2),
                'sp': product['sp'],
                'mrp': product['mrp']
            })
    
    return { 'cart': cart }

@app.post('/transcribe')
async def transcribe(audio: UploadFile = File(...)):
    if not audio:
        raise HTTPException(status_code=400, detail='No audio file provided')
    files = {
        'file': (audio.filename, await audio.read(), audio.content_type),
    }
    data = {
        'model': 'whisper-large-v3',
        'response_format': 'json',
        'language': 'en',  # You can make this dynamic if needed
    }
    headers = {
        'Authorization': f'Bearer {GROQ_API_KEY}'
    }
    response = pyrequests.post(GROQ_WHISPER_URL, files=files, data=data, headers=headers)
    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        raise HTTPException(status_code=500, detail={ 'error': 'Transcription failed', 'details': response.text })

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5001, reload=True) 
