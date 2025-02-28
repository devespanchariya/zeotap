import json
import os
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load scraped data
def load_cdp_data():
    cdp_data = {}
    data_dir = Path("cdp_data")
    
    for file_path in data_dir.glob("*_howto.json"):
        with open(file_path, 'r', encoding='utf-8') as file:
            cdp_name = file_path.stem.replace('_howto', '')
            cdp_data[cdp_name] = json.load(file)
    
    return cdp_data

# Process and index documents
def create_document_index(cdp_data):
    documents = []
    document_sources = []
    
    for cdp_name, cdp_content in cdp_data.items():
        for guide in cdp_content:
            # Assuming guide structure has 'title', 'content', and 'url'
            doc_text = f"{guide['title']} {guide['content']}"
            documents.append(doc_text)
            document_sources.append({
                'cdp': cdp_name,
                'title': guide['title'],
                'url': guide['url']
            })
    
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    return vectorizer, tfidf_matrix, document_sources