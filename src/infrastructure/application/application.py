import asyncio
from functools import partial
from typing import Callable, Coroutine, Iterable
from fastapi import APIRouter, FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from src.infrastructure.database.session import async_engine, Base
from contextlib import asynccontextmanager
import logging
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware


logger = logging.getLogger(__name__)

allowed_origins = [
    "http://localhost:3000",
    "https://localhost:3000"
]


# Init Database in memmory
async def init_db() -> None:
    """Initialize the database with tables."""
    try:
        logger.info("Creating database tables...")
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI application.
    Handles startup and shutdown events.
    """
    # Startup: Initialize the database
    try:
        await init_db()
        logger.info("Application startup completed successfully")

        startup_coroutines = []
        for task in app.state.startup_tasks:
            startup_coroutines.append(asyncio.create_task(task()))

        if startup_coroutines:
            logger.info(f"Running {len(startup_coroutines)} startup tasks...")
            await asyncio.gather(*startup_coroutines)

        logger.info("Application startup completed successfully")
    except Exception as e:
        logger.critical(f"Application startup failed: {e}")
        raise

    yield  # Application runs here

    # Shutdown: Cleanup resources
    logger.info("Application shutting down...")


def create(
    *_,
    rest_routers: Iterable[APIRouter],
    startup_tasks: Iterable[Callable[[], Coroutine]] | None = None,
    shutdown_tasks: Iterable[Callable[[], Coroutine]] | None = None,
    **kwargs,
) -> FastAPI:
    """The application factory using FastAPI framework.
    🎉 Only passing routes is mandatory to start.
    """

    # Initialize the base FastAPI application
    app = FastAPI(**kwargs, lifespan=lifespan)

    # Add middlewares
    app.add_middleware(HTTPSRedirectMiddleware)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.state.startup_tasks = startup_tasks or []
    app.state.shutdown_tasks = shutdown_tasks or []

    # Include REST API routers
    for router in rest_routers:
        app.include_router(router)

    return app
