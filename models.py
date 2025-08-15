from typing import TypedDict, List, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from enum import Enum


class InputType(Enum):
    WORD = "word"
    TEXT = "text"


class CaseStyle(Enum):
    CAMEL_CASE = "camelCase"
    SNAKE_CASE = "snake_case"
    PASCAL_CASE = "PascalCase"
    KEBAB_CASE = "kebab-case"
    CONSTANT_CASE = "CONSTANT_CASE"


class State(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    input_type: InputType
    current_input: str
    is_korean: bool
    translated_word: str
    abbreviations: List[str]
    processed_text: str
    selected_case_style: CaseStyle


def is_korean(text: str) -> bool:
    """입력 텍스트가 한국어 여부 검사"""
    for char in text:
        if "가" <= char <= "힣":
            return True
    return False


def get_case_style_options() -> List[tuple]:
    """케이스 스타일 선택 옵션 반환"""
    return [
        (1, CaseStyle.CAMEL_CASE, "camelCase (예: userName)"),
        (2, CaseStyle.SNAKE_CASE, "snake_case (예: user_name)"),
        (3, CaseStyle.PASCAL_CASE, "PascalCase (예: UserName)"),
        (4, CaseStyle.KEBAB_CASE, "kebab-case (예: user-name)"),
        (5, CaseStyle.CONSTANT_CASE, "CONSTANT_CASE (예: USER_NAME)"),
    ]


def get_case_style_by_number(number: int) -> CaseStyle:
    """번호로 케이스 스타일 반환"""
    options = get_case_style_options()
    for num, case_style, _ in options:
        if num == number:
            return case_style
    return CaseStyle.CAMEL_CASE  # 기본값


def prompt_case_style_selection() -> CaseStyle:
    """사용자에게 케이스 스타일 선택을 요청"""
    print("\n변수명 케이스 스타일을 선택하세요:")
    options = get_case_style_options()
    for num, _, description in options:
        print(f"{num}. {description}")

    while True:
        try:
            choice = input("\n선택 (1-5): ").strip()
            number = int(choice)
            if 1 <= number <= 5:
                selected_style = get_case_style_by_number(number)
                print(f"선택된 스타일: {selected_style.value}")
                return selected_style
            else:
                print("1부터 5까지의 숫자를 입력해주세요.")
        except ValueError:
            print("올바른 숫자를 입력해주세요.")
        except KeyboardInterrupt:
            print("\n기본값(camelCase)을 사용합니다.")
            return CaseStyle.CAMEL_CASE
