from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.config import get_settings
from app.routes import content, stats

settings = get_settings()

# Instância FastAPI
app = FastAPI(
    title="🏷️ TechTagger API",
    description="""
    API para organização inteligente de conteúdo técnico.
    
    ## Funcionalidades
    - 🏷️ **Classificação** automática de conteúdo por categoria
    - 🔑 **Extração de keywords** com YAKE
    - 🔗 **Recomendação** por similaridade semântica
    - 🔍 **Busca semântica** na base de conhecimento
    - 📦 **Processamento em lote** (CSV)
    
    ## Tecnologias
    - TF-IDF + Regressão Logística
    - Sentence Transformers (embeddings)
    - YAKE (keywords)
    - OCI Object Storage (modelos)
    """,
    version=settings.app_version,
    debug=settings.debug
)

# CORS (permitir frontend em qualquer origem)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Tratamento global de erros ---
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "detail": exc.errors()
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc)
        }
    )


# --- Rotas ---
app.include_router(stats.router)
app.include_router(content.router)


@app.get("/", tags=["Root"])
async def root():
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "redoc": "/redoc"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)