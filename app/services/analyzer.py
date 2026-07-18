import numpy as np
from typing import Dict, List
import traceback

from app.model_loader import get_pipeline, load_model
from app.utils.text_processing import clean_text, detect_language

TECHNOLOGIES = {
    "Java": ["java", "jvm", "jdk"],
    "Spring Boot": ["spring boot", "springboot", "spring-boot", "spring mvc", "@restcontroller"],
    "Node.js": ["node", "nodejs", "node.js", "express", "expressjs", "npm"],
    "Python": ["python", "django", "flask", "fastapi", "uvicorn", "pandas"],
    "React": ["react", "reactjs", "react.js", "jsx", "hooks", "next.js", "nextjs"],
    "Angular": ["angular"],
    "Vue": ["vue", "vuejs", "vue.js"],
    "JavaScript": ["javascript", "js", "ecmascript"],
    "TypeScript": ["typescript", "ts"],
    "Flutter": ["flutter", "dart"],
    "React Native": ["react native", "reactnative"],
    "Kotlin": ["kotlin"],
    "Swift": ["swift", "swiftui"],
    "OCI": ["oci", "oracle cloud", "oracle cloud infrastructure", "object storage", "autonomous database"],
    "AWS": ["aws", "amazon web services", "s3", "ec2", "lambda"],
    "Docker": ["docker", "dockerfile", "container", "docker-compose"],
    "Kubernetes": ["kubernetes", "k8s", "kubectl", "helm"],
    "Terraform": ["terraform"],
    "Scikit-learn": ["scikit-learn", "sklearn", "scikit learn"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "Spark": ["spark", "pyspark", "apache spark"],
    "Airflow": ["airflow", "apache airflow"],
    "PostgreSQL": ["postgresql", "postgres"],
    "MySQL": ["mysql"],
    "MongoDB": ["mongodb", "mongo"],
    "Oracle Database": ["oracle database", "oracle db", "pl/sql"],
    "SQL": ["sql"],
    "Redis": ["redis"],
    "GitHub Actions": ["github actions", "ci/cd"],
}

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

def extract_keywords(clean: str, top_n: int = 6) -> List[str]:
    try:
        pipeline = get_pipeline()
        tfidf = pipeline.named_steps["tfidf"]
        response = tfidf.transform([clean])
        feature_names = np.array(tfidf.get_feature_names_out())
        scores = response.toarray()[0]
        top_indices = scores.argsort()[-top_n:][::-1]
        return [str(feature_names[i]) for i in top_indices if scores[i] > 0]
    except Exception:
        return []

def detect_technologies(text: str) -> List[str]:
    try:
        artifacts = load_model()
        tech_dict = artifacts.get("technologies_dict") or TECHNOLOGIES
    except Exception:
        tech_dict = TECHNOLOGIES

    text_lower = text.lower()
    found = []
    for tech, keywords in tech_dict.items():
        if any(kw in text_lower for kw in keywords):
            found.append(tech)
    return sorted(list(set(found)))

def estimate_difficulty(text: str, word_count: int) -> str:
    text_lower = text.lower()
    advanced_terms = ["advanced", "avançado", "deep dive", "architecture", "otimização", "performance", "distributed", "microservices"]
    beginner_terms = ["introduction", "introdução", "basics", "básico", "para iniciantes", "getting started", "fundamentals"]

    adv_score = sum(1 for t in advanced_terms if t in text_lower)
    beg_score = sum(1 for t in beginner_terms if t in text_lower)

    if beg_score > 0 and adv_score == 0: return "Iniciante"
    if adv_score >= 1 or word_count > 150: return "Avançado"
    return "Intermediário"

def analyze_content(title: str, text: str) -> Dict:
    pipeline = get_pipeline()
    full_text = f"{title}. {text}"
    clean = clean_text(full_text)

    if not clean or len(clean.split()) < 2:
        raise ValueError("Texto insuficiente após limpeza para análise.")

    # Predição da categoria
    category = pipeline.predict([clean])[0]
    
    # Cálculo ultra seguro de probabilidade (Garante imunidade a erros AttributeError)
    probability = 0.95
    try:
        clf = pipeline.named_steps["clf"]
        
        # Caso o pipeline como um todo tenha predict_proba
        if hasattr(pipeline, "predict_proba"):
            proba = pipeline.predict_proba([clean])[0]
            probability = round(float(max(proba)), 3)
            
        # Caso apenas o estimador interno o tenha (TF-IDF separado)
        elif hasattr(clf, "predict_proba"):
            tfidf = pipeline.named_steps["tfidf"]
            vec = tfidf.transform([clean])
            proba = clf.predict_proba(vec)[0]
            probability = round(float(max(proba)), 3)
            
        # Caso utilize decision_function (como SVM bruto)
        elif hasattr(pipeline, "decision_function"):
            scores = pipeline.decision_function([clean])[0]
            proba = softmax(scores)
            probability = round(float(max(proba)), 3)
            
        elif hasattr(clf, "decision_function"):
            tfidf = pipeline.named_steps["tfidf"]
            vec = tfidf.transform([clean])
            scores = clf.decision_function(vec)[0]
            proba = softmax(scores)
            probability = round(float(max(proba)), 3)
    except Exception as e:
        print("Fallback probabilidade ativado:", e)
        probability = 0.95

    word_count = len(full_text.split())
    keywords = extract_keywords(clean, top_n=6)
    technologies = detect_technologies(full_text)
    difficulty = estimate_difficulty(full_text, word_count)
    reading_time = max(1, round(word_count / 200))
    language = detect_language(full_text)

    return {
        "category": str(category),
        "probability": probability,
        "keywords": keywords,
        "technologies": technologies,
        "difficulty": difficulty,
        "reading_time_minutes": reading_time,
        "word_count": word_count,
        "language": language,
    }
