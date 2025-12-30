from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.auth import router as auth_router
from .api.tasks import router as tasks_router
from .api.tags import router as tags_router
from .api.notifications import router as notifications_router
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

# Set up CORS middleware
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    "https://*.hf.space",
    "https://huggingface.co",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"Validation error: {exc}")
    logger.error(f"Request body: {await request.body()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )

# Custom logging middleware
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Include API routers
app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(tags_router)
app.include_router(notifications_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo Full-Stack Application API"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "message": "API is running"}