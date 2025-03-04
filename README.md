# JioPay Support Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that provides automated customer support for JioPay using publicly available information.

## Features

- Vector-based semantic search for accurate information retrieval
- Real-time chat interface with modern UI
- Source attribution for responses
- Support for both FAQ and website content
- Efficient chunking and context retrieval
- Chat history support

## Project Structure

```
app/
├── backend/
│   ├── data/
│   │   ├── FAQs.json
│   │   └── pages.json
│   ├── utils/
│   │   ├── embeddings.py
│   │   └── chat.py
│   ├── main.py
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── ChatInterface.js
    │   │   └── ChatMessage.js
    │   ├── App.js
    │   └── theme.js
    └── package.json
```

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- OpenAI API key

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd jiopay-support-chatbot
```

2. Set up the backend:
```bash
cd app/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Create a .env file in the backend directory:
```
OPENAI_API_KEY=your_api_key_here
```

4. Set up the frontend:
```bash
cd ../frontend
npm install
```

## Running the Application

1. Start the backend server:
```bash
cd app/backend
python main.py
```
The backend server will start at http://localhost:8000

2. Start the frontend development server:
```bash
cd app/frontend
npm start
```
The frontend will be available at http://localhost:3000

## Usage

1. Open your browser and navigate to http://localhost:3000
2. Type your question in the chat input
3. The chatbot will respond with relevant information from the JioPay knowledge base
4. Sources for the information will be displayed below each response

## Technical Details

### Vector Embeddings
- Uses sentence-transformers for generating embeddings
- Model: all-MiniLM-L6-v2
- ChromaDB for vector storage and retrieval

### Response Generation
- OpenAI GPT-3.5-turbo for natural language generation
- Context-aware responses with source attribution
- Temperature: 0.7 for balanced creativity and accuracy

### Frontend
- React with Chakra UI for modern, responsive design
- Real-time chat interface with markdown support
- Source attribution badges for transparency

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 