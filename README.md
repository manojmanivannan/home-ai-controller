# Home AI Controller
Home AI Controller 💬  is a REST framework running on the Langgraph module and open-source LLMs like llama, Mixtral, or OpenAI, etc. It provides a conversational AI interface to control home automation devices. This works only in tandem with [home-automation-server](https://github.com/manojmanivannan/home-automation-server) project which servers as the home automation server

## Features
- [x] List rooms and devices
- [x] Turn on/off device
- [ ] Turn on/off all devices in room

## Getting Started
### Prerequisites
- Python 3.11.9
- Docker
- Make

### Installation
1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Set up the virtual environment:
```bash
make venv
```

3. Configure environment variables:
```bash
cp .env-example .env
# Edit .env to add your configuration
```

4. Install dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Running the Application
1. Start the application using Docker Compose:
```bash
make run
```
2. Access the API documentation at http://localhost:8001/swagger. or UI at http://localhost:8501 to chat interactively.

#### Running without docker-compose:
1. `make venv` to prepare virtual env
2. `source venv/bin/activate` to activate the virtual env
3. `source .env` to load env variables
4. `fastapi run engine/main.py --port 8001`

### Stopping the Application
1. Stop the application:
```bash
make stop
```

## Configuration
Configuration to the AI framework is managed through `configuration.yaml` and `.env`. 

In `configuration.yaml`, set the language model to use under `engine:`, if you choose `openai`, then set the `OPENAI_API_KEY` of if you choose `ollama`, then set the `OLLAMA_HOST` in `.env` file.

### Logging
Logging configuration is defined in `logging.conf`.

## API Endpoints
- Health Check: GET /health
- Ask Question: POST / (defined in conversation.py)

### Example
```bash
curl -X 'POST' \
  'http://localhost:8001/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{ 
        "conversation_id": "123123", 
        "question": "are you sure ?" 
  }'
```