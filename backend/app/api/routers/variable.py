from fastapi import APIRouter, HTTPException

from ...schemas.variable import ProcessRequest, ProcessResponse
from ...api.deps import LangGraphDep

router = APIRouter()


@router.post("/process", response_model=ProcessResponse)
async def process_variable(request: ProcessRequest, langgraph_service: LangGraphDep):
    """변수명 생성 처리 엔드포인트"""
    try:
        if not request.input_text.strip():
            raise HTTPException(status_code=400, detail="입력 텍스트가 비어있습니다.")

        result = await langgraph_service.process_request(request.dict())

        if result.get("success", False):
            return ProcessResponse(
                success=True,
                result=result.get("result", {}),
                message="변수명 생성이 완료되었습니다.",
                thread_id=result.get("thread_id"),
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "처리 중 오류가 발생했습니다."),
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"처리 중 오류가 발생했습니다: {str(e)}"
        )


@router.get("/history/{thread_id}")
async def get_conversation_history(thread_id: str, langgraph_service: LangGraphDep):
    """대화 히스토리 조회"""
    try:
        history = langgraph_service.get_conversation_history(thread_id)
        return {"success": True, "thread_id": thread_id, "history": history}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"히스토리 조회 중 오류가 발생했습니다: {str(e)}"
        )
