# import os
# import google.generativeai as genai
# from serpapi import GoogleSearch
# from langgraph.prebuilt import ToolNode
# from langgraph.graph import StateGraph, START, END
# from typing_extensions import TypedDict
# from langchain_core.tools import tool
# from langchain_core.messages import ToolMessage, AIMessage
# import serpapi
# import dotenv

# dotenv.load_dotenv()
# # ─── A. Define state ──────────────────────────────────────────────────────────
# class Restaurant(TypedDict):
#     name: str
#     address: str
#     rating: float

# class RestDiscoveryState(TypedDict):
#     messages: list
#     query: str
#     restaurants: list[Restaurant]

# # ─── B. Setup Gemini LLM ─────────────────────────────────────────────────────
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# # ─── C. Create SerpAPI wrapper ────────────────────────────────────────────────
# @tool
# def ddg_serpapi(q: str) -> str:
#     """
#     Searches DuckDuckGo using SerpAPI and returns the results as a dictionary.
    
#     Args:
#         q (str): The search query to be executed on DuckDuckGo.
    
#     Returns:
#         dict: A dictionary containing the search results from DuckDuckGo.
#     """
#     params = {
#         "engine": "duckduckgo",
#         "q": q,
#         "kl": "us-en",
#         "api_key": os.getenv("SERPAPI_API_KEY"),
#         "num": "5"
#     }
#     return serpapi(params).get_dict()

# # ─── D. LangGraph subgraph ────────────────────────────────────────────────────
# def call_agent(state: RestDiscoveryState):
#     prompt = (
#         f"You are a restaurant discovery assistant. "
#         f"User query: \"{state['query']}\". "
#         f"Call the DDG tool to find 5 local restaurants, returning JSON "
#         f"with name, address, rating."
#     )
#     model=genai.GenerativeModel('gemini-2.0-flash')
#     resp = model.generate_content(prompt)
    
#     return {"messages": [AIMessage(content=resp.text)]}

# tool_node = ToolNode([ddg_serpapi])

# def extract_restaurants(state: RestDiscoveryState):
#     msg = next((m for m in state["messages"] if isinstance(m, ToolMessage)), None)
#     data = msg.content if msg else "[]"
#     import json
#     try: rest_list = json.loads(data)
#     except: rest_list = []
#     return {"restaurants": rest_list}

# builder = StateGraph(RestDiscoveryState)
# builder.add_node("agent", call_agent)
# builder.add_node("tools", tool_node)
# builder.add_node("extract", extract_restaurants)

# builder.add_edge(START, "agent")
# builder.add_edge("agent", "tools")
# builder.add_edge("tools", "extract")
# builder.add_edge("extract", END)

# rest_graph = builder.compile()

# # ─── E. Invoke for Testing ──────────────────────────────────────────────────
# state: RestDiscoveryState = {
#     "messages": [],
#     "query": "best sushi places in Bengaluru near MG Road",
#     "restaurants": []
# }
# result = rest_graph.invoke(state)
# print(result["restaurants"])


import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from langchain_core.tools import tool
from serpapi import GoogleSearch
import dotenv

dotenv.load_dotenv()

# ─── A. Define state ──────────────────────────────────────────────────────────
class Restaurant(TypedDict):
    name: str
    address: str
    rating: float

class RestDiscoveryState(TypedDict):
    messages: list
    query: str
    restaurants: list[Restaurant]

# ─── B. Setup Gemini LLM ─────────────────────────────────────────────────────
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GEMINI_API_KEY"))
# Note: Replace "GEMINI_API_KEY" with "GOOGLE_API_KEY" if that’s your env variable name

# ─── C. Create SerpAPI wrapper ────────────────────────────────────────────────
@tool
def ddg_serpapi(q: str) -> str:
    """
    Searches DuckDuckGo using SerpAPI and returns the results as a JSON string.
    
    Args:
        q (str): The search query to be executed on DuckDuckGo.
    
    Returns:
        str: A JSON string containing the search results.
    """
    params = {
        "engine": "duckduckgo",
        "q": q,
        "kl": "us-en",
        "api_key": os.getenv("SERPAPI_API_KEY"),
        "num": "5"
    }
    search = GoogleSearch(params)
    return json.dumps(search.get_dict())  # Return JSON string

# Bind the tool to the model
model_with_tools = model.bind_tools([ddg_serpapi])

# ─── D. LangGraph subgraph ────────────────────────────────────────────────────
def call_agent(state: RestDiscoveryState):
    prompt = (
        f"You are a restaurant discovery assistant with access to the DDG tool. "
        f"User query: \"{state['query']}\". "
        f"Call the DDG tool to find 5 local restaurants and return their name, address, and rating in JSON format."
    )
    message = HumanMessage(content=prompt)
    response = model_with_tools.invoke([message])
    #print("Agent response:", response)  # Debug output
    return {"messages": [response]}

tool_node = ToolNode([ddg_serpapi])

def extract_restaurants(state: RestDiscoveryState):
    msg = next((m for m in state["messages"] if isinstance(m, ToolMessage)), None)
    #print("Tool message:", msg)  # Debug output
    if msg:
        try:
            result_dict = json.loads(msg.content)
            # Adjust this based on SerpAPI’s DuckDuckGo response structure
            rest_list = [
                {
                    "name": res.get("title", "Unknown"),
                    "address": res.get("snippet", "No address"),
                    "rating": float(res.get("rating", 0.0)) if "rating" in res else 0.0
                }
                for res in result_dict.get("organic_results", [])
            ]
        except Exception as e:
            print("JSON parsing error:", e)
            rest_list = []
    else:
        rest_list = []
    return {"restaurants": rest_list}

builder = StateGraph(RestDiscoveryState)
builder.add_node("agent", call_agent)
builder.add_node("tools", tool_node)
builder.add_node("extract", extract_restaurants)

builder.add_edge(START, "agent")
builder.add_edge("agent", "tools")
builder.add_edge("tools", "extract")
builder.add_edge("extract", END)

rest_graph = builder.compile()

# ─── E. Invoke for Testing ──────────────────────────────────────────────────
state: RestDiscoveryState = {
    "messages": [],
    "query": "best sushi places in Bengaluru near MG Road",
    "restaurants": []
}
result = rest_graph.invoke(state)
print(result["restaurants"])