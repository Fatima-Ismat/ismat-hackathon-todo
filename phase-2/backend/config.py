"""
Configuration management for Phase 2 Backend
Uses pydantic-settings for environment variables

Enhancements for T027:
- Typed configuration fields
- Validation and defaults
- Environment variable parsing
- Configuration sections for different concerns
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator, Field
from typing import List, Dict, Any, Optional
import os


class Settings(BaseSettings):
    """
    Application settings with environment-based configuration

    Loads from .env file or environment variables
    """

    # App settings
    APP_NAME: str = Field(default="Hackathon Todo API", description="Application name")
    APP_VERSION: str = Field(default="2.0.0", description="Application version")
    DEBUG: bool = Field(default=False, description="Debug mode")

    # Database Configuration
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://user:password@localhost:5432/hackathon_todo",
        description="PostgreSQL database URL with asyncpg driver"
    )
    DATABASE_POOL_SIZE: int = Field(default=10, description="Database connection pool size")
    DATABASE_MAX_OVERFLOW: int = Field(default=20, description="Max database connections overflow")

    # JWT Authentication Configuration
    JWT_SECRET_KEY: str = Field(
        default="change-this-secret-key-in-production",
        description="Secret key for JWT signing (CHANGE IN PRODUCTION!)"
    )
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    JWT_EXPIRY_MINUTES: int = Field(default=60, description="Access token expiry in minutes")
    REFRESH_TOKEN_EXPIRY_DAYS: int = Field(default=30, description="Refresh token expiry in days")

    # CORS Configuration
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:3001"],
        description="Allowed CORS origins"
    )

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS_ORIGINS from comma-separated string or list"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    # SMTP Configuration (Email notifications)
    SMTP_HOST: str = Field(default="smtp.gmail.com", description="SMTP server host")
    SMTP_PORT: int = Field(default=587, description="SMTP server port")
    SMTP_USER: str = Field(default="", description="SMTP username")
    SMTP_PASSWORD: str = Field(default="", description="SMTP password")
    SMTP_TLS: bool = Field(default=True, description="Use TLS for SMTP")

    @property
    def SMTP_CONFIG(self) -> Dict[str, Any]:
        """Return SMTP configuration as dictionary for agents"""
        return {
            "host": self.SMTP_HOST,
            "port": self.SMTP_PORT,
            "user": self.SMTP_USER,
            "password": self.SMTP_PASSWORD,
            "tls": self.SMTP_TLS,
        }

    # Push Notification Configuration
    PUSH_SERVICE_URL: str = Field(default="", description="Push notification service URL")
    PUSH_API_KEY: str = Field(default="", description="Push notification API key")

    @property
    def PUSH_CONFIG(self) -> Dict[str, Any]:
        """Return push notification configuration as dictionary for agents"""
        return {
            "service_url": self.PUSH_SERVICE_URL,
            "api_key": self.PUSH_API_KEY,
        }

    # MCP Server Configuration
    MCP_ENABLED: bool = Field(default=True, description="Enable MCP server endpoints")
    MCP_TOOLS_ENDPOINT: str = Field(default="/api/mcp/tools", description="MCP tools listing endpoint")
    MCP_CALL_ENDPOINT: str = Field(default="/api/mcp/call", description="MCP tool call endpoint")

    # Performance Configuration
    TASK_PAGE_SIZE: int = Field(default=100, description="Default pagination size for tasks")
    TASK_MAX_PAGE_SIZE: int = Field(default=1000, description="Maximum pagination size")
    NOTIFICATION_PAGE_SIZE: int = Field(default=50, description="Default pagination size for notifications")

    # Security Configuration
    BCRYPT_ROUNDS: int = Field(default=12, description="Bcrypt hashing rounds")
    PASSWORD_MIN_LENGTH: int = Field(default=8, description="Minimum password length")

    # Logging Configuration
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format string"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Ignore extra fields from environment
    )


# Create settings instance
settings = Settings()
