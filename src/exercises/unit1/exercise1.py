from langchain_core.messages import (
    AIMessage,
    ChatMessage,
    HumanMessage,
    SystemMessage,
)
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict

# ---- Instructions ----
#
# 1. Define a State type using TypedDict with a 'messages' key.
#    - The 'messages' key should be annotated with add_messages.
#    - The type of 'messages' should be a list of HumanMessage or AIMessage.
# 2. Implement the llm_node function.
#    - This function should take in the current graph state and call an LLM.
#    - Use the last message in the state to prompt the LLM.
#    - If the last message is a HumanMessage, convert it to a ChatMessage if necessary.
#    - Include error handling for API failures.
#    - Return a new AIMessage to be added to the state.
# 3. Create a StateGraph.
#    - Add the llm_node to the graph.
#    - Add edges to connect the START node to the llm_node and the llm_node to the END node.
#    - Compile the graph.
#
# ---- End of Instructions ----

# Define the state for the agent
class State(TypedDict):
    # YOUR CODE HERE
    ...


# Initialize the LLM
llm = ChatOpenAI(model="gpt-4o")

def llm_node(state: State) -> dict[str, list[AIMessage]]:
    """
    This node is executed whenever the graph is invoked.
    It takes in the current graph state, calls an LLM, and returns a new message to be added to the state.
    """
    # YOUR CODE HERE
    ...

# This is the "builder" pattern that is used throughout LangChain
graph_builder = StateGraph(State)
# We add the node to the graph, using the "name"
graph_builder.add_node("llm", llm_node)
# We can add simple edges that go from node a -> b
graph_builder.add_edge(START, "llm")
graph_builder.add_edge("llm", END)

# Finally, we "compile" the graph. This is the object we will use to call the graph
graph = graph_builder.compile()