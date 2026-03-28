from pydantic import BaseModel
from typing import List
from typing import Optional


class ChatRequest(BaseModel):
    year: str
    major: str
    question: str
    history: Optional[str] = None


class ResourceItem(BaseModel):
    name: str
    type: str
    description: str
    url: str
    score: int
    why_matched: str


class SearchResponse(BaseModel):
    results: List[ResourceItem]


class ChatResponse(BaseModel):
    answer: str
    resources: List[ResourceItem]