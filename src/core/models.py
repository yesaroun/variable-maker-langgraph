from typing import TypedDict, List, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from enum import Enum
from dataclasses import dataclass


class InputType(Enum):
    WORD = "word"
    TEXT = "text"


class CaseStyle(Enum):
    CAMEL_CASE = "camelCase"
    SNAKE_CASE = "snake_case"
    PASCAL_CASE = "PascalCase"
    KEBAB_CASE = "kebab-case"
    CONSTANT_CASE = "CONSTANT_CASE"


@dataclass
class ChatMessage:
    """채팅 메시지를 관리하는 데이터 클래스"""

    role: str  # "user" 또는 "assistant"
    content: str

    def __post_init__(self):
        if self.role not in ["user", "assistant"]:
            raise ValueError(
                f"role은 'user' 또는 'assistant'여야 합니다. 입력값: {self.role}"
            )


@dataclass
class ChatSession:
    """채팅 세션을 관리하는 데이터 클래스"""

    title: str
    messages: List[ChatMessage]
    thread_id: str

    def __post_init__(self):
        if self.messages is None:
            self.messages = []

    def add_message(self, role: str, content: str) -> None:
        """새로운 메시지 추가"""
        self.messages.append(ChatMessage(role=role, content=content))


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
