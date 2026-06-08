from flask import Flask, render_template, request
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# LOAD JSON DATA
with open('data.json', 'r') as file:
    data = json.load(file)

questions = [item["question"] for item in data["questions"]]
answers = [item["answer"] for item in data["questions"]]

# TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')
question_vectors = vectorizer.fit_transform(questions)

# CHATBOT FUNCTION
def chatbot_response(user_input):

    if not user_input:
        return "Sorry, I don't understand your question. Please try again."

    user_input = user_input.strip()
    user_vector = vectorizer.transform([user_input])

    # Guard: if query has no known words, return fallback immediately
    if user_vector.nnz == 0:
        return "Sorry, I don't understand your question. Please try again."

    similarity = cosine_similarity(user_vector, question_vectors)

    best_match_index = similarity.argmax()

    best_score = similarity[0][best_match_index]

    if best_score > 0.3:
        return answers[best_match_index]

    else:
        return "Sorry, I don't understand your question. Please try again."

# HOME PAGE
@app.route("/")
def home():
    return render_template("home.html")

# CHAT PAGE
@app.route("/chat")
def chat():
    return render_template("index.html")

# BOT RESPONSE
@app.route("/get")
def get_bot_response():

    user_text = request.args.get('msg')

    return chatbot_response(user_text)

if __name__ == "__main__":
    app.run(debug=True)