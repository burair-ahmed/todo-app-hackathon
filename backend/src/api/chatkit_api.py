from fastapi import APIRouter, Request, Depends, Response
from fastapi.responses import StreamingResponse, JSONResponse
from ..services.chatkit_service import GeminiChatKitServer
from ..middleware.jwt_auth import get_chatkit_user
import json

router = APIRouter()
server = GeminiChatKitServer()

@router.post("/chat")
async def chatkit_chat(request: Request, current_user: dict = Depends(get_chatkit_user)):
    """
    Endpoint for ChatKit interaction.
    """
    # Read the raw body
    body = await request.body()
    
    # Context can be used to pass user info etc.
    # Pass the real user_id (UUID) from the authenticated user
    context = {"user_id": str(current_user["user_id"])}
    
    # Process the request
    # server.process returns a StreamingResult or NonStreamingResult
    try:
        result = await server.process(body, context)
        
        # Determine if we should stream
        is_streaming = hasattr(result, "__aiter__")
        
        if is_streaming:
            return StreamingResponse(
                result,
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no",  # Disable buffering for Nginx if applicable
                }
            )
        
        # Handle NonStreamingResult
        if hasattr(result, "json"):
             return Response(content=result.json, media_type="application/json")
        elif hasattr(result, "body"):
             return Response(content=result.body, media_type="application/json")
        else:
            return JSONResponse(content=result)

    except Exception as e:
        import traceback
        with open("error.log", "w") as f:
            f.write(traceback.format_exc())
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})
