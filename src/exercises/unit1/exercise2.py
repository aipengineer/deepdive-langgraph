from langchain_core.messages import (
    AIMessage,
    ChatMessage,
    HumanMessage,
    SystemMessage,
)
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from typing import Annotated, Sequence
from typing_extensions import TypedDict

# Define the state for the agent
class State(TypedDict):
    messages: Annotated[list[ChatMessage], add_messages]
    summary: str
    window_size: int

def summarize_messages(messages: Sequence[ChatMessage], llm: ChatOpenAI, max_tokens: int=3000) -> ChatMessage:
    """
    Summarize the provided messages.

    Args:
        messages (Sequence[ChatMessage]): The messages to summarize.
        llm (ChatOpenAI): The LLM to use for summarization.
        max_tokens (int): The maximum number of tokens to use for the summary.
    """
    try:
        summary = llm.invoke([
            SystemMessage(content="Summarize the conversation below:"),
            ChatMessage(content="\n".join([str(m) for m in messages]))
        ])
    except Exception:
        # If for whatever reason, the summarization LLM fails, we will return a canned response
        summary = ChatMessage(content="No summary available.")
    return summary

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4o")

# Build the graph
graph_builder = StateGraph(State)

def llm_node(state: State) -> dict[str, list[AIMessage]]:
    """
    This node is executed whenever the graph is invoked.
    It takes in the current graph state, calls an LLM, and returns a new message to be added to the state.
    """
    messages = state["messages"]
    window_size = state["window_size"]
    summary = state["summary"]
    
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
            # For this example, we will use the last message in the state as the message to prompt the LLM.
            history = "\n".join([str(m) for m in messages[-window_size:]])
            new_message = llm.invoke([
                SystemMessage(content=(
                    "You are a helpful AI assistant. "
                    f"Here is your chat history:\n\n{history}"
                    f"Here is a summary of the chat history:\n\n{summary}"
                )),
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

def summarize(state: State) -> State:
    """Summarize the last 5 messages."""
    messages = state["messages"]
    window_size = state["window_size"]
    
    # Summarize the messages
    summary = summarize_messages(messages[-window_size:], llm)
    return {"summary": summary.content, "window_size": window_size}

graph_builder.add_node("llm", llm_node)
graph_builder.add_node("summarize", summarize)
# Add edges
graph_builder.add_edge(START, "llm")
graph_builder.add_edge("llm", "summarize")
graph_builder.add_edge("summarize", END)

graph = graph_builder.compile()