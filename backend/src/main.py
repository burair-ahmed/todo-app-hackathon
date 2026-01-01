from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.auth import router as auth_router
from .api.tasks import router as tasks_router
from .api.tags import router as tags_router
from .api.notifications import router as notifications_router
from .api.chat_api import router as chat_router
from .config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    redirect_slashes=False
)

# Custom logging middleware
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    try:
        response = await call_next(request)
        logger.info(f"Response status: {response.status_code}")
        return response
    except Exception as e:
        logger.exception(f"Exception in request processing: {e}")
        raise

# Set up CORS middleware - Added LAST so it is the OUTERMOST middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False, # Set to False when using allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_cors_debug_headers(request, call_next):
    response = await call_next(request)
    if "access-control-allow-origin" not in [k.lower() for k in response.headers.keys()]:
        logger.warning(f"Response missing CORS headers for {request.method} {request.url}")
    return response

from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"Validation error: {exc}")
    # Don't try to read body here as it might be already consumed or cause issues in some cases
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

from .services.task_service import check_upcoming_reminders
import asyncio

async def reminder_loop():
    """Background loop to check for upcoming task reminders every minute."""
    while True:
        try:
            # Run sync DB check in thread to avoid blocking main loop
            await asyncio.to_thread(check_upcoming_reminders)
        except Exception as e:
            logger.error(f"Error in reminder loop: {e}")
        await asyncio.sleep(60)

@app.on_event("startup")
async def start_background_tasks():
    """Start background tasks on app startup."""
    asyncio.create_task(reminder_loop())

# Include API routers
app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(tags_router)
app.include_router(notifications_router)
from .api.chatkit_api import router as chatkit_router
app.include_router(chatkit_router, prefix="/api/chatkit", tags=["chatkit"])

# Include chat_router after specific api routes to avoid capturing "chatkit" as user_id
app.include_router(chat_router, prefix="/api/{user_id}", tags=["chat"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo Full-Stack Application API"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "message": "API is running"}