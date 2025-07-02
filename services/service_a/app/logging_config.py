"""Logging setup for Service A."""

from __future__ import annotations

from loguru import logger
from opentelemetry.instrumentation.logging import LoggingInstrumentor


def configure_logging(instance_id: str):
    """Configure loguru and return a bound logger."""
    LoggingInstrumentor().instrument(set_logging_format=True)
    bound = logger.bind(instance_id=instance_id)
    bound.info("Logging configured")
    return bound
