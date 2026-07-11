from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime


# ==========================================
# REQUEST SCHEMAS
# ==========================================

class ContentRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=500, description="Título do conteúdo")
    text: str = Field(..., min_length=10, max_length=10000, description="Texto/descrição")
    
    @validator("title", "text")
    def not_empty(cls, v):
        if not v.strip():
            raise ValueError("Campo não pode ser vazio")
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Introduction to Spring Boot",
                "text": "In this content we present the basic concepts for creating REST APIs using Java and Spring Boot."
            }
        }


class BatchContentRequest(BaseModel):
    items: List[ContentRequest] = Field(..., min_length=1, max_length=100)


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=500)
    top_n: int = Field(5, ge=1, le=20)


# ==========================================
# RESPONSE SCHEMAS
# ==========================================

class CategoryScore(BaseModel):
    name: str
    score: float


class RelatedContent(BaseModel):
    title: str
    category: str
    similarity: float
    url: Optional[str] = None


class ContentResponse(BaseModel):
    category: str
    probability: float
    top_categories: List[CategoryScore]
    keywords: List[str]
    related_content: List[RelatedContent]
    processed_at: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "category": "Backend",
                "probability": 0.91,
                "top_categories": [
                    {"name": "Backend", "score": 0.91},
                    {"name": "DevOps", "score": 0.05}
                ],
                "keywords": ["Spring Boot", "Java", "REST API"],
                "related_content": [
                    {
                        "title": "Building REST APIs with Spring",
                        "category": "Backend",
                        "similarity": 0.87,
                        "url": "https://dev.to/..."
                    }
                ],
                "processed_at": "2025-01-15T10:30:00"
            }
        }


class HealthResponse(BaseModel):
    status: str
    app: str
    version: str
    model_loaded: bool


class StatsResponse(BaseModel):
    total_content: int
    n_categories: int
    categories: List[str]
    model_version: str
    accuracy: float
    f1_score: float
    trained_at: str


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None