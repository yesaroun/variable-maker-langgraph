import requests
from typing import Dict, Any, Optional

from config.settings import BACKEND_URL, DEFAULT_TIMEOUT


class VariableMakerAPIClient:
    """백엔드와 통신하는 클라이언트"""

    def __init__(self) -> None:
        self.base_url = BACKEND_URL

    def process_variable_request(
        self, user_input: str, case_style: str, thread_id: str
    ) -> Optional[Dict[str, Any]]:
        try:
            response = requests.post(
                f"{self.base_url}/variable/process",
                json={
                    "input_text": user_input,
                    "case_style": (
                        case_style.value if hasattr(case_style, "value") else case_style
                    ),
                    "thread_id": thread_id,
                },
                timeout=DEFAULT_TIMEOUT,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"백엔드 통신 오류: {e}")
