from langchain_core.messages import HumanMessage, AIMessage
from graph import create_graph
from models import CaseStyle


def chat_loop():
    """대화형 CLI 루프 실행"""
    print("Variable Maker Chatbot에 오신 것을 환영합니다!")
    print("단어나 텍스트를 입력하면 변수명을 생성해드립니다.")
    print(":help로 도움말, :case로 케이스 스타일 변경, :quit로 종료하세요.\n")

    app = create_graph()
    thread_id = "user_session_1"
    config = {"configurable": {"thread_id": thread_id}}

    # 현재 케이스 스타일을 세션에서 관리
    current_case_style = CaseStyle.CAMEL_CASE

    while True:
        try:
            user_input = input("입력: ").strip()

            if not user_input:
                continue

            if user_input.lower() in [":quit"]:
                print("\n프로그램이 종료됩니다.")
                break

            initial_state = {
                "messages": [HumanMessage(content=user_input)],
                "input_type": None,
                "current_input": "",
                "is_korean": False,
                "translated_word": "",
                "abbreviations": [],
                "processed_text": "",
                "selected_case_style": current_case_style,
            }

            result = app.invoke(initial_state, config)

            # 케이스 스타일이 변경되었다면 현재 스타일 업데이트
            if "selected_case_style" in result:
                current_case_style = result["selected_case_style"]

            for message in result["messages"]:
                if isinstance(message, AIMessage):
                    print(f"{message.content}")

            print()

        except KeyboardInterrupt:
            print("\n\n프로그램을 종료합니다.")
            break
        except EOFError:
            print("\n\n프로그램을 종료합니다.")
            break
        except Exception as e:
            print(f"오류가 발생했습니다: {e}")
            print("다시 시도해주세요.\n")
