# Zeotap Project Repository

## Overview


This repository contains two assignments: a web application mimicking Google Sheets and a support agent chatbot for Customer Data Platforms (CDPs). These projects demonstrate proficiency in web development and natural language processing.

## Assignment 1: Web Application Mimicking Google Sheets
![Image](https://github.com/user-attachments/assets/ae21bfb0-d1b2-42f1-8c62-c4278a1ea4df)

### Features
- **Spreadsheet Interface**: Mimics Google Sheets UI with a toolbar, formula bar, and cell structure.
- **Drag Functions**: Implemented drag functionality for cell content and formulas.
- **Cell Dependencies**: Formulas update automatically based on cell changes.
- **Mathematical Functions**: Includes SUM, AVERAGE, MAX, MIN, and COUNT.
- **Data Quality Functions**: Implements TRIM, UPPER, LOWER, REMOVE_DUPLICATES, and FIND_AND_REPLACE.

### Tech Stack
- **Frontend**: React, Vite

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/devespanchariya/zeotap.git
   cd zeotap

# Support Agent Chatbot for CDP "How-to" Questions

## Overview
This chatbot is designed to answer "how-to" questions related to four Customer Data Platforms (CDPs): Segment, mParticle, Lytics, and Zeotap. It extracts relevant information from the official documentation of these CDPs to guide users in performing tasks or achieving specific outcomes.

![Image](https://github.com/user-attachments/assets/bf486eb9-9e93-4c44-8d53-40274d12fbe9)

![Image](https://github.com/user-attachments/assets/e3007db1-cac2-4060-8b68-50b69c0b1df9)

![Image](https://github.com/user-attachments/assets/e9ad2d61-2546-4ee2-9408-69cdea24cbbc)



## Features
- **Answer "How-to" Questions**: Provides responses based on official documentation.
- **Documentation Extraction**: Retrieves and processes relevant sections dynamically.
- **Handles Variations in Queries**: Understands different phrasings and prevents irrelevant queries.
- **Cross-CDP Comparisons (Bonus)**: Compares functionalities across multiple CDPs.
- **Advanced Queries (Bonus)**: Handles complex configurations and integrations.

## Tech Stack
- **CODE**: Python
- **NLP Model**: OpenAI API for natural language processing
- **Data Source**: Web scraping from official CDP documentation

## Installation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/devespanchariya/zeotap
   cd zeotap/chatbot
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the chatbot:
   ```bash
   python app.py
   ```
