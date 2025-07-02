"""Service A application with observability configured."""

from __future__ import annotations

import os
import socket

from fastapi import FastAPI, HTTPException

from .logging_config import configure_logging
from .metrics import configure_metrics
from .tracing import configure_tracing

app = FastAPI(title="Service A")


def configure_observability(application: FastAPI) -> None:
    """Configure metrics, tracing and logging."""
    instance_id = os.getenv("SERVICE_INSTANCE_ID", socket.gethostname())

    configure_metrics(application)
    configure_tracing(application, instance_id)

    global logger
    logger = configure_logging(instance_id)


configure_observability(app)


@app.get("/health")
async def health() -> dict[str, str]:
    """Simple healthcheck endpoint."""
    return {"status": "ok"}


@app.get("/compute")
async def compute(n: int = 10) -> dict[str, int]:
    """Return the sum of squares up to ``n``.

    Parameters
    ----------
    n: int
        Upper bound for the calculation. Must be between 0 and 100000.
    """

    if n < 0 or n > 100_000:
        raise HTTPException(
            status_code=400,
            detail="n must be between 0 and 100000",
        )

    result = sum(i * i for i in range(n))
    return {"input": n, "result": result}
