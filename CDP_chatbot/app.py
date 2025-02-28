from flask import Flask, render_template, request, jsonify
import pandas as pd
from retriever import Retriever  # Ensure this imports your Retriever class

app = Flask(__name__)

# Load your QA pairs DataFrame
qa_pairs_df = pd.read_csv(r'C:\Users\Ananya Tiwari\cdp-chatbot\qa_pairs.csv')  # Ensure this path is correct
retriever = Retriever(qa_pairs_df)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.form['query']
    response = retriever.retrieve(user_query)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Changed to port 5001