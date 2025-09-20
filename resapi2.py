# import os
# import json
# import http.client
# import urllib.parse
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
# from langgraph.graph import StateGraph, START, END
# from typing_extensions import TypedDict
# from langchain_core.tools import tool
# import dotenv
# from datetime import timedelta

# dotenv.load_dotenv()

# # Define state
# class Restaurant(TypedDict):
#     name: str
#     address: str
#     cuisines: list[str]
#     rating: float
#     price: str
#     phone: str
#     opening_hours: list[dict]
#     distance: float
#     menu: list[dict]  # Added to store menu items

# class RestDiscoveryState(TypedDict):
#     messages: list
#     query: str
#     restaurants: list[Restaurant]

# # Setup Gemini LLM
# model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GEMINI_API_KEY"))

# # Create Uber Eats Scraper API wrapper
# @tool
# def uber_eats_restaurant_search(address: str, query: str = "", max_rows: int = 5, locale: str = "en-US", page: int = 1) -> str:
#     """
#     Searches for restaurants using the Uber Eats Scraper API and returns results as a JSON string.
    
#     Args:
#         address (str): The address or city to search in.
#         query (str): The search query (e.g., "pizza").
#         max_rows (int): Number of results to return.
#         locale (str): Locale for the search.
#         page (int): Page number for pagination.
    
#     Returns:
#         str: A JSON string containing the search results.
#     """
#     conn = http.client.HTTPSConnection("uber-eats-scraper-api.p.rapidapi.com")
    
#     payload = json.dumps({
#         "scraper": {
#             "maxRows": max_rows,
#             "query": query,
#             "address": address,
#             "locale": locale,
#             "page": page
#         }
#     })
    
#     headers = {
#         'x-rapidapi-key': " c83c16ff40mshf1d83cb2edd8813p1c9dfcjsnd8e79b6a4f8a",
#         'x-rapidapi-host': "uber-eats-scraper-api.p.rapidapi.com",
#         'Content-Type': "application/json"
#     }
    
#     try:
#         conn.request("POST", "/api/job", payload, headers)
#         res = conn.getresponse()
#         print("HTTP status:", res.status)
#         body = res.read().decode("utf-8")
#         print("RAW BODY:", body)
#         response_data = json.loads(body)
#         returnvalue = response_data.get("returnvalue", {})
#         return json.dumps(returnvalue)
#     except Exception as e:
#         err = json.dumps({"error": str(e)})
#         return err
#     finally:
#         conn.close()

# # Bind the tool to the model
# model_with_tools = model.bind_tools([uber_eats_restaurant_search])

# # Helper Functions
# def parse_query(query: str) -> dict:
#     query = query.lower()
#     params = {"address": "", "query": ""}
    
#     if " in " in query:
#         parts = query.split(" in ")
#         if len(parts) == 2:
#             params["address"] = parts[1].strip()
#             if parts[0] != "restaurants":
#                 params["query"] = parts[0].strip()
#     else:
#         params["query"] = query.strip()
    
#     return params

# def convert_minutes_to_time(minutes: int) -> str:
#     time_delta = timedelta(minutes=minutes)
#     hours = (time_delta.seconds // 3600) % 24
#     mins = (time_delta.seconds // 60) % 60
#     period = "AM" if hours < 12 else "PM"
#     if hours == 0:
#         hours = 12
#     elif hours > 12:
#         hours -= 12
#     return f"{hours:02d}:{mins:02d} {period}"

# #LangGraph subgraph
# def call_agent(state: RestDiscoveryState):
#     messages = state["messages"]
#     if not messages:
#         return {"messages": [AIMessage(content="Please provide a query.")]}

#     latest_msg = messages[-1]
#     if isinstance(latest_msg, HumanMessage):
#         if not state["restaurants"] or "restaurants in" in latest_msg.content.lower():
#             # Treat as search query
#             parsed_params = parse_query(latest_msg.content)
#             system_msg = SystemMessage(content="You are a restaurant recommendation assistant. Use the uber_eats_restaurant_search tool with the provided address and query.")
#             human_msg = HumanMessage(content=f"Look up restaurants with query '{parsed_params['query']}' in address '{parsed_params['address']}'")
#             ai_msg = model_with_tools.invoke([system_msg, human_msg])
#             tool_msgs = []
#             for tool_call in ai_msg.tool_calls:
#                 output = uber_eats_restaurant_search.invoke(tool_call['args'])
#                 tool_msgs.append(ToolMessage(content=output, tool_call_id=tool_call['id']))
#             # Extract restaurants from tool message
#             try:
#                 result_dict = json.loads(tool_msgs[0].content)
#                 rest_list = []
#                 restaurants = result_dict.get("data", [])[:5]
#                 for res in restaurants:
#                     hours = res.get("hours", [])
#                     opening_hours = []
#                     for day in hours:
#                         day_range = day.get("dayRange", "")
#                         for section in day.get("sectionHours", []):
#                             # Convert startTime and endTime to integers
#                             start_time = int(section.get("startTime", 0))
#                             end_time = int(section.get("endTime", 0))
#                             opening_hours.append({
#                                 "day": day_range,
#                                 "open": convert_minutes_to_time(start_time),
#                                 "close": convert_minutes_to_time(end_time)
#                             })
#                     menu = res.get("menu", [])
#                     menu_items = []
#                     for section in menu:
#                         for item in section.get("catalogItems", [])[:3]:
#                             menu_items.append({
#                                 "title": item.get("title", ""),
#                                 "price": item.get("price", 0)
#                             })
#                     restaurant = {
#                         "name": res.get("title", "Unknown"),
#                         "address": res.get("location", {}).get("address", "No address"),
#                         "cuisines": res.get("cuisineList", []),
#                         "rating": float(res.get("rating", {}).get("ratingValue", 0.0)),
#                         "price": "Unknown",
#                         "phone": res.get("phoneNumber", "No phone"),
#                         "opening_hours": opening_hours,
#                         "distance": 0.0,
#                         "menu": menu_items
#                     }
#                     rest_list.append(restaurant)
#                 # Generate restaurant list message
#                 rest_names = [rest["name"] for rest in rest_list]
#                 message = "Here are some restaurants:\n" + "\n".join([f"{i+1}. {name}" for i, name in enumerate(rest_names)])
#                 ai_response = AIMessage(content=message)
#                 return {"messages": messages + [system_msg, human_msg, ai_msg] + tool_msgs + [ai_response], "restaurants": rest_list}
#             except Exception as e:
#                 print("Error processing restaurants:", e)  # Log the error for debugging
#                 ai_response = AIMessage(content="Sorry, I couldn't find any restaurants.")
#                 return {"messages": messages + [ai_response]}
#         else:
#             # Treat as restaurant selection
#             selected_rest = latest_msg.content.strip()
#             for rest in state["restaurants"]:
#                 if selected_rest.lower() in rest["name"].lower():
#                     menu_items = rest["menu"]
#                     menu_str = f"Menu for {rest['name']}:\n"
#                     for item in menu_items:
#                         menu_str += f"- {item['title']}: ${item['price'] / 100:.2f}\n"
#                     ai_msg = AIMessage(content=menu_str)
#                     return {"messages": messages + [ai_msg]}
#             ai_msg = AIMessage(content="Sorry, I couldn't find that restaurant.")
#             return {"messages": messages + [ai_msg]}
#     return state


# # LangGraph subgraph - MODIFIED SECTION
# # ... (keep all code above the call_agent function the same) ...



# builder = StateGraph(RestDiscoveryState)
# builder.add_node("agent", call_agent)
# builder.add_edge(START, "agent")
# builder.add_edge("agent", END)
# rest_graph = builder.compile()

# # # Invoke for Testing
# initial_state = {
#     "messages": [HumanMessage(content="pizza in 1600 Pennsylvania Avenue, Washington DC")],
#     "query": "pizza in 1600 Pennsylvania Avenue, Washington DC",
#     "restaurants": []
# }
# state_after_search = rest_graph.invoke(initial_state)
# print(state_after_search["messages"][-1].content)  # Displays the restaurant list

# if state_after_search["restaurants"]:
#     restaurant_name = state_after_search["restaurants"][0]["name"]
#     state_after_selection = {
#         "messages": state_after_search["messages"] + [HumanMessage(content=restaurant_name)],
#         "restaurants": state_after_search["restaurants"]
#     }
#     final_state = rest_graph.invoke(state_after_selection)
#     print(final_state["messages"][-1].content)  # Displays the menu
# else:
#     print("No restaurants found.")








# import os
# import json
# import http.client
# import urllib.parse
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
# from langgraph.graph import StateGraph, START, END
# from typing_extensions import TypedDict
# from langchain_core.tools import tool
# import dotenv
# from datetime import timedelta

# dotenv.load_dotenv()

# # Define state
# class Restaurant(TypedDict):
#     name: str
#     address: str
#     cuisines: list[str]
#     rating: float
#     price: str
#     phone: str
#     opening_hours: list[dict]
#     distance: float
#     menu: list[dict]  # Added to store menu items

# class RestDiscoveryState(TypedDict):
#     messages: list
#     query: str
#     restaurants: list[Restaurant]

# # Setup Gemini LLM
# model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GEMINI_API_KEY"))

# # Create Uber Eats Scraper API wrapper
# @tool
# def uber_eats_restaurant_search(address: str, query: str = "", max_rows: int = 5, locale: str = "en-US", page: int = 1) -> str:
#     """
#     Searches for restaurants using the Uber Eats Scraper API and returns results as a JSON string.
    
#     Args:
#         address (str): The address or city to search in.
#         query (str): The search query (e.g., "pizza").
#         max_rows (int): Number of results to return.
#         locale (str): Locale for the search.
#         page (int): Page number for pagination.
    
#     Returns:
#         str: A JSON string containing the search results.
#     """
#     conn = http.client.HTTPSConnection("uber-eats-scraper-api.p.rapidapi.com")
    
#     payload = json.dumps({
#         "scraper": {
#             "maxRows": max_rows,
#             "query": query,
#             "address": address,
#             "locale": locale,
#             "page": page
#         }
#     })
    
#     headers = {
#         'x-rapidapi-key': "c83c16ff40mshf1d83cb2edd8813p1c9dfcjsnd8e79b6a4f8a",
#         'x-rapidapi-host': "uber-eats-scraper-api.p.rapidapi.com",
#         'Content-Type': "application/json"
#     }
    
#     try:
#         conn.request("POST", "/api/job", payload, headers)
#         res = conn.getresponse()
#         print("HTTP status:", res.status)
#         body = res.read().decode("utf-8")
#         print("RAW BODY:", body)
#         response_data = json.loads(body)
#         returnvalue = response_data.get("returnvalue", {})
#         return json.dumps(returnvalue)
#     except Exception as e:
#         err = json.dumps({"error": str(e)})
#         return err
#     finally:
#         conn.close()

# # Bind the tool to the model
# model_with_tools = model.bind_tools([uber_eats_restaurant_search])

# # Helper Functions
# def parse_query(query: str) -> dict:
#     query = query.lower()
#     params = {"address": "", "query": ""}
    
#     if " in " in query:
#         parts = query.split(" in ")
#         if len(parts) == 2:
#             params["address"] = parts[1].strip()
#             if parts[0] != "restaurants":
#                 params["query"] = parts[0].strip()
#     else:
#         params["query"] = query.strip()
    
#     return params

# def convert_minutes_to_time(minutes: int) -> str:
#     time_delta = timedelta(minutes=minutes)
#     hours = (time_delta.seconds // 3600) % 24
#     mins = (time_delta.seconds // 60) % 60
#     period = "AM" if hours < 12 else "PM"
#     if hours == 0:
#         hours = 12
#     elif hours > 12:
#         hours -= 12
#     return f"{hours:02d}:{mins:02d} {period}"

# # LangGraph subgraph - CORRECTED VERSION
# def call_agent(state: RestDiscoveryState):
#     messages = state["messages"]
#     if not messages:
#         return {"messages": [AIMessage(content="Please provide a query.")]}

#     latest_msg = messages[-1]
#     if isinstance(latest_msg, HumanMessage):
#         # If we have no restaurants or user is doing a new search
#         if not state["restaurants"] or "restaurants in" in latest_msg.content.lower():
#             # Treat as search query
#             parsed_params = parse_query(latest_msg.content)
#             system_msg = SystemMessage(content="You are a restaurant recommendation assistant. Use the uber_eats_restaurant_search tool with the provided address and query.")
#             human_msg = HumanMessage(content=f"Look up restaurants with query '{parsed_params['query']}' in address '{parsed_params['address']}'")
#             ai_msg = model_with_tools.invoke([system_msg, human_msg])
#             tool_msgs = []
#             for tool_call in ai_msg.tool_calls:
#                 output = uber_eats_restaurant_search.invoke(tool_call['args'])
#                 tool_msgs.append(ToolMessage(content=output, tool_call_id=tool_call['id']))
            
#             # Extract restaurants from tool message
#             try:
#                 result_dict = json.loads(tool_msgs[0].content)
#                 rest_list = []
                
#                 # CORRECTED: Access restaurant data from the proper location
#                 if "data" in result_dict:
#                     # Top-level data exists
#                     restaurants = result_dict["data"]
#                 elif "returnvalue" in result_dict and "data" in result_dict["returnvalue"]:
#                     # Nested in returnvalue
#                     restaurants = result_dict["returnvalue"]["data"]
#                 else:
#                     # Try to find any data array in the response
#                     restaurants = []
#                     for key in result_dict:
#                         if isinstance(result_dict[key], list):
#                             restaurants = result_dict[key]
#                             break
                
#                 # Process only if we have valid restaurant data
#                 if isinstance(restaurants, list) and restaurants:
#                     for res in restaurants[:5]:  # Limit to first 5 results
#                         if not isinstance(res, dict):
#                             continue
                            
#                         # Process hours
#                         opening_hours = []
#                         hours = res.get("hours", [])
#                         for day in hours:
#                             if not isinstance(day, dict):
#                                 continue
#                             day_range = day.get("dayRange", "")
#                             section_hours = day.get("sectionHours", [])
#                             for section in section_hours:
#                                 if not isinstance(section, dict):
#                                     continue
#                                 start_time = section.get("startTime", 0)
#                                 end_time = section.get("endTime", 0)
                                
#                                 # Ensure time values are integers
#                                 try:
#                                     start_time = int(start_time)
#                                 except:
#                                     start_time = 0
#                                 try:
#                                     end_time = int(end_time)
#                                 except:
#                                     end_time = 0
                                
#                                 opening_hours.append({
#                                     "day": day_range,
#                                     "open": convert_minutes_to_time(start_time),
#                                     "close": convert_minutes_to_time(end_time)
#                                 })
                        
#                         # Process menu
#                         menu_items = []
#                         menu = res.get("menu", [])
#                         for section in menu:
#                             if not isinstance(section, dict):
#                                 continue
#                             catalog_items = section.get("catalogItems", [])
#                             for item in catalog_items[:3]:  # First 3 items per section
#                                 if not isinstance(item, dict):
#                                     continue
#                                 menu_items.append({
#                                     "title": item.get("title", "Unknown Item"),
#                                     "price": item.get("price", 0)
#                                 })
                        
#                         # Build restaurant object
#                         location = res.get("location", {}) or {}
#                         rating = res.get("rating", {}) or {}
                        
#                         restaurant = {
#                             "name": res.get("title", "Unknown Restaurant"),
#                             "address": location.get("address", "Address not available"),
#                             "cuisines": res.get("cuisineList", []),
#                             "rating": float(rating.get("ratingValue", 0.0)),
#                             "price": "Unknown",
#                             "phone": res.get("phoneNumber", "Phone not available"),
#                             "opening_hours": opening_hours,
#                             "distance": 0.0,
#                             "menu": menu_items
#                         }
#                         rest_list.append(restaurant)
                    
#                     # Generate restaurant list with numbers
#                     if rest_list:
#                         rest_list_str = "\n".join(
#                             [f"{i+1}. {rest['name']} ({rest['rating']}★)" 
#                              for i, rest in enumerate(rest_list)]
#                         )
#                         message = f"🍽️ Found {len(rest_list)} restaurants:\n{rest_list_str}\n\n🔢 Please enter the NUMBER of the restaurant you want to see the menu for."
#                         ai_response = AIMessage(content=message)
#                         return {
#                             "messages": messages + [system_msg, human_msg, ai_msg] + tool_msgs + [ai_response],
#                             "restaurants": rest_list
#                         }
                
#                 # If we reach here, no restaurants were found
#                 print("No restaurants found in API response. Full response:")
#                 print(json.dumps(result_dict, indent=2)[:2000] + "...")
                
#                 ai_response = AIMessage(content="🔍 No restaurants found matching your criteria.")
#                 return {"messages": messages + [ai_response]}
            
#             except Exception as e:
#                 print(f"Error processing restaurants: {e}")
#                 if tool_msgs:
#                     print("Raw API response:", tool_msgs[0].content[:2000] + "...")
                
#                 ai_response = AIMessage(content="⚠️ Sorry, I encountered an error while processing restaurant data.")
#                 return {"messages": messages + [ai_response]}
        
#         # If we have restaurants and user is selecting by number
#         elif state["restaurants"]:
#             selected_input = latest_msg.content.strip()
            
#             # Check if input is a valid number
#             if selected_input.isdigit():
#                 index = int(selected_input) - 1
#                 if 0 <= index < len(state["restaurants"]):
#                     rest = state["restaurants"][index]
#                     menu_items = rest["menu"]
#                     menu_str = f"📋 Menu for {rest['name']}:\n"
#                     for item in menu_items:
#                         # Convert price from cents to dollars
#                         price_dollars = item['price'] / 100
#                         menu_str += f"- {item['title']}: ${price_dollars:.2f}\n"
                    
#                     ai_msg = AIMessage(content=menu_str)
#                     return {"messages": messages + [ai_msg]}
#                 else:
#                     ai_msg = AIMessage(content=f"❌ Invalid selection. Please enter a number between 1 and {len(state['restaurants'])}.")
#                     return {"messages": messages + [ai_msg]}
#             else:
#                 ai_msg = AIMessage(content="🔢 Please enter a NUMBER corresponding to the restaurant.")
#                 return {"messages": messages + [ai_msg]}
    
#     return state

# # Build the graph
# builder = StateGraph(RestDiscoveryState)
# builder.add_node("agent", call_agent)
# builder.add_edge(START, "agent")
# builder.add_edge("agent", END)
# rest_graph = builder.compile()

# # Test the system
# initial_state = {
#     "messages": [HumanMessage(content="pizza in 1600 Pennsylvania Avenue, Washington DC")],
#     "query": "pizza in 1600 Pennsylvania Avenue, Washington DC",
#     "restaurants": []
# }

# # Step 1: Search for restaurants
# state_after_search = rest_graph.invoke(initial_state)
# print("\n===== RESTAURANT LIST =====")
# print(state_after_search["messages"][-1].content)

# if state_after_search["restaurants"]:
#     # Step 2: Select a restaurant by number
#     state_after_selection = {
#         "messages": state_after_search["messages"] + [HumanMessage(content="1")],
#         "restaurants": state_after_search["restaurants"]
#     }
#     final_state = rest_graph.invoke(state_after_selection)
#     print("\n===== RESTAURANT MENU =====")
#     print(final_state["messages"][-1].content)
# else:
#     print("\nNo restaurants found.")




import os
import json
import http.client
import urllib.parse
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from langchain_core.tools import tool
import dotenv
from datetime import timedelta

dotenv.load_dotenv()

# Define state
class Restaurant(TypedDict):
    name: str
    address: str
    cuisines: list[str]
    rating: float
    price: str
    phone: str
    opening_hours: list[dict]
    distance: float
    menu: list[dict]  # Added to store menu items

class RestDiscoveryState(TypedDict):
    messages: list
    query: str
    restaurants: list[Restaurant]

# Setup Gemini LLM
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GEMINI_API_KEY"))

# Create Uber Eats Scraper API wrapper
@tool
def uber_eats_restaurant_search(address: str, query: str = "", max_rows: int = 5, locale: str = "en-US", page: int = 1) -> str:
    """
    Searches for restaurants using the Uber Eats Scraper API and returns results as a JSON string.
    
    Args:
        address (str): The address or city to search in.
        query (str): The search query (e.g., "pizza").
        max_rows (int): Number of results to return.
        locale (str): Locale for the search.
        page (int): Page number for pagination.
    
    Returns:
        str: A JSON string containing the search results.
    """
    conn = http.client.HTTPSConnection("uber-eats-scraper-api.p.rapidapi.com")
    
    payload = json.dumps({
        "scraper": {
            "maxRows": max_rows,
            "query": query,
            "address": address,
            "locale": locale,
            "page": page
        }
    })
    
    headers = {
        'x-rapidapi-key': "c83c16ff40mshf1d83cb2edd8813p1c9dfcjsnd8e79b6a4f8a",
        'x-rapidapi-host': "uber-eats-scraper-api.p.rapidapi.com",
        'Content-Type': "application/json"
    }
    
    try:
        conn.request("POST", "/api/job", payload, headers)
        res = conn.getresponse()
        print("HTTP status:", res.status)
        body = res.read().decode("utf-8")
        print("RAW BODY:", body)
        response_data = json.loads(body)
        returnvalue = response_data.get("returnvalue", {})
        return json.dumps(returnvalue)
    except Exception as e:
        err = json.dumps({"error": str(e)})
        return err
    finally:
        conn.close()

# Bind the tool to the model
model_with_tools = model.bind_tools([uber_eats_restaurant_search])

# Helper Functions
def parse_query(query: str) -> dict:
    query = query.lower()
    params = {"address": "", "query": ""}
    
    if " in " in query:
        parts = query.split(" in ")
        if len(parts) == 2:
            params["address"] = parts[1].strip()
            if parts[0] != "restaurants":
                params["query"] = parts[0].strip()
    else:
        params["query"] = query.strip()
    
    return params

def convert_minutes_to_time(minutes: int) -> str:
    time_delta = timedelta(minutes=minutes)
    hours = (time_delta.seconds // 3600) % 24
    mins = (time_delta.seconds // 60) % 60
    period = "AM" if hours < 12 else "PM"
    if hours == 0:
        hours = 12
    elif hours > 12:
        hours -= 12
    return f"{hours:02d}:{mins:02d} {period}"

# LangGraph subgraph - CORRECTED VERSION
def call_agent(state: RestDiscoveryState):
    messages = state["messages"]
    if not messages:
        return {"messages": [AIMessage(content="Please provide a query.")]}

    latest_msg = messages[-1]
    if isinstance(latest_msg, HumanMessage):
        # If we have no restaurants or user is doing a new search
        if not state["restaurants"] or "restaurants in" in latest_msg.content.lower():
            # Treat as search query
            parsed_params = parse_query(latest_msg.content)
            system_msg = SystemMessage(content="You are a restaurant recommendation assistant. Use the uber_eats_restaurant_search tool with the provided address and query.")
            human_msg = HumanMessage(content=f"Look up restaurants with query '{parsed_params['query']}' in address '{parsed_params['address']}'")
            ai_msg = model_with_tools.invoke([system_msg, human_msg])
            tool_msgs = []
            for tool_call in ai_msg.tool_calls:
                output = uber_eats_restaurant_search.invoke(tool_call['args'])
                tool_msgs.append(ToolMessage(content=output, tool_call_id=tool_call['id']))
            
            # Extract restaurants from tool message
            try:
                result_dict = json.loads(tool_msgs[0].content)
                rest_list = []
                
                # CORRECTED: Access restaurant data from the proper location
                if "data" in result_dict:
                    # Top-level data exists
                    restaurants = result_dict["data"]
                elif "returnvalue" in result_dict and "data" in result_dict["returnvalue"]:
                    # Nested in returnvalue
                    restaurants = result_dict["returnvalue"]["data"]
                else:
                    # Try to find any data array in the response
                    restaurants = []
                    for key in result_dict:
                        if isinstance(result_dict[key], list):
                            restaurants = result_dict[key]
                            break
                
                # Process only if we have valid restaurant data
                if isinstance(restaurants, list) and restaurants:
                    for res in restaurants[:5]:  # Limit to first 5 results
                        if not isinstance(res, dict):
                            continue
                            
                        # Process hours
                        opening_hours = []
                        hours = res.get("hours", [])
                        for day in hours:
                            if not isinstance(day, dict):
                                continue
                            day_range = day.get("dayRange", "")
                            section_hours = day.get("sectionHours", [])
                            for section in section_hours:
                                if not isinstance(section, dict):
                                    continue
                                start_time = section.get("startTime", 0)
                                end_time = section.get("endTime", 0)
                                
                                # Ensure time values are integers
                                try:
                                    start_time = int(start_time)
                                except:
                                    start_time = 0
                                try:
                                    end_time = int(end_time)
                                except:
                                    end_time = 0
                                
                                opening_hours.append({
                                    "day": day_range,
                                    "open": convert_minutes_to_time(start_time),
                                    "close": convert_minutes_to_time(end_time)
                                })
                        
                        # Process menu
                        menu_items = []
                        menu = res.get("menu", [])
                        for section in menu:
                            if not isinstance(section, dict):
                                continue
                            catalog_items = section.get("catalogItems", [])
                            for item in catalog_items[:3]:  # First 3 items per section
                                if not isinstance(item, dict):
                                    continue
                                menu_items.append({
                                    "title": item.get("title", "Unknown Item"),
                                    "price": item.get("price", 0)
                                })
                        
                        # Build restaurant object
                        location = res.get("location", {}) or {}
                        rating = res.get("rating", {}) or {}
                        
                        restaurant = {
                            "name": res.get("title", "Unknown Restaurant"),
                            "address": location.get("address", "Address not available"),
                            "cuisines": res.get("cuisineList", []),
                            "rating": float(rating.get("ratingValue", 0.0)),
                            "price": "Unknown",
                            "phone": res.get("phoneNumber", "Phone not available"),
                            "opening_hours": opening_hours,
                            "distance": 0.0,
                            "menu": menu_items
                        }
                        rest_list.append(restaurant)
                    
                    # Generate restaurant list with numbers
                    if rest_list:
                        rest_list_str = "\n".join(
                            [f"{i+1}. {rest['name']} ({rest['rating']}★)" 
                             for i, rest in enumerate(rest_list)]
                        )
                        message = f"🍽️ Found {len(rest_list)} restaurants:\n{rest_list_str}\n\n🔢 Please enter the NUMBER of the restaurant you want to see the menu for."
                        ai_response = AIMessage(content=message)
                        return {
                            "messages": messages + [system_msg, human_msg, ai_msg] + tool_msgs + [ai_response],
                            "restaurants": rest_list
                        }
                
                # If we reach here, no restaurants were found
                print("No restaurants found in API response. Full response:")
                print(json.dumps(result_dict, indent=2)[:2000] + "...")
                
                ai_response = AIMessage(content="🔍 No restaurants found matching your criteria.")
                return {"messages": messages + [ai_response]}
            
            except Exception as e:
                print(f"Error processing restaurants: {e}")
                if tool_msgs:
                    print("Raw API response:", tool_msgs[0].content[:2000] + "...")
                
                ai_response = AIMessage(content="⚠️ Sorry, I encountered an error while processing restaurant data.")
                return {"messages": messages + [ai_response]}
        
        # If we have restaurants and user is selecting by number
        elif state["restaurants"]:
            selected_input = latest_msg.content.strip()
            
            # Check if input is a valid number
            if selected_input.isdigit():
                index = int(selected_input) - 1
                if 0 <= index < len(state["restaurants"]):
                    rest = state["restaurants"][index]
                    menu_items = rest["menu"]
                    menu_str = f"📋 Menu for {rest['name']}:\n"
                    for item in menu_items:
                        # Convert price from cents to dollars
                        price_dollars = item['price'] / 100
                        menu_str += f"- {item['title']}: ${price_dollars:.2f}\n"
                    
                    ai_msg = AIMessage(content=menu_str)
                    return {"messages": messages + [ai_msg]}
                else:
                    ai_msg = AIMessage(content=f"❌ Invalid selection. Please enter a number between 1 and {len(state['restaurants'])}.")
                    return {"messages": messages + [ai_msg]}
            else:
                ai_msg = AIMessage(content="🔢 Please enter a NUMBER corresponding to the restaurant.")
                return {"messages": messages + [ai_msg]}
    
    return state

# Build the graph
builder = StateGraph(RestDiscoveryState)
builder.add_node("agent", call_agent)
builder.add_edge(START, "agent")
builder.add_edge("agent", END)
rest_graph = builder.compile()

# Interactive test function
def run_interactive_test():
    # Initial search
    initial_state = {
        "messages": [HumanMessage(content="pizza in 1600 Pennsylvania Avenue, Washington DC")],
        "query": "pizza in 1600 Pennsylvania Avenue, Washington DC",
        "restaurants": []
    }
    
    # Step 1: Search for restaurants
    state = rest_graph.invoke(initial_state)
    print("\n===== RESTAURANT LIST =====")
    print(state["messages"][-1].content)
    
    if not state["restaurants"]:
        print("\nNo restaurants found. Exiting.")
        return
    
    # Step 2: Get user selection
    while True:
        try:
            selection = input("\nEnter the NUMBER of the restaurant you want to see the menu for: ")
            if not selection.strip():
                continue
                
            # Create state with user's selection
            selection_state = {
                "messages": state["messages"] + [HumanMessage(content=selection)],
                "restaurants": state["restaurants"],
                "query": state["query"]
            }
            
            # Process selection
            result_state = rest_graph.invoke(selection_state)
            print("\n===== RESTAURANT MENU =====")
            print(result_state["messages"][-1].content)
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Please try again with a valid number.")

# Run the interactive test
run_interactive_test()