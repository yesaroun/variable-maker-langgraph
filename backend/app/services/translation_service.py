from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")


class TranslationService:
    """번역 서비스"""

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
