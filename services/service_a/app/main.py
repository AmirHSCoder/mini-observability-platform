"""Service A application with observability configured."""

from __future__ import annotations

import os

from fastapi import FastAPI, HTTPException
from loguru import logger
from opentelemetry.exporter.otlp.proto.http.trace_exporter import \
    OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Service A")


def configure_observability(application: FastAPI) -> None:
    """Configure metrics, tracing and logging."""

    # Prometheus metrics
    Instrumentator().instrument(application).expose(application)

    # OpenTelemetry tracing
    resource = Resource.create({"service.name": "service_a"})
    trace_provider = TracerProvider(resource=resource)

    otlp_endpoint = os.environ.get(
        "OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318"
    )
    trace_provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(endpoint=f"{otlp_endpoint}/v1/traces"))
    )

    FastAPIInstrumentor.instrument_app(application, tracer_provider=trace_provider)

    # Structured logging
    LoggingInstrumentor().instrument(set_logging_format=True)
    logger.info("Observability configured")


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
        raise HTTPException(status_code=400, detail="n must be between 0 and 100000")

    result = sum(i * i for i in range(n))
    return {"input": n, "result": result}
