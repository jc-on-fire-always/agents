import os
import gradio as gr
from openinference.instrumentation.openai import OpenAIInstrumentor
from opentelemetry import trace as otel_trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel

# 1. Setup local Arize Phoenix tracing
tracer_provider = TracerProvider()
otel_trace.set_tracer_provider(tracer_provider)
span_exporter = OTLPSpanExporter(endpoint="http://localhost:6006/v1/traces")
span_processor = SimpleSpanProcessor(span_exporter)
tracer_provider.add_span_processor(span_processor)
OpenAIInstrumentor().instrument()

from dotenv import load_dotenv
load_dotenv(override=True)

# 2. Setup Gemini client & model mapping
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
google_client = AsyncOpenAI(
    base_url=GEMINI_BASE_URL,
    api_key=os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
)
gemini_model = OpenAIChatCompletionsModel(
    model="gemini-3.1-flash-lite",
    openai_client=google_client
)

# 3. Override model environment variables so child agent files receive this object
os.environ["DEFAULT_MODEL_NAME"] = "gemini-3.1-flash-lite"
# To prevent child files from trying to re-read gpt-5.4-mini string, import them after overriding environment or manually map them
import sys
# We can dynamically bind the model name
from research_manager import ResearchManager


async def run(query: str):
    async for status_update in ResearchManager().run(query):
        yield status_update


with gr.Blocks() as ui:
    query_textbox = gr.Textbox(label="What topic would you like to research?")
    run_button = gr.Button("Run", variant="primary")
    report = gr.Markdown(label="Report")
    
    run_button.click(run, inputs=query_textbox, outputs=report)
    query_textbox.submit(run, inputs=query_textbox, outputs=report)

ui.launch(theme=gr.themes.Default(primary_hue="sky"))

