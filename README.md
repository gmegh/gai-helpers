# DocuChat - Document-Based Chatbot with Weaviate and OpenAI

DocuChat is a powerful document-based chatbot that leverages the capabilities of Weaviate for document indexing and OpenAI's GPT-3.5 Turbo for natural language understanding. This repository contains the source code and necessary files to set up your own DocuChat chatbot. With DocuChat, you can interact with a chatbot that can answer questions, provide information, and generate responses based on a vast repository of documents.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Setting Up Weaviate](#setting-up-weaviate)
  - [Configuring Environment Variables](#configuring-environment-variables)
  - [Running the Application](#running-the-application)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Overview

DocuChat is a document-based chatbot designed for various applications such as information retrieval, customer support, and more. It utilizes Weaviate, an open-source vector search engine, to index and search through documents, making it easy to provide accurate responses to user queries. OpenAI's GPT-3.5 Turbo, a state-of-the-art language model, powers the chatbot's conversational abilities.

## Features

- **Document Indexing**: Weaviate is used to index and search through a wide range of documents, including PDFs, text files, CSVs, DOCX, PPTX, and XLSX files.

- **Natural Language Understanding**: OpenAI's GPT-3.5 Turbo understands and generates natural language responses to user queries.

- **Interactive Chat Interface**: The chat interface allows users to engage in real-time conversations with the chatbot.

- **Document Retrieval**: DocuChat can retrieve specific information from documents and present it to the user in a conversational manner.

- **Easy Configuration**: The environment variables make it easy to set up and configure DocuChat for your specific use case.

## Prerequisites

Before you get started with DocuChat, make sure you have the following prerequisites installed on your system:

- [Python](https://www.python.org/downloads/)
- [Weaviate](https://weaviate.io/developers/weaviate) - Make sure to set up Weaviate and obtain an API key.
- [OpenAI API Key](https://platform.openai.com/account/api-keys) - You'll need an API key from OpenAI to use GPT-3.5 Turbo.

## Getting Started

Follow these steps to set up and run DocuChat on your system:

### Setting Up Weaviate

1. Install and set up Weaviate as per the [official documentation](https://www.semi.technology/developers/weaviate/current/getting-started.html).

2. Create an index in Weaviate, and note the index name. You will configure this index in your environment variables.

### Configuring Environment Variables

1. Create a `.env` file in the root directory of the repository.

2. Populate the `.env` file with the following environment variables:

   ```env
   WEAVIATE_URL=<Your Weaviate URL>
   WEAVIATE_API_KEY=<Your Weaviate API Key>
   OPENAI_API_KEY=<Your OpenAI API Key>
   ```

   Replace `<Your Weaviate URL>`, `<Your Weaviate API Key>`, and `<Your OpenAI API Key>` with your respective Weaviate URL and API key, and your OpenAI API key.

### Running the Application

1. Install the required Python packages by running:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the main application by executing:

   ```bash
   streamlit run app.py
   ```

   This will start the DocuChat Streamlit application on http://localhost:8501 and display a chat interface in your browser.

## Usage

DocuChat is designed to provide interactive conversations with the chatbot. Users can type their questions or queries, and the chatbot will generate responses based on the indexed documents in Weaviate. You can customize the behavior and responses of the chatbot by modifying the code in `app.py`.

## Contributing

We welcome contributions to enhance and improve DocuChat. If you'd like to contribute, please follow our [Contribution Guidelines](CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Thank you for using DocuChat! If you have any questions or feedback, please don't hesitate to reach out to us.