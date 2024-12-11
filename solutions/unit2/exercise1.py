from typing import Annotated, Optional, Any

from langchain_core.messages import (
    AIMessage,
    ChatMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain.tools import TavilySearch  # 3. Initialize the Tavily Search tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from pydantic import BaseModel, Field, validator
from typing_extensions import TypedDict

# 1. Define the expected Tool Input schema using Pydantic
class TavilySearchInput(BaseModel):
    query: str = Field(description="The search query to execute.")

    # 2. Add a validator to ensure the query is not empty
    @validator("query")
    def query_not_empty(cls, field):
        if not field:
            raise ValueError("Search query cannot be empty.")
        return field

# Define the state for the agent
class State(TypedDict):
    messages: Annotated[list, add_messages]
    tool_code: Optional[str]

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4o")

# 3. Initialize the Tavily Search Tool
search_tool = TavilySearch()

# Build the graph
graph_builder = StateGraph(State)

def llm_node(state: State) -> dict[str, list[AIMessage]]:
    """
    This node is executed whenever the graph is invoked.
    It takes in the current graph state, calls an LLM, and returns a new message
    to be added to the state.
    """
    messages = state["messages"]
    tool_code = state["tool_code"]

    # For this example, we will use the last message in the state as the
    # message to prompt the LLM.
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
                            "You are a customer support agent for an airline. "
                            "You have access to a search tool that can answer "
                            "questions about flights, car rentals, hotels, and "
                            "trip recommendations. Use the tool to get the "
                            "information you need to answer the user's query."
                        )
                    ),
                    ChatMessage(
                        content=(
                            "You can optionally call a tool to assist the user. "
                            f"Here is the tool code:\n\n{tool_code}"
                        )
                    ),
                    chat_message,
                ]
            )
        except Exception:
            # Handle errors that may arise when calling the LLM API
            new_message = AIMessage(
                content=(
                    "I'm sorry, I had a problem communicating with the LLM API. "
                    "Please try again."
                )
            )

    # If the last message was not a "HumanMessage", respond with a canned
    # response.
    else:
        new_message = AIMessage(content="I'm sorry, I don't understand.")

    # Append the LLM's response to the state
    return {"messages": [new_message]}

# 4. Create a ToolNode for the TavilySearch tool
#    - Use the TavilySearchInput schema for input validation
#    - Set retry_policy to handle failures
tool_node = ToolNode(
    search_tool,
    name="tavily_search",
    description="A search engine for finding information.",
    input_schema=TavilySearchInput,
    retry_policy={"max_retries": 3, "backoff_factor": 1.5},
)

def tool_result_processor(state: State) -> State:
    """
    5. Process the tool output:
       - Extract relevant information
       - Handle potential errors
       - Format the output for the user
    """
    messages = state["messages"]
    last_message = messages[-1]

    if isinstance(last_message, ToolMessage):
        try:
            # Example: Extract the relevant information from the tool output
            search_results = last_message.content

            # Format the output for the user
            formatted_output = f"Here are some search results I found:\n\n{search_results}"

            return {"messages": [AIMessage(content=formatted_output)], "tool_code": "search_tool()"}
        except Exception:
            return {
                "messages": [
                    AIMessage(
                        content=(
                            "I'm sorry, I had a problem processing the search "
                            "results. Please try again."
                        )
                    )
                ],
                "tool_code": None
            }
    else:
        return {
            "messages": [AIMessage(content="I'm sorry, I don't understand.")],
            "tool_code": None
        }

graph_builder.add_node("llm", llm_node)
# 6. Add the ToolNode to the graph
graph_builder.add_node("tavily_search", tool_node)
# 7. Add the tool result processing node to the graph
graph_builder.add_node("tool_result_processor", tool_result_processor)

# Add edges
graph_builder.add_edge(START, "llm")
graph_builder.add_conditional_edges("llm", tools_condition)
# 8. Connect the ToolNode and the result processor to the main graph
graph_builder.add_edge("tavily_search", "tool_result_processor")
graph_builder.add_edge("tool_result_processor", "llm")

graph = graph_builder.compile()