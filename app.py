from flask import Flask, request, jsonify, render_template
import random

app = Flask(__name__, static_folder='static', template_folder='templates')

# --- Word Pool ---
WORDS = [
    "money", "swing", "ghost", "build", "honey", "place",
    "lymph", "pluck", "crimp", "wreck", "jumbo"
]

# --- Helpers ---
def has_duplicate_letters(word):
    return len(set(word)) != len(word)

def check_positions(secret, guess):
    return sum(1 for s, g in zip(secret, guess) if s == g)

def check_characters(secret, guess):
    return sum(min(secret.count(c), guess.count(c)) for c in set(guess))

# --- Routes ---
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/check', methods=['POST'])
def check_word():
    data = request.json
    secret = data.get("secret")
    guess = data.get("guess")

    if len(guess) != 5:
        return jsonify({"error": "Word must be exactly 5 letters."}), 400
    if has_duplicate_letters(guess):
        return jsonify({"error": "All letters must be unique."}), 400

    guess = guess.lower()
    pos_correct = check_positions(secret, guess)
    char_correct = check_characters(secret, guess) - pos_correct

    result = {
        "correct": guess == secret,
        "position_match": pos_correct,
        "character_match": char_correct
    }
    return jsonify(result)

@app.route('/random-word', methods=['GET'])
def get_random_word():
    return jsonify({"word": random.choice(WORDS)})

# --- No __main__ block needed for deployment ---
