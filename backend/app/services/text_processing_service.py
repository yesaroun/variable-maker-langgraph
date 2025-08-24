from typing import List
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")


class AbbreviationService:
    """약어 생성 서비스"""

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
    """텍스트 처리 서비스"""

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
