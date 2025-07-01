from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

app = FastAPI(title="Service A")

# Prometheus metrics
Instrumentator().instrument(app).expose(app)

# OpenTelemetry Tracing
resource = Resource.create({"service.name": "service_a"})
trace_provider = TracerProvider(resource=resource)
trace_provider.add_span_processor(
    BatchSpanProcessor(
        OTLPSpanExporter(endpoint="http://otel-collector:4318/v1/traces")
    )
)
FastAPIInstrumentor.instrument_app(app, tracer_provider=trace_provider)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/compute")
async def compute(n: int = 10):
    # Dummy CPU-intensive calculation
    result = sum(i * i for i in range(n))
    return {"input": n, "result": result}
