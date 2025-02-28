# responder.py
import pandas as pd
from retriever import Retriever  # Ensure you have the correct import

# Load your QA pairs DataFrame
qa_pairs_df = pd.read_csv(r'C:\Users\Ananya Tiwari\cdp-chatbot\qa_pairs.csv')  # Ensure this path is correct

# Initialize the retriever
retriever = Retriever(qa_pairs_df)
