from flask import Flask, request, jsonify, render_template
import joblib
import re
import random

app = Flask(__name__)

# Cargar modelo autónomo
model = joblib.load('modelo_autonomo.pkl')
vectorizer = joblib.load('vectorizer_autonomo.pkl')

# Consejos de seguridad dinámicos
consejos = [
    "Los dominios con más de 3 niveles suelen ser sospechosos",
    "Verifica que el TLD (.com, .org) coincida con el sitio real",
    "Las URLs con más de 50 caracteres tienen mayor riesgo",
    "Los sitios legítimos rara vez usan caracteres Unicode",
    "El 92% de los ataques de phishing evitan el uso de HTTPS"
]

def preprocess_url(url):
    """Preprocesamiento idéntico al usado en entrenamiento"""
    url = str(url).lower().strip()
    url = re.sub(r'^https?://', '', url)
    url = re.sub(r'www\.', '', url)
    return re.sub(r'[^\w.-]', ' ', url)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predecir', methods=['POST'])
def predecir():
    data = request.get_json()
    url = data.get('url', '').strip()

    if not url:
        return jsonify({'error': 'URL requerida'}), 400

    try:
        # Preprocesamiento consistente
        url_procesada = preprocess_url(url)
        
        # Vectorización
        X = vectorizer.transform([url_procesada])
        
        # Predicción probabilística
        prob_segura = model.predict_proba(X)[0][1] * 100
        
        # Clasificación con umbrales optimizados
        if prob_segura < 30:
            respuesta = {
                "resultado": "❌ URL peligrosa",
                "probabilidad": prob_segura,
                "icono": "red",
                "razon": f"Alto riesgo ({prob_segura:.1f}% de seguridad)"
            }
        elif prob_segura < 65:
            respuesta = {
                "resultado": "⚠️ URL sospechosa", 
                "probabilidad": prob_segura,
                "icono": "orange",
                "razon": f"Riesgo moderado ({prob_segura:.1f}% de seguridad)"
            }
        elif prob_segura < 90:
            respuesta = {
                "resultado": "🟢 URL aceptable",
                "probabilidad": prob_segura,
                "icono": "blue",
                "razon": f"Bajo riesgo ({prob_segura:.1f}% de seguridad)"
            }
        else:
            respuesta = {
                "resultado": "✅🔒 URL segura",
                "probabilidad": prob_segura,
                "icono": "green",
                "razon": f"Segura ({prob_segura:.1f}% de seguridad)"
            }
            
        return jsonify(respuesta)

    except Exception as e:
        return jsonify({
            "error": "Error en el análisis",
            "detalle": str(e),
            "probabilidad": 0
        }), 500

@app.route('/consejo')
def consejo():
    return jsonify({"consejo": random.choice(consejos)})

if __name__ == '__main__':
    app.run(debug=True)