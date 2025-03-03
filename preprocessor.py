import os
import json
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk

# Ensure you have the NLTK stopwords downloaded
nltk.download('stopwords')

# Initialize the stemmer and stop words
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

def load_json_files(directory):
    """Load all JSON files from the specified directory."""
    data = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
                file_data = json.load(f)
                data.extend(file_data)  # Assuming each file contains a list of entries
    return data

def generate_qa_pairs(scraped_data):
    """Generate question-answer pairs from the scraped data."""
    qa_pairs = []

    for entry in scraped_data:
        if isinstance(entry, dict):  # Ensure entry is a dictionary
            title = entry.get('title', 'No Title')
            content = entry.get('content', '')
            
            # Generate questions based on the content
            if "Vault" in content:
                qa_pairs.append({
                    "question": "What is Vault in Lytics?",
                    "answer": "Vault is a feature in Lytics that helps manage and secure user identities."
                })
            
            if "Identity Resolution" in content:
                qa_pairs.append({
                    "question": "What is Identity Resolution in Lytics?",
                    "answer": "Identity Resolution is a key concept in Lytics that helps unify customer identities across different data sources."
                })
            
            if "Cloud Connect" in content:
                qa_pairs.append({
                    "question": "What is Cloud Connect in Lytics?",
                    "answer": "Cloud Connect allows you to connect your data warehouses to Lytics for better data management."
                })
            
            if "mParticle" in title:
                qa_pairs.append({
                    "question": "What is mParticle?",
                    "answer": "mParticle is a customer data platform (CDP) that simplifies how you collect and connect your user data to hundreds of vendors."
                })
            
            if "data quality" in content:
                qa_pairs.append({
                    "question": "How does mParticle ensure data quality?",
                    "answer": "mParticle ensures data quality by providing validation and monitoring features."
                })
            
            if "Segment" in title:
                qa_pairs.append({
                    "question": "What is Segment?",
                    "answer": "Segment is a customer data platform that helps you collect, manage, and integrate your customer data with hundreds of tools."
                })
            
            if "Zeotap" in title:
                qa_pairs.append({
                    "question": "What is Zeotap CDP?",
                    "answer": "Zeotap CDP is a customer data platform that helps businesses collect, unify, and activate customer data across multiple platforms."
                })
            
            # Additional questions based on keywords in the content
            if "audiences" in content:
                qa_pairs.append({
                    "question": "How do I activate audiences in Lytics?",
                    "answer": "You can activate audiences by leveraging user profiles and using the Audiences feature."
                })
            
            if "integration" in content:
                qa_pairs.append({
                    "question": "How do I integrate data sources in Zeotap?",
                    "answer": "You can integrate data sources in Zeotap using the Integration Options available in the platform."
                })
            
            if "personalization" in content:
                qa_pairs.append({
                    "question": "How do I personalize experiences using Segment?",
                    "answer": "You can build audiences and journeys from real-time customer data to personalize experiences on every channel."
                })
            
            
            
            if "data pipeline" in content:
                qa_pairs.append({
                    "question": "What is the Data Pipeline in Lytics?",
                    "answer": "The Data Pipeline in Lytics is used for managing and processing customer data efficiently."
                })
            
            if "user profiles" in content:
                qa_pairs.append({
                    "question": "How do I manage user profiles in Lytics?",
                    "answer": "User  profiles can be managed through the User Profiles section, where you can view and edit user data."
                })
            
            if "metrics" in content:
                qa_pairs.append({
                    "question": "How do I monitor metrics in Lytics?",
                    "answer": "You can monitor metrics and alerts through the Monitoring section in Lytics."
                })
            
            if "SDKs" in content:
                qa_pairs.append({
                    "question": "What SDKs are available for Lytics?",
                    "answer": "Lytics provides SDKs for Web, Mobile, and Chrome Extension integrations."
                })
            
            # mParticle Questions
            if "mParticle" in title:
                qa_pairs.append({
                    "question": "What is mParticle?",
                    "answer": "mParticle is a customer data platform (CDP) that simplifies how you collect and connect your user data to hundreds of vendors."
                })
            
            if "data quality" in content:
                qa_pairs.append({
                    "question": "How does mParticle ensure data quality?",
                    "answer": "mParticle ensures data quality by providing validation and monitoring features."
                })
            
            if "identity" in content:
                qa_pairs.append({
                    "question": "What is IDSync in mParticle?",
                    "answer": "IDSync is a feature that helps manage user identities across different platforms."
                })
            
            if "events" in content:
                qa_pairs.append({
                    "question": "What is the Events API in mParticle?",
                    "answer": "The Events API allows you to send events directly to mParticle for processing."
                })
            
            if "privacy" in content:
                qa_pairs.append({
                    "question": "How does mParticle ensure user privacy?",
                    "answer": "mParticle ensures compliance with GDPR, CCPA, and your privacy policies through its User Privacy features."
                })
            
            # Segment Questions
            if "Segment" in title:
                qa_pairs.append({
                    "question": "What is Segment?",
                    "answer": "Segment is a customer data platform that helps you collect, manage, and integrate your customer data with hundreds of tools."
                })
            
            if "data collection" in content:
                qa_pairs.append({
                    "question": "How can Segment help with data collection?",
                    "answer": "Segment simplifies data collection and integrates the tools you need for analytics, growth, and marketing."
                })
            
            if "data integrity" in content:
                qa_pairs.append({
                    "question": "How do I protect data integrity in Segment?",
                    "answer": "Segment prevents data quality issues with a tracking schema and enforcement with Protocols."
                })
            
            if "personalization" in content:
                qa_pairs.append({
                    "question": "How do I personalize experiences using Segment?",
                    "answer": "You can build audiences and journeys from real-time customer data to personalize experiences on every channel."
                })
            
            if "Segment Spec" in content:
                qa_pairs.append({
                    "question": "What is the Segment Spec?",
                    "answer": "The Segment Spec helps you identify, capture, and format meaningful data for use with Segment libraries and APIs."
                })
            
            # Zeotap Questions
            if "Zeotap" in title:
                qa_pairs.append({
                    "question": "What is Zeotap CDP?",
                    "answer": "Zeotap CDP is a customer data platform that helps businesses collect, unify, and activate customer data across multiple platforms."
                })
            
            if "unify" in content:
                qa_pairs.append({
                    "question": "How do I unify customer data in Zeotap?",
                    "answer": "You can unify customer data using the Catalogue, Calculated Attributes, and ID Strategy features."
                })
            
            if "audiences" in content:
                qa_pairs.append({
                    "question": "How do I create audiences in Zeotap?",
                    "answer": "You can create audiences in Zeotap to segment and activate your customer data."
                })
            
            if "dashboard" in content:
                qa_pairs.append({
                    "question": "What is the Dashboard in Zeotap?",
                    "answer": "The Dashboard in Zeotap allows you to analyze your platform usage and explore consumption metrics."
                })
            
            if "compliance" in content:
                qa_pairs.append({
                    "question": "How does Zeotap ensure compliance with GDPR?",
                    "answer": "Zeotap ensures compliance with GDPR by implementing features like Consent management and Data Lifecycle controls."
                })
            
            if "target" in content:
                qa_pairs.append({
                    "question": "What is the Target feature in Zeotap?",
                    "answer": "The Target feature in Zeotap allows you to create and activate deterministic third-party audiences."
                })
            
            if "admin" in content:
                qa_pairs.append({
                    "question": "What is the Admin module in Zeotap?",
                    "answer":                 "The Admin module in Zeotap allows you to create organizations and add users with specific roles and access."
            })
            
            if "customer 360" in content:
                qa_pairs.append({
                    "question": "What is the Customer 360 feature in Zeotap?",
                    "answer": "The Customer 360 feature in Zeotap provides a comprehensive view of customer interactions and data across platforms."
                })
            
            if "journeys" in content:
                qa_pairs.append({
                    "question": "How do I create custom journeys in Zeotap?",
                    "answer": "You can create custom journeys in Zeotap using the ID feature to provide optimal actions based on user behavior."
                })
            
            if "data lifecycle" in content:
                qa_pairs.append({
                    "question": "What is the Data Lifecycle feature in Zeotap?",
                    "answer": "The Data Lifecycle feature in Zeotap helps manage customer data in compliance with regulatory frameworks."
                })
            
            if "integration options" in content:
                qa_pairs.append({
                    "question": "What are the Integration Options in Zeotap?",
                    "answer": "The Integration Options in Zeotap allow you to connect various data sources and activate your data across platforms."
                })

    return qa_pairs
            
def preprocess_text(text):
    """Preprocess the text by lowering case, removing punctuation, and stemming."""
    # Lowercase
    text = text.lower()
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Tokenization
    tokens = text.split()
    # Remove stop words and stem
    tokens = [stemmer.stem(word) for word in tokens if word not in stop_words]
    return ' '.join(tokens)

# Load data from the specified directory
scraped_data = load_json_files(r'C:\Users\Ananya Tiwari\cdp-chatbot\cdp_data')  # Use raw string or forward slashes

# Generate QA pairs from the scraped data
qa_pairs = generate_qa_pairs(scraped_data)

# Create a DataFrame from the QA pairs
df_qa = pd.DataFrame(qa_pairs)

# Preprocess questions and answers
df_qa['processed_question'] = df_qa['question'].apply(preprocess_text)
df_qa['processed_answer'] = df_qa['answer'].apply(preprocess_text)

# Display the processed DataFrame
print(df_qa[['question', 'processed_question', 'answer', 'processed_answer']])

# Save the DataFrame to a CSV file
df_qa.to_csv('qa_pairs.csv', index=False)  # Save without the index column

print("QA pairs saved to qa_pairs.csv")