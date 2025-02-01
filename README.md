# RAG-app


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

-secondly run the following command on your terminal
```
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```
you will receive a link which you will use as initial value and current value in your postman collection,
after that you will add a request to the collection with the route you want to try out