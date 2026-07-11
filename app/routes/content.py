from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from app.schemas import (
    ContentRequest, ContentResponse, 
    BatchContentRequest, SearchRequest,
    RelatedContent, CategoryScore
)
from app.services.ml_service import MLService

router = APIRouter(prefix="/content", tags=["Content"])
ml = MLService()


@router.post("", response_model=ContentResponse, status_code=status.HTTP_200_OK)
async def processar_conteudo(request: ContentRequest):
    """
    🏷️ **Processa um conteúdo técnico e retorna:**
    - Categoria principal + probabilidade
    - Top 3 categorias
    - Keywords extraídas
    - 3 conteúdos relacionados
    """
    try:
        resultado = ml.processar_completo(request.title, request.text)
        
        return ContentResponse(
            category=resultado["category"],
            probability=resultado["probability"],
            top_categories=[CategoryScore(**c) for c in resultado["top_categories"]],
            keywords=resultado["keywords"],
            related_content=[RelatedContent(**r) for r in resultado["related_content"]],
            processed_at=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar conteúdo: {str(e)}"
        )


@router.post("/batch")
async def processar_lote(request: BatchContentRequest):
    """
    📦 **Processa múltiplos conteúdos de uma vez (máx 100).**
    """
    try:
        resultados = []
        for item in request.items:
            r = ml.processar_completo(item.title, item.text)
            resultados.append({
                "title": item.title,
                **r
            })
        return {"total": len(resultados), "results": resultados}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/search")
async def buscar_conteudo(request: SearchRequest):
    """
    🔍 **Busca semântica** por conteúdos similares à query.
    """
    try:
        resultados = ml.buscar(request.query, top_n=request.top_n)
        return {
            "query": request.query,
            "total": len(resultados),
            "results": resultados
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/categories")
async def listar_categorias():
    """📚 **Lista todas as categorias disponíveis.**"""
    stats = ml.get_stats()
    return {
        "total": stats["n_categories"],
        "categories": stats["categories"]
    }