from datetime import UTC, datetime
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel

from slo_sentinel import SERVICE_NAME, __version__


class HealthResponse(BaseModel):
    status: Literal["ok"]
    service: str
    version: str
    time: datetime


def create_app() -> FastAPI:
    app = FastAPI(
        title=SERVICE_NAME,
        version=__version__,
        openapi_url="/api/openapi.json",
        docs_url="/api/docs",
        redoc_url=None,
    )

    @app.get("/health", response_model=HealthResponse, tags=["ops"])
    async def health() -> HealthResponse:
        """Liveness check: the Worker is up and serving requests.

        Later this will also report cron freshness (is the prober still
        running?) so it doubles as a readiness signal for smoke tests.
        """
        return HealthResponse(
            status="ok",
            service=SERVICE_NAME,
            version=__version__,
            time=datetime.now(UTC),
        )

    return app


app = create_app()