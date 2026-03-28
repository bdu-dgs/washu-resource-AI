from fastapi import FastAPI
from app.schemas import ChatRequest, SearchResponse, ChatResponse
from app.crud import search_all_resources
from app.db import get_connection
from app.ai import generate_chat_response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/debug-openapi")
def debug_openapi():
    return {
        "app_type": str(type(app)),
        "openapi_url": app.openapi_url,
        "docs_url": app.docs_url,
        "redoc_url": app.redoc_url,
    }

@app.get("/test")
def test():
    return {"ok": True}

@app.get("/")
def root():
    return {"message": "Backend is running"}


@app.get("/test-db")
def test_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1;")
    result = cur.fetchone()
    cur.close()
    conn.close()
    return {"result": result}


@app.post("/search")
def search(request: ChatRequest):
    results = search_all_resources(request.question)
    return {"results": results}


@app.post("/chat")
def chat(request: ChatRequest):
    resources = search_all_resources(request.question)
    answer = generate_chat_response(
        year=request.year,
        major=request.major,
        question=request.question,
        resources=resources
    )

    cleaned_resources = []
    for r in resources:
        cleaned_resources.append({
            "name": r["name"],
            "type": r["type"],
            "description": r["description"],
            "url": r["url"],
            "why_matched": r["why_matched"]
        })

    return {
        "answer": answer,
        "resources": cleaned_resources
    }