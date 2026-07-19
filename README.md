# SureHealth Pharmacy Assistant

AI-powered pharmacy assistant built with Streamlit, Groq, and local pharmacy data.

## Overview

SureHealth Pharmacy Assistant is a chat-based internal tool for pharmacy operations. It helps staff retrieve inventory details and internal policy information through a simple natural-language interface instead of manually searching spreadsheets or documents.

The application combines:

- A Streamlit chat interface
- A Groq-hosted language model
- Local pharmacy inventory data
- A local pharmacy policy document
- Tool-calling for grounded responses

## Data Note

The inventory data used in this project is randomly generated demo data. The generation logic is included in `data/data.py`, which creates the pharmacy inventory CSV used by the assistant.

## Features

- Inventory search by medication name, SKU, or related text
- Direct medication lookup by SKU
- Low-stock detection
- Expiry monitoring for medications nearing expiration
- Internal policy and procedure lookup
- Chat workflow designed for fast operational support

## How It Works

When a user sends a message, the assistant:

1. Receives the prompt in the Streamlit chat UI
2. Sends the conversation to the language model
3. Lets the model call local tools when structured data is needed
4. Queries inventory data from `documents/pharmacy_inventory_2000.csv`
5. Queries policy content from `documents/policy.txt`
6. Returns a final grounded response in the chat interface

This keeps responses tied to local project data instead of relying only on model memory.

## Tech Stack

- Python
- Streamlit
- Groq API
- pandas
- python-dotenv

## Project Structure

```text
app.py                  # Streamlit app entrypoint
config.py               # Central configuration
bootstrap/              # Service container and tool registration
services/               # LLM, agent, inventory, memory, and policy services
tools/                  # AI-callable local tools
schemas/                # Tool schemas for function calling
models/                 # Chat, state, and response models
ui/                     # Streamlit UI components
documents/              # Inventory and policy files
prompts/                # System prompt
```

## Run Locally

### 1. Create and activate a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

Main app:

```powershell
pip install -r requirements.txt
```

Optional retrieval experiment in `data/store_data.py`:

```powershell
pip install -r requirements-optional.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Start the app

```powershell
streamlit run app.py
```

## Example Prompts

- `Search for Amoxicillin`
- `Find medication with SKU00003`
- `Which items are low in stock?`
- `Show medications expiring in 30 days`
- `What is the return policy?`
- `What does the policy say about expired medicines?`

## Use Case

This project is built for pharmacy environments where staff need quick access to operational information such as:

- Medication availability
- Stock levels
- Warehouse or storage references
- Expiry awareness
- Internal policy guidance

## Why I Built It

The goal of this project is to combine conversational AI with pharmacy business data in a practical way. Instead of building a generic chatbot, the assistant is grounded in real project files so it can answer inventory and policy questions with useful operational context.

The current inventory dataset is synthetic and randomly generated for demo and testing purposes rather than sourced from a live pharmacy system.

## Future Improvements

- Add a `requirements.txt`
- Pin package versions
- Add automated tests
- Support richer inventory filters
- Improve policy retrieval with semantic search
- Add admin tools for document or inventory updates

## License

Add your preferred license here.
