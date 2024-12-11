from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Annotated, Optional, List, Dict, Union, Callable, Any

from langchain_core.messages import (
    AIMessage,
    ChatMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict

# Define the state for the agent
class State(TypedDict):
    messages: Annotated[list, add_messages]
    pending_tools: List[ToolCall]
    results: Dict[str, ToolResult]
    errors: Dict[str, str]
    tool_code: Optional[str]

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4o")

# Initialize the tools
@tool
def search_flights(destination: str) -> str:
    """Searches for flights to the given destination."""
    return f"Flights to {destination}"

@tool
def search_hotels(location: str) -> str:
    """Searches for hotels in the given location."""
    return f"Hotels in {location}"

@tool
def search_car_rentals(pickup_location: str) -> str:
    """Searches for car rentals in the given location."""
    return f"Car rentals in {pickup_location}"

# Build the graph
graph_builder = StateGraph(State)


# This is a stub class - you need to implement it
class ParallelToolExecutor:
    def __init__(self, tools: List[Callable]):
        """
        Initializes a new instance of the ParallelToolExecutor class.

        Args:
            tools (List[Callable]): The list of tools to execute in parallel.
        """
        self.tools = tools

    def execute(self, tool_inputs: List[Dict[str, Any]]) -> Dict[str, Union[Any, str]]:
        """
        Executes the tools in parallel with the given inputs.

        Args:
            tool_inputs (List[Dict[str, Any]]): A list of dictionaries where each dictionary contains the input arguments for a tool.

        Returns:
            Dict[str, Union[Any, str]]: A dictionary containing the results or error messages of each tool call.
        """
        # Implement parallel execution, result aggregation, error handling, and progress reporting here
        pass

# Initialize the ParallelToolExecutor
executor = ParallelToolExecutor(tools=[search_flights, search_hotels, search_car_rentals])

def llm_node(state: State) -> dict[str, list[AIMessage]]:
    """
    This node is executed whenever the graph is invoked.
    It takes in the current graph state, calls an LLM, and returns a new message to be added to the state.
    """
    messages = state["messages"]
    tool_code = state["tool_code"]
    
    # For this example, we will use the last message in the state as the message to prompt the LLM.
    last_message = messages[-1]
    if isinstance(last_message, HumanMessage):
        # The LLM should be invoked with a ChatMessage, so we convert it.
        if isinstance(last_message, ChatMessage):
            chat_message = last_message
        else:
            chat_message = ChatMessage(content=last_message.content)
        
        # This is the call to the LLM
        try:
            new_message = llm.invoke([
                SystemMessage(content=(
                    "You are a customer support agent for an airline. "
                    "Here are the tools you can use:\n"
                    "- search_flights: Searches for flights.\n"
                    "- update_ticket_to_new_flight: Updates a ticket to a new flight.\n"
                    "- cancel_ticket: Cancels a ticket.\n"
                    "- search_car_rentals: Searches for car rentals.\n"
                    "- book_car_rental: Books a car rental.\n"
                    "- update_car_rental: Updates a car rental.\n"
                    "- cancel_car_rental: Cancels a car rental.\n"
                    "- search_hotels: Searches for hotels.\n"
                    "- book_hotel: Books a hotel.\n"
                    "- update_hotel: Updates a hotel.\n"
                    "- cancel_hotel: Cancels a hotel.\n"
                    "- search_trip_recommendations: Searches for trip recommendations.\n"
                    "- book_excursion: Books an excursion.\n"
                    "- update_excursion: Updates an excursion.\n"
                    "- cancel_excursion: Cancels an excursion.\n"
                )),
                ChatMessage(content=f"You can optionally call a tool to assist the user. Here is the tool code:\n\n{tool_code}"),
                chat_message
            ])
        except Exception:
            # Handle errors that may arise when calling the LLM API
            new_message = AIMessage(content="I'm sorry, I had a problem communicating with the LLM API. Please try again.")
    
    # If the last message was not a "HumanMessage", respond with a canned response.
    else:
        new_message = AIMessage(content="I'm sorry, I don't understand.")

    # Append the LLM's response to the state
    return {"messages": [new_message]}

def search_tool(state: State) -> State:
    """
    Searches for flights, car rentals, hotels, and trip recommendations.
    """
    messages = state["messages"]
    last_message = messages[-1]
    try:
        # For now, we will use a simple heuristic to classify the message
        if "flight" in last_message.content:
            tool_code = "search_flights()"
        elif "car rental" in last_message.content:
            tool_code = "search_car_rentals()"
        elif "hotel" in last_message.content:
            tool_code = "search_hotels()"
        elif "trip recommendation" in last_message.content:
            tool_code = "search_trip_recommendations()"
        else:
            tool_code = None
    except Exception as e:
        # If the last message is not a HumanMessage, we will raise an error.
        raise ValueError(f"The last message is not a HumanMessage, so it cannot be classified. Last message: {last_message}, Error: {e}")
    
    if tool_code:
        return {
            "messages": [ToolMessage(content=f"Here are the results:\n\n{tool_code}")],
            "tool_code": tool_code
        }
    else:
        return {
            "messages": [AIMessage(content="I'm sorry, I can't help you with that.")],
            "tool_code": None
        }

graph_builder.add_node("llm", llm_node)
graph_builder.add_node("search_tool", search_tool)

# Add edges
graph_builder.add_edge(START, "llm")
graph_builder.add_conditional_edges("llm", tools_condition)
# Any time a tool is called, we return to the llm to decide the next step
graph_builder.add_edge("search_tool", "llm")

graph = graph_builder.compile()