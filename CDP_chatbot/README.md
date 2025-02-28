# CDP Support Agent Chatbot

## Overview

The CDP Support Agent Chatbot is a web-based application designed to assist users with "how-to" questions related to four Customer Data Platforms (CDPs): Segment, mParticle, Lytics, and Zeotap. The chatbot extracts relevant information from the official documentation of these platforms to guide users on how to perform tasks or achieve specific outcomes.

## Features

- **Answer "How-to" Questions**: The chatbot can respond to user inquiries about specific tasks or features within each CDP.
- **Extract Information from Documentation**: It retrieves relevant information from the official documentation to provide accurate answers.
- **Handle Variations in Questions**: The chatbot can manage different phrasing and terminology in user questions.
- **Cross-CDP Comparisons**: It can answer questions about the differences in approaches or functionalities between the four CDPs.
- **Advanced "How-to" Questions**: The chatbot can handle complex or platform-specific questions and provide guidance on advanced configurations and integrations.

## Data Sources

- **Segment Documentation**: [Segment Docs](https://segment.com/docs/?ref=nav)
- **mParticle Documentation**: [mParticle Docs](https://docs.mparticle.com/)
- **Lytics Documentation**: [Lytics Docs](https://docs.lytics.com/)
- **Zeotap Documentation**: [Zeotap Docs](https://docs.zeotap.com/home/en-us/)

## Requirements

To run this project, you need to have Python 3.x installed. The following Python packages are required:

- Flask
- requests
- beautifulsoup4
- selenium
- pandas
- nltk
- redis

You can install the required packages using the following command:

Steps to Run the Project
Ensure Python is Installed: Make sure you have Python 3.x installed on your machine. You can download it from python.org.

Navigate to the Project Directory: Change into the project directory where the requirements.txt file is located.

Install Dependencies: Run the command to install all required Python packages listed in requirements.txt.

Run the Scraper: Execute the scraper script to collect data from the CDP documentation. This will create JSON files containing the scraped data.

Start the Flask Application: Run the Flask application to start the web server.

Open the Chatbot Interface: Use your web browser to navigate to the specified URL to interact with the chatbot.

Contributing
Contributions are welcome! If you have suggestions for improvements or new features, please feel free to submit a pull request or open an issue.

```bash
pip install -r requirements.txt