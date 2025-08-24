from enum import Enum
from typing import List, Optional
from dataclasses import dataclass, field


@dataclass
class ChatMessage:
    role: str  # "user" or "assistant"
    content: str


@dataclass
class ChatSession:
    title: str
    messages: List[ChatMessage] = field(default_factory=list)
    thread_id: Optional[str] = None

    def add_message(self, role: str, content: str):
        """메시지를 추가합니다."""
        self.messages.append(ChatMessage(role=role, content=content))


class CaseStyle(Enum):
    CAMEL_CASE = "camelCase"
    SNAKE_CASE = "snake_case"
    PASCAL_CASE = "PascalCase"
    KEBAB_CASE = "kebab-case"
    CONSTANT_CASE = "CONSTANT_CASE"


def get_case_style_options() -> List[tuple]:
    """케이스 스타일 선택 옵션 반환"""
    return [
        (1, CaseStyle.CAMEL_CASE, "camelCase (예: userName)"),
        (2, CaseStyle.SNAKE_CASE, "snake_case (예: user_name)"),
        (3, CaseStyle.PASCAL_CASE, "PascalCase (예: UserName)"),
        (4, CaseStyle.KEBAB_CASE, "kebab-case (예: user-name)"),
        (5, CaseStyle.CONSTANT_CASE, "CONSTANT_CASE (예: USER_NAME)"),
    ]
