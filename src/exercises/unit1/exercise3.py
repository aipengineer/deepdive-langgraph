from typing import Annotated, Literal

from langchain_core.messages import (
    AIMessage,
    ChatMessage,
    HumanMessage,
    SystemMessage,
)
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

# Define the state for the agent
class State(TypedDict):
    messages: Annotated[list, add_messages]
    classification: str
    confidence: float

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
    classification = state["classification"]
    
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
                    "You are a helpful AI assistant. "
                    f"Here is a classification of the user's intent:{classification}"
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

def classify(state: State) -> State:
    """
    Classify the message and return the classification and confidence.
    """
    messages = state["messages"]
    last_message = messages[-1]
    try:
        # For now, we will use a simple heuristic to classify the message
        if "weather" in last_message.content:
            classification = "weather"
            confidence = 0.9
        else:
            classification = "not weather"
            confidence = 0.9
    except Exception as e:
        # If the last message is not a HumanMessage, we will raise an error.
        raise ValueError(f"The last message is not a HumanMessage, so it cannot be classified. Last message: {last_message}, Error: {e}")
    
    return {
        "messages": [ChatMessage(
            content=f"The classification is {classification} with confidence {confidence}"
        )],
        "classification": classification,
        "confidence": confidence,
    }

# Implement the following functions

def respond_to_weather(state: State) -> dict:
    """Respond to the weather classification."""
    # This function should return a dict with the key "messages" and a list of messages as the value
    # The messages should be a response to the weather classification
    # The last message in the state is the user's message
    # The classification is "weather"
    # The confidence is 0.9
    raise NotImplementedError

def respond_to_not_weather(state: State) -> dict:
    """Respond to the not weather classification."""
    # This function should return a dict with the key "messages" and a list of messages as the value
    # The messages should be a response to the not weather classification
    # The last message in the state is the user's message
    # The classification is "not weather"
    # The confidence is 0.9
    raise NotImplementedError

graph_builder.add_node("llm", llm_node)
graph_builder.add_node("classify", classify)
graph_builder.add_node("weather", respond_to_weather)
graph_builder.add_node("not_weather", respond_to_not_weather)

# Define the routing function
def route_classification(state: State) -> Literal["weather", "not_weather", END]:
    """Route the message to the correct node based on the classification."""
    if state["classification"] == "weather":
        return "weather"
    elif state["classification"] == "not weather":
        return "not_weather"
    else:
        # If the classification is not valid, we will end the graph.
        return END

# Add edges
graph_builder.add_edge(START, "llm")
graph_builder.add_edge("llm", "classify")
graph_builder.add_conditional_edges("classify", route_classification)
graph_builder.add_edge("weather", END)
graph_builder.add_edge("not_weather", END)

# Finally, we "compile" the graph
graph = graph_builder.compile()