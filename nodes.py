from langchain_core.messages import HumanMessage, AIMessage
from models import (
    State,
    is_korean,
    CaseStyle,
    prompt_case_style_selection,
)
from tools import classify_input_type, smart_case_convert
from services import (
    TranslationService,
    AbbreviationService,
    TextProcessingService,
    MessageFormatter,
)


def command_node(state: State) -> State:
    """명령어 처리 노드"""
    last_message = state["messages"][-1]
    content = last_message.content.strip().lower()

    if content in [":quit"]:
        state["messages"].append(AIMessage(content="프로그램을 종료합니다."))
        return state

    if content in [":help"]:
        help_msg = MessageFormatter.get_help_message()
        state["messages"].append(AIMessage(content=help_msg))
        return state

    if content in [":case"]:
        selected_style = prompt_case_style_selection()
        state["selected_case_style"] = selected_style
        state["messages"].append(
            AIMessage(
                content=f"케이스 스타일이 {selected_style.value}로 변경되었습니다."
            )
        )
        return state

    state["messages"].append(
        AIMessage(content="알 수 없는 명령어입니다. :help로 도움말을 확인하세요.")
    )
    return state


def word_node(state: State) -> State:
    """단어 처리 노드"""
    original_input = state["current_input"]
    state["is_korean"] = is_korean(original_input)
    case_style = state.get("selected_case_style", CaseStyle.CAMEL_CASE)

    # 번역 처리
    if state["is_korean"]:
        state["translated_word"] = TranslationService.translate_to_english(
            original_input
        )
    else:
        state["translated_word"] = original_input

    # 약어 생성 (camelCase로 받고 케이스 스타일 적용)
    camel_abbreviations = AbbreviationService.generate_abbreviations(
        state["translated_word"]
    )
    state["abbreviations"] = [
        smart_case_convert.invoke({"text": abbr, "case_style": case_style.value})
        for abbr in camel_abbreviations
    ]

    # 결과 메시지 생성
    result_msg = MessageFormatter.format_word_result(
        original_input,
        state["translated_word"],
        state["abbreviations"],
        state["is_korean"],
        case_style,
    )

    state["messages"].append(AIMessage(content=result_msg))
    return state


def text_node(state: State) -> State:
    """텍스트 처리 노드"""
    original_input = state["current_input"]
    case_style = state.get("selected_case_style", CaseStyle.CAMEL_CASE)

    # camelCase로 받고 케이스 스타일 적용
    camel_result = TextProcessingService.process_text(original_input)
    
    lines = camel_result.split("\n")
    converted_lines = []
    
    for line in lines:
        if ":" in line:
            concept, variants = line.split(":", 1)
            variant_list = [v.strip() for v in variants.split(",")]
            converted_variants = [
                smart_case_convert.invoke({"text": v, "case_style": case_style.value})
                for v in variant_list
            ]
            converted_lines.append(
                f"{concept.strip()}: {', '.join(converted_variants)}"
            )
        else:
            converted_lines.append(line)
    
    processed_result = "\n".join(converted_lines)
    state["processed_text"] = processed_result

    result_msg = MessageFormatter.format_text_result(original_input, processed_result)
    state["messages"].append(AIMessage(content=result_msg))
    return state


def chatbot_node(state: State) -> State:
    """메인 챗봇 노드 - 입력 분류 및 상태 설정"""
    last_message = state["messages"][-1]

    if not isinstance(last_message, HumanMessage):
        return state

    original_input = last_message.content.strip()
    state["current_input"] = original_input
    input_type_result = classify_input_type.invoke({"text": original_input})
    from models import InputType
    state["input_type"] = InputType(input_type_result)

    return state
