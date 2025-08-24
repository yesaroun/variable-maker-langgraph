from enum import Enum
from typing import TypedDict, List, Annotated, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from pydantic import BaseModel


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


class ProcessRequest(BaseModel):
    """변수명 생성 요청 스키마"""
    input_text: str
    case_style: Optional[CaseStyle] = CaseStyle.CAMEL_CASE
    thread_id: Optional[str] = None

    class Config:
        use_enum_values = True


class ProcessResponse(BaseModel):
    """변수명 생성 응답 스키마"""
    success: bool
    result: dict
    message: str
    thread_id: Optional[str] = None


class CaseStyleOption(BaseModel):
    """케이스 스타일 옵션"""
    id: str
    name: str
    example: str


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
