# 🏷️ TechTagger API

> Organização inteligente de conteúdo técnico com Machine Learning

API REST desenvolvida durante o **Hackathon ONE – Alura + Oracle** que utiliza técnicas de Ciência de Dados para classificar, extrair keywords e recomendar conteúdo técnico automaticamente.

---

## 🎯 Sobre o Projeto

Profissionais e estudantes de tecnologia consomem diariamente uma grande quantidade de conteúdo técnico, o que dificulta a organização e reutilização dessas informações.

O **TechTagger** resolve isso recebendo textos técnicos (artigos, documentação, tutoriais) e retornando:
- 🏷️ Categoria classificada (Backend, Frontend, DataScience, etc.)
- 🔑 Palavras-chave extraídas automaticamente
- 🔗 Conteúdos relacionados por similaridade semântica

Tudo em formato JSON, pronto para consumo por outras aplicações.

---

## 🛠️ Tecnologias

- **Python 3.10+**
- **FastAPI** – API REST de alta performance
- **scikit-learn** – TF-IDF + Regressão Logística
- **sentence-transformers** – Embeddings semânticos
- **YAKE** – Extração de keywords
- **OCI Object Storage** – Armazenamento dos modelos na nuvem Oracle

---

## 📁 Estrutura do Projeto
TechTagger-API/
├── app/
│ ├── main.py # Ponto de entrada da API
│ ├── config.py # Configurações
│ ├── schemas.py # Modelos Pydantic
│ ├── services/
│ │ ├── ml_service.py # Lógica de Machine Learning
│ │ └── storage_service.py
│ ├── rotas/
│ │ ├── content.py # Endpoints de conteúdo
│ │ └── stats.py # Métricas do sistema
│ └── utilitários/
│ └── text_utils.py # Pré-processamento de texto
├── models/ # Modelos treinados
│ ├── classifier.pkl
│ ├── embeddings.npy
│ ├── metadata.csv
│ └── model_info.json
├── requisitos.txt
└── README.md


## 🚀 Como Executar

### Pré-requisitos
- Python 3.10+
- pip

### 1. Clone o repositório

git clone https://github.com/Ryos75/TechTagger-API.git
cd TechTagger-API
### Pré-requisitos
- Python 3.10+
- pip


### 2. Crie e ative o ambiente virtual
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate

3. Instale as responsabilidades
pip install -r requirements.txt

4. Executar uma API
uvicorn app.main:app --reload

5. Acesse a documentação
Interface do Swagger: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

📡 Pontos finais
Método	  Ponto final	          Descrição
PEGAR  	  /health	            Exame de saúde
PEGAR	     /stats	               Estatísticas do modelo
PUBLICAR	  /content	            Processa conteúdo técnico
PUBLICAR	  /content/batch	      Processamento em lote
PUBLICAR	  /content/search	      Busca seminal
PEGAR	     /content/categories	Lista categorias

🧪 Exemplos de Uso
POST /content– Classificar conteúdo
Reserva:

Bash

curl -X POST http://localhost:8000/content \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Introduction to Spring Boot",
    "text": "In this content we present the basic concepts for creating REST APIs using Java and Spring Boot."
  }'
Resposta:

JSON

{
  "category": "Backend",
  "probability": 0.89,
  "top_categories": [
    {"name": "Backend", "score": 0.89},
    {"name": "DevOps", "score": 0.05},
    {"name": "Cloud", "score": 0.02}
  ],
  "keywords": ["Spring Boot", "REST APIs", "Java"],
  "related_content": [
    {
      "title": "Building REST APIs with Spring Security",
      "category": "Backend",
      "similarity": 0.87
    }
  ],
  "processed_at": "2025-01-15T10:30:00"
}
POST /content/search– Busca semântica
Reserva:

Bash

curl -X POST http://localhost:8000/content/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "how to authenticate users with tokens",
    "top_n": 3
  }'
Resposta:

JSON

{
  "query": "how to authenticate users with tokens",
  "total": 3,
  "results": [
    {
      "title": "JWT Authentication in Node.js",
      "category": "Backend",
      "similarity": 0.89
    }
  ]
}



☁️ Integração OCI
A solução está preparada para integração com Oracle Cloud Infrastructure (OCI) :

OCI Object Storage: armazenamento dos modelos ( classifier.pkl, embeddings.npy)
OCI Compute: hospedagem da aplicação (via Docker)
Para ativar o carregamento dos modelos via OCI, configure as variáveis ​​de ambiente no arquivo .env:

## 🧠 Modelo de Machine Learning

- **Algoritmo:** TF‑IDF (n‑grams 1–3) + Regressão Logística, otimizado por **GridSearchCV**
- **Melhores hiperparâmetros:** `C=2.0`, `max_features=5000`, `ngram_range=(1,3)`
- **Embeddings (recomendação):** sentence‑transformers `all-MiniLM-L6-v2`
- **Keywords:** YAKE com fallback automático por TF‑IDF
- **Dataset:** 1.520 artigos técnicos balanceados (Dev.to API), 8 categorias
- **Protocolo de avaliação:** treino com tags como sinal auxiliar; **teste apenas com título + descrição** (sem vazamento)

### 📊 Métricas (teste honesto)
| Métrica | Valor |
|---|---|
| **Accuracy** | **0.955** |
| **F1 (weighted)** | 0.955 |
| **F1 (macro)** | 0.955 |
| **F1 (CV 5‑fold)** | 0.960 |

### 🏷️ Categorias (F1 por classe)
Mobile 0.99 · Cloud 0.99 · Data Science 0.97 · Frontend 0.96 · Backend 0.95 · Databases 0.94 · DevOps 0.93 · Data Engineering 0.91

