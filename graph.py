from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver

from models import State
from nodes import chatbot_node, word_node, text_node


def create_graph():
    """LangGraph 생성 및 설정"""
    graph = StateGraph(State)

    graph.add_node("chatbot", chatbot_node)
    graph.add_node("word", word_node)
    graph.add_node("text", text_node)

    graph.add_edge(START, "chatbot")

    # chatbot에서 직접 조건부 라우팅
    graph.add_conditional_edges(
        "chatbot",
        lambda state: state["input_type"].value,
        {"word": "word", "text": "text"},
    )

    graph.add_edge("word", END)
    graph.add_edge("text", END)

    memory = MemorySaver()
    return graph.compile(checkpointer=memory)
