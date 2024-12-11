from typing import Annotated, Optional, Dict, List

from langchain_core.messages import (
    AIMessage,
    ChatMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict

# Define the state for the agent
class State(TypedDict):
    messages: Annotated[list, add_messages]
    available_tools: List[ToolNode]
    tool_usage: Dict[str, int]
    rate_limits: Dict[str, int]  # Rate limit per tool (calls per conversation)

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4")

# Build the graph
graph_builder = StateGraph(State)

def llm_node(state: State) -> State:
    """
    This node is executed whenever the graph is invoked.
    It takes the current graph state, calls an LLM, and returns a new state.
    This includes deciding which tool to use (if any) and updating the tool_code.
    """
    messages = state["messages"]
    tool_code = state.get("tool_code")  # Tool code from previous step (if any)

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
            new_message = llm.invoke(
                [
                    SystemMessage(
                        content=(
                            "You are a helpful AI assistant. "
                            "You can optionally call a tool to assist the user. "
                            "Here's how to call tools:\n\n"
                            "search: Search for information on the web.\n"
                            "calculator: Use a calculator to solve math problems.\n"
                            "weather: Get the current weather in a given location.\n\n"
                            "To call a tool, simply write 'tool_code: tool_name(query)' "
                            "where 'tool_name' is the name of the tool you want to call "
                            "and 'query' is the input to the tool. "
                            "For example, to search for information about the Eiffel Tower, "
                            "you would write 'tool_code: search(Eiffel Tower)'. "
                            "You can only call one tool at a time. "
                            f"Here is the previous tool code:\n\n{tool_code}"
                        )
                    ),
                    chat_message,
                ]
            )
        except Exception:
            # Handle errors that may arise when calling the LLM API
            new_message = AIMessage(
                content="I'm sorry, I had a problem communicating with the LLM API. Please try again."
            )

        # Extract tool_code from the LLM's response
        # (This is a simple example, more robust parsing might be needed)
        tool_code = None
        if new_message.content.startswith("tool_code:"):
            tool_code = new_message.content.split("tool_code:")[1].strip()

        return {"messages": [new_message], "tool_code": tool_code}

    # If the last message was not a HumanMessage, respond with a canned response.
    else:
        return {
            "messages": [AIMessage(content="I'm sorry, I don't understand.")],
            "tool_code": None,
        }


def tool_selection_node(state: State) -> State:
    """
    This node selects the appropriate tool based on the tool_code in the state.
    It also enforces rate limits and updates tool usage.
    """
    tool_code = state["tool_code"]
    available_tools = state["available_tools"]
    tool_usage = state["tool_usage"]
    rate_limits = state["rate_limits"]

    # Identify the correct tool based on tool_code
    selected_tool = None
    for tool in available_tools:
        if tool_code.startswith(tool.name):
            selected_tool = tool
            break

    if selected_tool:
        tool_name = selected_tool.name
        # Check if the tool's rate limit has been reached
        if tool_usage.get(tool_name, 0) >= rate_limits.get(tool_name, 1):
            return {
                "messages": [
                    AIMessage(
                        content=f"I'm sorry, I've reached the usage limit for {tool_name}."
                    )
                ],
                "tool_code": None,
            }

        # Update tool usage
        tool_usage[tool_name] = tool_usage.get(tool_name, 0) + 1

        try:
            # Call the tool
            tool_output = selected_tool.invoke(state)
            # Return the tool's output
            return {
                "messages": tool_output["messages"],
                "tool_code": None,  # Reset tool_code after tool use
                "tool_usage": tool_usage,
            }
        except Exception as e:
            return {
                "messages": [
                    AIMessage(
                        content=f"I'm sorry, I encountered an error while using {tool_name}: {e}"
                    )
                ],
                "tool_code": None,
            }
    else:
        return {
            "messages": [AIMessage(content="I'm sorry, I don't know that tool.")],
            "tool_code": None,
        }


# Define your tool functions here (search, math, weather)
def search_tool(state: State) -> State:
    """Searches for information on the web."""
    # This is a placeholder, you would use a search API here
    query = state["tool_code"].split("search(")[1][:-1]
    return {
        "messages": [ToolMessage(content=f"Search results for {query}: ...")],
    }


def calculator_tool(state: State) -> State:
    """Uses a calculator to solve math problems."""
    # This is a placeholder, you would use a calculator API or library here
    query = state["tool_code"].split("calculator(")[1][:-1]
    return {
        "messages": [ToolMessage(content=f"Calculator result: {query} = ...")],
    }


def weather_tool(state: State) -> State:
    """Gets the current weather in a given location."""
    # This is a placeholder, you would use a weather API here
    query = state["tool_code"].split("weather(")[1][:-1]
    return {
        "messages": [ToolMessage(content=f"Weather in {query}: ...")],
    }


# Create ToolNodes for the tools
search_tool_node = ToolNode(
    name="search",
    func=search_tool,
)
calculator_tool_node = ToolNode(
    name="calculator",
    func=calculator_tool,
)
weather_tool_node = ToolNode(name="weather", func=weather_tool)

# Add nodes to the graph
graph_builder.add_node("llm", llm_node)
graph_builder.add_node("tool_selection", tool_selection_node)
graph_builder.add_node("search", search_tool_node)
graph_builder.add_node("calculator", calculator_tool_node)
graph_builder.add_node("weather", weather_tool_node)

# Add edges
graph_builder.add_edge(START, "llm")
graph_builder.add_conditional_edges("llm", tools_condition)
graph_builder.add_edge("tool_selection", "llm")  # Return to LLM after tool use

graph = graph_builder.compile()