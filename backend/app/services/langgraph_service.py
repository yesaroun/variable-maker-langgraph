from typing import Dict, Any
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage

from ..schemas.variable import State, CaseStyle, InputType
from ..utils.nodes import chatbot_node, word_node, text_node


class LangGraphFactory:
    """LangGraph 팩토리"""

    @staticmethod
    def create_graph() -> StateGraph:
        """새로운 LangGraph 인스턴스 생성"""
        graph = StateGraph(State)

        graph.add_node("chatbot", chatbot_node)
        graph.add_node("word", word_node)
        graph.add_node("text", text_node)

        graph.add_edge(START, "chatbot")

        graph.add_conditional_edges(
            "chatbot",
            lambda state: state["input_type"].value,
            {"word": "word", "text": "text"},
        )

        graph.add_edge("word", END)
        graph.add_edge("text", END)

        # 각 요청마다 새로운 메모리 체크포인터
        memory = MemorySaver()
        return graph.compile(checkpointer=memory)


class LangGraphService:
    """LangGraph 서비스"""

    @staticmethod
    async def process_request(input_data: Dict[str, Any]) -> Dict[str, Any]:
        """요청 처리"""
        thread_id = input_data.get("thread_id", f"thread_{id(input_data)}")

        # 새로운 그래프 인스턴스 생성
        graph = LangGraphFactory.create_graph()

        try:
            input_text = input_data.get("input_text", "")
            case_style = input_data.get("case_style", CaseStyle.CAMEL_CASE.value)

            if isinstance(case_style, str):
                case_style = CaseStyle(case_style)

            initial_state = {
                "messages": [HumanMessage(content=input_text)],
                "input_type": InputType.WORD,
                "current_input": "",
                "is_korean": False,
                "translated_word": "",
                "abbreviations": [],
                "processed_text": "",
                "selected_case_style": case_style,
            }

            config = {"configurable": {"thread_id": thread_id}}
            final_state = await graph.ainvoke(initial_state, config=config)
            result = LangGraphService._format_result(final_state)

            return {
                "success": True,
                "result": result,
                "thread_id": thread_id,
                "input_type": final_state.get("input_type", InputType.WORD).value,
            }

        except Exception as e:
            print(f"LangGraph 처리 중 오류: {str(e)}")
            return {
                "success": False,
                "result": {},
                "error": str(e),
                "thread_id": thread_id,
            }
        finally:
            # 그래프 인스턴스 정리
            graph = None

    @staticmethod
    def _format_result(state: State) -> Dict[str, Any]:
        """결과 포맷팅"""
        result = {
            "input_type": state.get("input_type", InputType.WORD).value,
            "current_input": state.get("current_input", ""),
            "is_korean": state.get("is_korean", False),
            "case_style": state.get("selected_case_style", CaseStyle.CAMEL_CASE).value,
        }

        if state.get("input_type") == InputType.WORD:
            result.update(
                {
                    "translated_word": state.get("translated_word", ""),
                    "abbreviations": state.get("abbreviations", []),
                }
            )
        else:
            result.update(
                {
                    "processed_text": state.get("processed_text", ""),
                }
            )

        # 메시지 히스토리 추가
        messages = state.get("messages", [])
        if messages:
            ai_messages = [
                msg
                for msg in messages
                if hasattr(msg, "content")
                and getattr(msg, "__class__", None).__name__ == "AIMessage"
            ]
            if ai_messages:
                result["formatted_response"] = ai_messages[-1].content

        return result

    @staticmethod
    def get_conversation_history(thread_id: str) -> Dict[str, Any]:
        # TODO: 추후에 DB로 변경하기
        """대화 히스토리 조회"""
        return {
            "thread_id": thread_id,
            "messages": [],
            "note": "현재는 요청별로 독립된 인스턴스를 사용하므로 히스토리가 유지되지 않습니다.",
        }
