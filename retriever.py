import pandas as pd
from sentence_transformers import SentenceTransformer, util
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Ensure you have the necessary NLTK resources
nltk.download('stopwords')
nltk.download('wordnet')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = text.split()
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return ' '.join(tokens)

class Retriever:
    def __init__(self, qa_data):
        self.qa_data = qa_data
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Load a pre-trained model
        self.question_embeddings = self.model.encode(self.qa_data['processed_question'].tolist(), convert_to_tensor=True)

    def retrieve(self, user_query):
        print("Retrieve method called")
        user_query_processed = preprocess_text(user_query)
    
        # Encode the user query
        user_query_embedding = self.model.encode(user_query_processed, convert_to_tensor=True)
    
        # Compute cosine similarity
        similarities = util.pytorch_cos_sim(user_query_embedding, self.question_embeddings)
    
        # Check if similarities is empty or has invalid values
        if similarities.numel() == 0:
            return "I'm sorry, I couldn't find an answer to your question."
    
        # Get the index of the most similar question
        most_similar_index = similarities.argmax().item()  # Ensure this is an integer
    
        # Check if the index is valid
        if most_similar_index < 0 or most_similar_index >= len(self.qa_data):
            return "I'm sorry, I couldn't find an answer to your question."
    
        return self.qa_data.iloc[most_similar_index]['answer']

# Load your QA pairs DataFrame
qa_pairs_df = pd.read_csv(r'C:\Users\Ananya Tiwari\cdp-chatbot\qa_pairs.csv')  # Ensure this path is correct

# Initialize the retriever
retriever = Retriever(qa_pairs_df)
