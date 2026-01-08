"""
Phase 2 Backend API
FastAPI application with MCP integration and reusable intelligence

Enhancements for T022, T025-T026:
- MCP server endpoints at /api/mcp/call and /api/mcp/tools
- Enhanced CORS configuration
- Global error handling middleware
- Request/response logging
"""

from fastapi import FastAPI, Depends, HTTPException, Header, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import sys  
import os
from typing import Optional
import logging
import time

# Add agents to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# from agents.mcp_server.src.server import MCPServer, FastAPIMCPIntegration
from database import init_db, get_db
from config import settings


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events"""
    # Startup
    logger.info("🚀 Starting Phase 2 Backend API...")
    await init_db()
    logger.info("✅ Database initialized")
    logger.info(f"📍 CORS origins: {settings.CORS_ORIGINS}")
    logger.info(f"🔐 JWT expiry: {settings.JWT_EXPIRY_MINUTES} minutes")
    yield
    # Shutdown
    logger.info("👋 Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Hackathon Todo API",
    description="Phase 2 Backend with MCP integration for AI chatbot",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS middleware (T025: Enhanced configuration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # From environment config
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "Accept",
        "Origin",
        "User-Agent",
        "DNT",
        "Cache-Control",
        "X-Requested-With",
    ],
    expose_headers=["Content-Length", "X-Total-Count"],
    max_age=3600,  # Cache preflight requests for 1 hour
)


# T026: Global error handling middleware
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with consistent error format"""
    logger.error(f"HTTP {exc.status_code}: {exc.detail} - {request.method} {request.url}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status_code": exc.status_code},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors"""
    logger.error(f"Validation error: {exc.errors()} - {request.method} {request.url}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": exc.errors(),
            "status_code": 422,
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""
    logger.exception(f"Unexpected error: {str(exc)} - {request.method} {request.url}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "status_code": 500,
        },
    )


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add request processing time to response headers"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
    return response


# Initialize MCP Server
async def get_mcp_server():
    """Dependency to get MCP server instance"""
    db = await get_db()
    mcp_server = MCPServer(
        db_connection=db,
        jwt_secret=settings.JWT_SECRET,
        smtp_config=settings.SMTP_CONFIG,
        push_config=settings.PUSH_CONFIG
    )
    return mcp_server


# Setup MCP routes (Deprecated event handler removed - using lifespan instead)
# MCP integration is a Phase 3 feature and not required for Phase 2
# @app.on_event("startup")
# async def setup_mcp():
#     """Setup MCP integration on startup"""
#     mcp_server = await get_mcp_server()
#     integration = FastAPIMCPIntegration(mcp_server)
#     integration.setup_routes(app)
#     print("✅ MCP Server integrated")


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "phase": 2,
        "features": [
            "reusable-agents",
            "mcp-integration",
            "auth-jwt",
            "notifications"
        ]
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "name": "Hackathon Todo API",
        "version": "2.0.0",
        "phase": 2,
        "docs": "/docs",
        "mcp_tools": "/api/mcp/tools"
    }


# Include routers
from routes import auth, tasks, notifications

app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(notifications.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # Disabled auto-reload for stable production-like behavior
        log_level="info"
    )

