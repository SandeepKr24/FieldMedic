from src.agents.rag import ingest_case
from src.infra.init_db import initialize_database
from src.agents.orchestrator import triage_patient
from src.utils import extract_text_from_pdf

from src.agents.rag import (
    ingest_case,
    ingest_knowledge_document,
)

from src.models import (
    KnowledgeIngestRequest,
    TriageRequest,
    TriageResult,
)

from fastapi import (
    FastAPI,
    HTTPException,
    UploadFile,
    File,
)

app = FastAPI(
    title="FieldMedic API",
    version="1.0.0"
)

initialize_database()


@app.get("/")
def root():
    return {
        "message": "Welcome to FieldMedic!"
    }


@app.get("/status")
def status():
    return {
        "status": "ok"
    }


@app.post("/cases")
def ingest(request: TriageRequest):
    return ingest_case(
        request.symptoms,
        request.vitals
    )

@app.post("/knowledge")
def ingest_knowledge(
    request: KnowledgeIngestRequest,
):
    return ingest_knowledge_document(
        source=request.source,
        title=request.title,
        text=request.text,
    )

@app.post(
    "/triage",
    response_model=TriageResult,
)
def triage(request: TriageRequest):
    try:
        return triage_patient(
            symptoms=request.symptoms,
            vitals=request.vitals,
            additional_info=request.additional_info,
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=503,
            detail=str(e),
        )

    except ValueError as e:
        raise HTTPException(
            status_code=502,
            detail=str(e),
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected internal server error occurred.",
        )
    
@app.post("/knowledge/pdf")
async def ingest_pdf(
    file: UploadFile = File(...),
):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    pdf_bytes = await file.read()

    text = extract_text_from_pdf(pdf_bytes)

    return ingest_knowledge_document(
        source=file.filename,
        title=file.filename,
        text=text,
    )