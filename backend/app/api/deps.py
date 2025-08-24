from typing import Annotated
from fastapi import Depends

from ..services.langgraph_service import LangGraphService


def get_langgraph_service() -> LangGraphService:
    """LangGraph 서비스"""
    return LangGraphService


# 의존성 타입 어노테이션
LangGraphDep = Annotated[LangGraphService, Depends(get_langgraph_service)]
