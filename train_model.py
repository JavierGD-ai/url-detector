import time
import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

start = time.time()

# 1. Cargar datos balanceados
df_malicious = pd.read_csv("malicious_phish.csv").sample(n=5000, random_state=42)
df_safe = pd.read_csv("safety_url.csv").sample(n=5000, random_state=42)

# 2. Preprocesamiento mejorado
def preprocess_url(url):
    url = str(url).lower().strip()
    url = re.sub(r'^https?://', '', url)
    url = re.sub(r'www\.', '', url)
    url = re.sub(r'[^\w.-]', ' ', url)
    return url

df_malicious['url'] = df_malicious['url'].apply(preprocess_url)
df_safe['url'] = df_safe['url'].apply(preprocess_url)

# 3. Etiquetado
df_malicious['label'] = 0  # Maliciosa
df_safe['label'] = 1       # Segura
data = pd.concat([df_malicious, df_safe])

# 4. Vectorización con n-gramas
vectorizer = TfidfVectorizer(
    max_features=1500,
    ngram_range=(1, 3),
    analyzer='char',
    lowercase=False
)
X = vectorizer.fit_transform(data['url'])
y = data['label']

# 5. Modelo rápido con mejores hiperparámetros
model = LogisticRegression(
    C=0.5,
    solver='saga',
    max_iter=1000,
    class_weight='balanced',
    penalty='elasticnet',
    l1_ratio=0.5,
    n_jobs=-1
)

# 6. Entrenamiento rápido (20-30 segundos)
model.fit(X, y)

# 7. Guardar modelo
joblib.dump(model, 'modelo_autonomo.pkl')
joblib.dump(vectorizer, 'vectorizer_autonomo.pkl')

print(f"✅ Entrenado en {time.time()-start:.2f} segundos | Precisión: {model.score(X, y):.2%}")