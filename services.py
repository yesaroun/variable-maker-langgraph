from typing import List
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from models import CaseStyle

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")


class TranslationService:
    @staticmethod
    def translate_to_english(korean_word: str) -> str:
        """한국어 단어를 영어로 번역"""
        try:
            prompt = HumanMessage(
                content=(
                    f"Translate '{korean_word}' to English."
                    "Return only the translated word in English, without any additional text, explanation, or punctuation. "
                    "For example, for '고양이', return 'cat'."
                )
            )
            response = llm.invoke([prompt])
            return response.content.strip()
        except Exception:
            return "translation_error"


class AbbreviationService:
    @staticmethod
    def generate_abbreviations(word: str) -> List[str]:
        """영어 단어에 대한 약어 생성 (camelCase로 고정 반환)"""
        try:
            prompt = HumanMessage(
                content=(
                    f"Generate programming variable abbreviations for: '{word}'\n\n"
                    f"Rules:\n"
                    f"1. For single words: provide common abbreviations (e.g., 'international' → 'intl', 'int')\n"
                    f"2. For phrases: create meaningful acronyms and shortened forms\n"
                    f"3. Use camelCase for multi-word concepts\n"
                    f"4. If no good abbreviations exist, return empty\n\n"
                    f"Examples:\n"
                    f"- 'database' → 'db'\n"
                    f"- 'Christmas tree' → 'xmasTree', 'christmasTree'\n"
                    f"- 'Tax reduction for employees' → 'taxReduction', 'empTaxReduction', 'taxRed'\n"
                    f"- 'BTS' → 'bts' (already abbreviated)\n\n"
                    f"Return only space-separated camelCase abbreviations, or empty if none suitable:"
                )
            )
            response = llm.invoke([prompt])
            content = response.content.strip()

            if not content or content.lower() in ["empty", "none", "no abbreviations"]:
                return []

            abbreviations = content.split()
            filtered_abbreviations = [
                abbr for abbr in abbreviations if abbr != "." and len(abbr) > 0
            ]
            return filtered_abbreviations
        except Exception:
            return []


class TextProcessingService:
    @staticmethod
    def process_text(text: str) -> str:
        """텍스트에서 변수명 후보 추출 및 처리 (camelCase로 고정 반환)"""
        try:
            prompt = HumanMessage(
                content=(
                    f"Analyze this Korean/English text and identify the main business/domain concepts that should become variable names. "
                    f"Ignore common words like '변수', '만들어주세요', '해주세요', etc.\n"
                    f"Text: '{text}'\n\n"
                    f"Focus on:\n"
                    f"- Business terms\n"
                    f"- Domain-specific concepts\n"
                    f"- Key nouns that represent data or entities\n\n"
                    f"For each concept, provide camelCase style variable names and abbreviated versions:\n"
                    f"Format: concept_name: camelCaseVersion, abbr1, abbr2\n"
                    f"Example style (camelCase): smallBusinessEmployeeTax, smbEmpTax, sbeTax\n\n"
                    f"Output only the results:"
                )
            )
            response = llm.invoke([prompt])
            return response.content.strip()
        except Exception:
            return "Error processing text."


class MessageFormatter:
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

    @staticmethod
    def get_help_message() -> str:
        """도움말 메시지 반환"""
        return (
            "Variable Maker 사용법:\n\n"
            "단어 입력 (약어 생성):\n"
            "- 예시: 중취감, international, 데이터베이스\n"
            "- 결과: 한국어는 영어 번역 후 약어 생성\n"
            "- 케이스 스타일: camelCase, snake_case, PascalCase, kebab-case, CONSTANT_CASE\n\n"
            "문장/텍스트 입력 (변수명 추출):\n"
            "- 예시: 중소기업 취업자 감면을 변수로 만들어주세요\n"
            "- 팁: 핵심 비즈니스 용어에 집중합니다\n"
            "- 팁: '변수', '만들어주세요' 같은 요청 문구는 무시됩니다\n\n"
            "명령어:\n"
            "- :quit: 프로그램 종료\n"
            "- :help: 이 메시지 출력\n"
            "- :case: 케이스 스타일 변경"
        )
