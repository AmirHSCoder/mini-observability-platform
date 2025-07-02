"""OpenTelemetry tracing setup for Service A."""

from __future__ import annotations

import os

from fastapi import FastAPI
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def configure_tracing(app: FastAPI, instance_id: str) -> None:
    """Configure tracing for the application."""
    resource = Resource.create(
        {"service.name": "service_a", "service.instance.id": instance_id}
    )
    provider = TracerProvider(resource=resource)

    otlp_endpoint = os.environ.get(
        "OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318"
    )
    provider.add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporter(endpoint=f"{otlp_endpoint}/v1/traces")
        )  # noqa: E501
    )

    FastAPIInstrumentor.instrument_app(app, tracer_provider=provider)
