# import http.client
# import urllib.parse

# conn = http.client.HTTPSConnection("restaurants222.p.rapidapi.com")

# params = {
#     "location_id": "297704",
#     "language": "en_US",
#     "currency": "USD",
#     "offset": "0"
# }

# payload = urllib.parse.urlencode(params)

# headers = {
#     'x-rapidapi-key': "565f6b5957msh30764c74f1c6f78p1826a4jsncbb57377cdcf",
#     'x-rapidapi-host': "restaurants222.p.rapidapi.com",
#     'Content-Type': "application/x-www-form-urlencoded"
# }

# conn.request("POST", "/search", payload, headers)

# res = conn.getresponse()
# data = res.read()

# print(data.decode("utf-8"))


# import requests
# import json

# def rapidapi_restaurant_search():
#     url = "https://restaurants222.p.rapidapi.com/search"
#     payload = {
#         "location_id": "297628",  # Bengaluru
#         "language": "en_US",
#         "currency": "USD",
#         "offset": "0",
#         "limit": "1"  # Requests one restaurant (though API may return more)
#     }
#     headers = {
#         'x-rapidapi-key': "565f6b5957msh30764c74f1c6f78p1826a4jsncbb57377cdcf",
#         'x-rapidapi-host': "restaurants222.p.rapidapi.com",
#         'Content-Type': "application/x-www-form-urlencoded"
#     }

#     try:
#         # Make the API request
#         response = requests.post(url, data=payload, headers=headers)
#         response.raise_for_status()  # Check for HTTP errors
#         api_response = response.text
#         print("Raw API response:", api_response)  # Print raw response for debugging

#         # Parse JSON
#         result_dict = json.loads(api_response)

#         # Debugging: Inspect the structure
#         print("Top-level keys:", result_dict.keys())
#         if "results" in result_dict:
#             print("Keys in 'results':", result_dict["results"].keys())

#         # Correctly access the restaurant data
#         if ("results" in result_dict and 
#             isinstance(result_dict["results"], dict) and 
#             "data" in result_dict["results"] and 
#             isinstance(result_dict["results"]["data"], list) and 
#             len(result_dict["results"]["data"]) > 0):
#             first_restaurant = result_dict["results"]["data"][0]
#             with open("restaurant.json", "w") as f:
#                 json.dump(first_restaurant, f, indent=2)
#             print("Saved one restaurant to restaurant.json")
#         else:
#             with open("restaurant.json", "w") as f:
#                 json.dump({"message": "No restaurants found"}, f, indent=2)
#             print("No restaurants found. Saved message to restaurant.json")

#     except requests.RequestException as e:
#         print(f"API request failed: {e}")
#     except json.JSONDecodeError as e:
#         print(f"JSON decode error: {e}")

# if __name__ == "__main__":
#     rapidapi_restaurant_search()






import os
import json
import http.client
import urllib.parse
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from langchain_core.tools import tool
import dotenv
from datetime import timedelta

dotenv.load_dotenv()

# ─── A. Define state ──────────────────────────────────────────────────────────
class Restaurant(TypedDict):
    name: str
    address: str
    cuisines: list[str]
    rating: float
    price: str
    phone: dict
    opening_hours: list[dict]
    distance: float

class RestDiscoveryState(TypedDict):
    messages: list
    query: str
    restaurants: list[Restaurant]

# ─── B. Setup Gemini LLM ─────────────────────────────────────────────────────
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GEMINI_API_KEY"))

# ─── C. Create RapidAPI wrapper ───────────────────────────────────────────────
@tool
def rapidapi_restaurant_search(location_id: str = "297628", query: str = "", limit:str="1") -> str:
    """
    Searches for restaurants using the RapidAPI restaurants222 endpoint and returns results as a JSON string.
    
    Args:
        location_id (str): The location ID for the search (e.g., "297628" for Bengaluru).
        query (str): The search query to find restaurants (e.g., "sushi").
        limit (str): Number of results to return (default: "5").
    
    Returns:
        str: A JSON string containing the search results.
    """
    conn = http.client.HTTPSConnection("restaurants222.p.rapidapi.com")

    params = {
        "location_id": location_id,
        "language": "en_US",
        "currency": "USD",
        "offset": "0",
        "limit": limit
    }
    if query.strip():
        params["q"] = query
    
    payload = urllib.parse.urlencode(params)

    headers = {
        'x-rapidapi-key': "565f6b5957msh30764c74f1c6f78p1826a4jsncbb57377cdcf",
        'x-rapidapi-host': "restaurants222.p.rapidapi.com",
        'Content-Type': "application/x-www-form-urlencoded"
    }
    try:
        conn.request("POST", "/search", payload, headers)
        res = conn.getresponse()
        data = res.read().decode('utf-8')
        print("[DEBUG] RapidAPI raw response:", data)
        return data
    except Exception as e:
        err = json.dumps({"error": str(e)})
        print("[DEBUG] RapidAPI error:", err)
        return err
    finally:
        conn.close()

# Bind the tool to the model
model_with_tools = model.bind_tools([rapidapi_restaurant_search])

# ─── D. Helper Functions ─────────────────────────────────────────────────────
def parse_query(query: str) -> dict:
    query = query.lower()
    params = {"location_id": "297628", "specific_query": ""}  # Default location (e.g., Bengaluru)
    
    location_map = {
        "bengaluru": "297628",
        "mumbai": "298027"  # Correct ID for Mumbai
    }
    
    for city, loc_id in location_map.items():
        if city in query:
            params["location_id"] = loc_id
            break
    
    print(f"[DEBUG] parse_query -> {params}")
    return params
def convert_minutes_to_time(minutes: int) -> str:
    """
    Convert minutes since midnight to a human-readable time (e.g., 420 -> "07:00 AM").
    
    Args:
        minutes (int): Minutes since midnight.
    
    Returns:
        str: Formatted time string.
    """
    time_delta = timedelta(minutes=minutes)
    hours = (time_delta.seconds // 3600) % 24
    mins = (time_delta.seconds // 60) % 60
    period = "AM" if hours < 12 else "PM"
    if hours == 0:
        hours = 12
    elif hours > 12:
        hours -= 12
    return f"{hours:02d}:{mins:02d} {period}"

# ─── E. LangGraph subgraph ────────────────────────────────────────────────────
def call_agent(state: RestDiscoveryState):
    parsed_params = parse_query(state["query"])
    # System message to guide the model
    system_msg = SystemMessage(content="You are a restaurant recommendation assistant. When asked to look up restaurants, use the rapidapi_restaurant_search tool with the provided location_id.")
    # Human message with query and location_id
    human_msg = HumanMessage(content=f"Look up {state['query']} with location_id {parsed_params['location_id']}")
    print(f"[DEBUG] call_agent human_msg: {human_msg.content}")
    # Invoke model with system and human messages
    ai_msg = model_with_tools.invoke([system_msg, human_msg])
    print(f"[DEBUG] AIMessage: {ai_msg.content}")
    print(f"[DEBUG] tool_calls: {[tc for tc in ai_msg.tool_calls]}")

    tool_msgs = []
    for tool_call in ai_msg.tool_calls:
        # Use dictionary key access instead of dot notation
        print(f"[DEBUG] Executing tool {tool_call['name']} with args {tool_call['args']}")
        output = rapidapi_restaurant_search.invoke({
            "location_id": parsed_params["location_id"],
            "query": parsed_params["specific_query"],
            "limit": "1"
        })
        print(f"[DEBUG] tool output: {output}")
        tool_msgs.append(ToolMessage(
            content=output,
            tool_call_id=tool_call['id']
        ))

    return {"messages": [system_msg, human_msg, ai_msg] + tool_msgs}

tool_node = ToolNode([rapidapi_restaurant_search])

def extract_restaurants(state: RestDiscoveryState):
    msg = next((m for m in state["messages"] if isinstance(m, ToolMessage)), None)
    if msg:
        try:
            result_dict = json.loads(msg.content)
            rest_list = []
            
            # Access restaurants from results.data
            restaurants = result_dict.get("results", {}).get("data", [])[:3]  # Limit to 5
            
            for res in restaurants:
                # Extract cuisines
                cuisines = [c.get("name", "") for c in res.get("cuisine", []) if c.get("name")]
                
                # Convert hours
                hours_data = res.get("hours", {}).get("week_ranges", [])
                opening_hours = []
                day_names = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
                for day_idx, day_schedule in enumerate(hours_data):
                    for slot in day_schedule:
                        opening_hours.append({
                            "day": day_names[day_idx],
                            "open": convert_minutes_to_time(slot.get("open_time", 0)),
                            "close": convert_minutes_to_time(slot.get("close_time", 0))
                        })
                
                restaurant = {
                    "name": res.get("name", "Unknown"),
                    "address": res.get("address", "No address"),
                    "cuisines": cuisines,
                    "rating": float(res.get("rating", 0.0)),
                    "price": res.get("price", "Unknown"),
                    "phone": {
                        "phone": res.get("phone", "No phone"),
                        "website": res.get("website", "No website")
                    },
                    "opening_hours": opening_hours,
                    "distance": float(res.get("distance", 0.0)) if res.get("distance") else 0.0
                }
                
                # Filter for sushi places if specified
                if "sushi" in state["query"].lower():
                    if any(c.lower() in ["sushi", "japanese"] for c in cuisines):
                        rest_list.append(restaurant)
                else:
                    rest_list.append(restaurant)
            
            return {"restaurants": rest_list}
        except Exception as e:
            print("JSON parsing error:", e)
            return {"restaurants": []}
    return {"restaurants": []}

builder = StateGraph(RestDiscoveryState)
builder.add_node("agent", call_agent)
builder.add_node("tools", tool_node)
builder.add_node("extract", extract_restaurants)

builder.add_edge(START, "agent")
builder.add_edge("agent", "tools")
builder.add_edge("tools", "extract")
builder.add_edge("extract", END)

rest_graph = builder.compile()

# ─── F. Invoke for Testing ──────────────────────────────────────────────────
state: RestDiscoveryState = {
    "messages": [],
    "query": "restaurants in mumbai",
    "restaurants": []
}
result = rest_graph.invoke(state)
print(json.dumps(result["restaurants"], indent=2))