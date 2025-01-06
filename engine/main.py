from fastapi import FastAPI
from .apis.router import conversation
from .common.logger import log


description = """
Home AI Controller 💬 is the REST framework running 
on [LangChain](https://www.langchain.com/) module and open-source LLM like llama, Mixtral, etc

## Features

You will be able to:

- [x] List rooms and devices
- [x] Turn on/off device
- [ ] Turn on/off all devices in room

"""

app = FastAPI(
    title="Home AI Controller",
    docs_url="/swagger", 
    description=description,
    openapi_url="/api/v1/openapi.json",
    defaultModelRendering=["example*", "model"],  # ["example", "model"]"example", "model"],
    defaultModelExpandDepth=5,

    )

# def custom_openapi():

#     in_file = "openapi/openapi.yaml"

#     with open(in_file) as file:
#         openapi_schema = yaml.YAML(typ='safe').load(file)

#     del openapi_schema["servers"]
#     app.openapi_schema = openapi_schema
#     return openapi_schema

@app.get("/health")
def get_status():
    log.info('get_status')
    return {"status": "Engine Running"}

# @app.middleware("http")
# async def log_request_headers(request, call_next):
#     log.info(request.headers)
#     return await call_next(request)

app.include_router(conversation.router)
# app.openapi = custom_openapi