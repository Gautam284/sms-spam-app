from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pickle
import os
import re
import string
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from nltk.stem.porter import PorterStemmer

# Initialize Flask
app = Flask(__name__)
CORS(app)  # Allow frontend requests

# Load model + vectorizer
try:
    model = pickle.load(open("model.pkl", "rb"))
    vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
except:
    print(" Model files not found. Please make sure model.pkl and vectorizer.pkl are in the same directory.")

# Initialize stemmer
ps = PorterStemmer()

# Custom text preprocessing (no nltk.download needed)
def transform_text(text):
    text = text.lower()
    
    # Tokenize using regex (only words/numbers)
    tokens = re.findall(r"\b\w+\b", text)
    
    # Remove stopwords + punctuation
    tokens = [t for t in tokens if t not in ENGLISH_STOP_WORDS and t not in string.punctuation]
    
    # Apply stemming
    tokens = [ps.stem(t) for t in tokens]
    
    return " ".join(tokens)

# Home route → serves HTML frontend
@app.route("/")
def home():
    return render_template("index.html")

# Prediction route → handles AJAX/Fetch requests
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "No message provided"}), 400

        message = data["message"]

        # Preprocess → Vectorize → Predict
        transformed_msg = transform_text(message)
        X = vectorizer.transform([transformed_msg])
        prediction = model.predict(X)[0]

        # Convert labels
        label = "Not Spam" if prediction == 0 else "Spam"
        
        return jsonify({"prediction": label})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)


