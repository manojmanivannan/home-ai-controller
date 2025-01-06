# Home AI Controller
Home AI Controller 💬  is a REST framework running on the Langgraph module and open-source LLMs like llama, Mixtral, etc. It provides a conversational AI interface to control home automation devices. This works in tandem with [home-controller](https://github.com/manojmanivannan/home-controller) project which servers as the home automation server

## Features
- [x] List rooms and devices
- [x] Turn on/off device
- [ ] Turn on/off all devices in room

## Project Structure
```bash
.env
.env-example
.gitignore
.python-version
docker-compose.yaml
Dockerfile
engine/
    __init__.py
    __pycache__/
    apis/
        __pycache__/
        api.py
        opts/
        router/
    common/
        __init__.py
        __pycache__/
        logger.py
        logging.conf
    configuration/
        __init__.py
        __pycache__/
        config_loader.py
    framework/
        __init__.py
        __pycache__/
        agents/
        history/
        models/
        tools/
    main.py
Makefile
requirements.txt
tests/
    test.configuration.yaml
venv/
    bin/
    include/
    lib/
    lib64
    pyvenv.cfg
```
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
2. Access the API documentation at http://localhost:8001/swagger.

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
Configuration is managed through the ConfigLoader class in `config_loader.py`. The configuration file path is specified in the `.env` file.

### Logging
Logging configuration is defined in logging.conf.

## API Endpoints
- Health Check: GET /health
- Ask Question: POST / (defined in conversation.py)
