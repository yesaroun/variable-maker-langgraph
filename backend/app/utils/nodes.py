from typing import List
from langchain_core.messages import HumanMessage, AIMessage
from ..schemas.variable import State, is_korean, CaseStyle, InputType
from .tools import classify_input_type, smart_case_convert
from ..services.translation_service import TranslationService
from ..services.text_processing_service import (
    AbbreviationService,
    TextProcessingService,
)


class MessageFormatter:
    """메시지 포맷팅 유틸리티"""

    @staticmethod
    def format_word_result(
        original_word: str,
        translated_word: str,
        abbreviations: List[str],
        is_korean: bool,
        case_style: CaseStyle,
    ) -> str:
        """단어 결과 메시지 포맷팅"""
        abbrev_text = ", ".join(abbreviations) if abbreviations else "없음"
        case_style_text = f" ({case_style.value})"

        if is_korean:
            return f"'{original_word}' → '{translated_word}' 약어{case_style_text}: {abbrev_text}"
        else:
            return f"'{original_word}' 약어{case_style_text}: {abbrev_text}"

    @staticmethod
    def format_text_result(original_text: str, processed_result: str) -> str:
        """텍스트 결과 메시지 포맷팅"""
        return f"텍스트 분석 결과:\n{processed_result}"


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

    state["input_type"] = InputType(input_type_result)

    return state
