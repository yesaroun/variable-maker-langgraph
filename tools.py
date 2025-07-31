from langchain_core.tools import tool
from enum import Enum
import re


class InputType(Enum):
    WORD = "word"
    TEXT = "text"
    COMMAND = "command"


class CaseStyle(Enum):
    CAMEL_CASE = "camelCase"
    SNAKE_CASE = "snake_case"
    PASCAL_CASE = "PascalCase"
    KEBAB_CASE = "kebab-case"
    CONSTANT_CASE = "CONSTANT_CASE"


@tool
def smart_case_convert(text: str, case_style: str) -> str:
    """약어에 최적화된 스마트 케이스 변환 도구
    
    Args:
        text: 변환할 텍스트 (camelCase 형태의 약어)
        case_style: 변환할 케이스 스타일 (camelCase, snake_case, PascalCase, kebab-case, CONSTANT_CASE)
    
    Returns:
        변환된 텍스트
    """
    try:
        style = CaseStyle(case_style)
    except ValueError:
        return text
    
    # camelCase 패턴 감지 (소문자로 시작하고 중간에 대문자가 있는 경우)
    has_camel_case = re.search(r'^[a-z]+[A-Z]', text)
    
    if has_camel_case:
        # camelCase를 단어로 분리하여 변환
        words = re.sub(r'([a-z])([A-Z])', r'\1 \2', text).split()
        
        if style == CaseStyle.CAMEL_CASE:
            return text  # 이미 camelCase
        elif style == CaseStyle.SNAKE_CASE:
            return "_".join(word.lower() for word in words)
        elif style == CaseStyle.PASCAL_CASE:
            return "".join(word.capitalize() for word in words)
        elif style == CaseStyle.KEBAB_CASE:
            return "-".join(word.lower() for word in words)
        elif style == CaseStyle.CONSTANT_CASE:
            return "_".join(word.upper() for word in words)
    else:
        # 단순 약어의 경우 (db, intl 등) - 대소문자만 변경
        if style == CaseStyle.CAMEL_CASE:
            return text.lower()
        elif style == CaseStyle.SNAKE_CASE:
            return text.lower()
        elif style == CaseStyle.PASCAL_CASE:
            return text.capitalize()
        elif style == CaseStyle.KEBAB_CASE:
            return text.lower()
        elif style == CaseStyle.CONSTANT_CASE:
            return text.upper()
    
    return text


@tool
def classify_input_type(text: str) -> str:
    """입력 텍스트의 타입을 분류하는 도구
    
    Args:
        text: 분류할 입력 텍스트
    
    Returns:
        입력 타입 (word, text, command)
    """
    text = text.strip()

    if text.startswith(":"):
        return InputType.COMMAND.value

    # 텍스트 체크 (공백이 있으면 텍스트로 간주)
    if " " in text or len(text.split()) > 1:
        return InputType.TEXT.value

    return InputType.WORD.value