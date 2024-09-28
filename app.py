from flask import Flask, render_template, request, redirect, flash
from main import llmworkflow
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key'

logging.basicConfig(level=logging.INFO)

chat_history = []

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        return handle_post_request()
    else:    
        return render_template("index.html", chat_history=chat_history)

def handle_post_request():
    value = request.form.get('query', '').strip()
    if not value:
        flash("Query cannot be empty. Please enter a valid input.", "warning")
        return redirect("/")

    try:
        llmoutput = llmworkflow(value)
        chat_history.append({'sender': 'user', 'message': value})
        chat_history.append({'sender': 'ai', 'message': llmoutput})
        return render_template("index.html", chat_history=chat_history)
    except Exception as e:
        logging.error(f"Error processing LLM workflow: {e}")
        flash("There was an error processing your request. Please try again.", "danger")
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
