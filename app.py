from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pickle
import nltk
from nltk.corpus import stopwords
import string
import os

# Initialize Flask
app = Flask(__name__)
CORS(app)  # Allow frontend requests

# Load model + vectorizer
try:
    model = pickle.load(open("model.pkl", "rb"))
    vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
except:
    print("Model files not found. Please make sure model.pkl and vectorizer.pkl are in the same directory.")

# NLTK requirements
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

nltk.download('punkt')
nltk.download('stopwords')

# Text preprocessing
def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

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

        # ✅ Changed label here
        label = "Not Spam" if prediction == 0 else "Spam"
        return jsonify({"prediction": label})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

