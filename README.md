# Project explaination
This project can be simplified as a RAG "engine" as it's a scalable, flexible and easy to use open-source code to create multiple chat-bots(projects), each project can hold multiple text or pdf files, all the projects will share environmental values in the .env file of the project making it easy to change the generation model, embedding model or vectorDB from any provider available in the project using a factory design, Other values can be changed in the .env file which will  be explained in the next section.

Pull requests and any other developments are welcome so if you have any question then please e-mail me at: momaniammar44@gmail.com.


# How to use
Before getting into the requirements and actual production let's explain the enviromnetal values we talked about before.
## Environmental values
The values are as follows:
```
APP_NAME: The name you choose for your application
APP_VERSION: The version you choose for your application

ALLOWED_FILE_TYPE: The type of files allowed to be uplouded to the RAG engine, for now only the following are allowed '["text/plain", "application/pdf"]' more to come later
FILE_MAX_SIZE: Maximum size of uploaded files in MB
FILE_CHUNK_SIZE: The chunk size while uploading files to projects in KB

MONGODB_URL: The URL to the mongodb database, usually something like "mongodb://admin:admin@localhost:27017/"
MONGODB_DATABASE: The name of the database in mongodb

===== LLM Config =====
GENERATION_BACKEND: The provider for the generation model
EMBEDDING_BACKEND: The provider for the embedding model # current available providers (OpenAI, COHERE, Ollama)
OPENAI_API_KEY: In the name
OPENAI_API_URL: In the name
COHERE_API_KEY: In the name
OLLAMA_API_KEY: While Ollama is local and doesn't provide api support, this can be anything just can't be left empty is using Ollama as provider
OLLAMA_API_URL: The URL for Ollama server

GENERATION_MODEL_ID: The name of generation model
EMBEDDING_MODEL_ID: The name of embedding model
EMBEDDING_MODEL_SIZE: The vector size when embedding

DEFAULT_INPUT_MAX_CHARACTERS: The number of character that can be inputed to a model
DEFAULT_GENERATION_MAX_TOKENS: The maximum number of token generated with the response
DEFAULT_GENERATION_TEMPERATURE: Temperature used while generating

===== VectorDB Config =====
VECTOR_DB_BACKEND: The provider for vectorDB # currently available (qdrantDB)
VECTOR_DB_PATH: The name of the folder that will be created in the server
VECTOR_DB_DISTANCE_METHOD: The distance method that will be used when retrieving chunks

===== Template Config =====
PRIMARY_LANG: The language that will be used in the system prompt and template
DEFAULT_LANG: Default if the previouse is not defined
```

## Requirments
- python 3.13 or later
### make sure to activate your environment after creating it:
```
$ conda create -n RAG-app python=3.13
$ conda activate RAG-app
```

## install required packages from requirements.txt
```
$ pip install -r requirements.txt
```
## setup environment
change .env.example to .env and set your own variables in blank values:
```
$ cp .env.example .env
```

## how to run uvicorn to use app
-firstly make sure to have postman installed (or any other software to run your api)

-secondly run the following command in your terminal
```
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```
you will receive a link which you will use in postman to send request to your API.

## Requests
Before starting, the names for those request are just suggestions, and the port number is just an example.

### base_request(GET)

```
http://0.0.0.0:5000/base/
```
This request just return the app name and version to check if the API is running.

### file_uploading(POST)

```
http://0.0.0.0:5000/data/upload/{project_id}
```
This request should take a file as input, it can be done in postman from the form-data section where the **KEY** should be "file".

Also make sure the change '{project_id}' with the actual alphanumeric id of your project, not only for this request but for all the request to follow.

### file_processing(POST)

```
http://0.0.0.0:5000/data/process/{project_id}
```
This request processes the file you uploaded and takes a raw JSON input that looks like as follows:
```
{
    // "file_id" : "", //optional
    "chunk_size": 600,
    "overlap_size": 20,
    "do_reset": 1
}
```
The input defines how to process the uploaded file, for the first input if not defined then will process all the files in the project.

### push_to_vectordb(POST)

```
http://0.0.0.0:5000/nlp/index/push/{project_id}
```
This request embeds the chunks from the previouse request and then pushes them into the vectorDB, it also takes the following input:
```
{
    "do_reset": 0 // if set to 1, it will remove everything and not add vectors
}
```
### vectordb_info(GET)
```
http://0.0.0.0:5000/nlp/index/info/{project_id}
```
This just returns information about the vectors in a project.

### vectordb_search(POST)
```
http://0.0.0.0:5000/nlp/index/search/{project_id}
```
This request only returns the most relative chunks depending on inputs that are as follows:
```
{
    "text": "how old is the person mentioned in the documents",
    "limit": 6, # how many chunks to return at max
    "score_threshold": 0.6
}
```

### answer(POST)
```
http://0.0.0.0:5000/nlp/index/answer/{project_id}
```
This request takes the same exact input as the previouse request it just returns the answer instead.