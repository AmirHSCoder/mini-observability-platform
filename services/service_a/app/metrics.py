"""Prometheus metrics setup for Service A."""

from __future__ import annotations

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator


def configure_metrics(app: FastAPI) -> None:
    """Expose Prometheus metrics for the given app."""
    Instrumentator().instrument(app).expose(app)
