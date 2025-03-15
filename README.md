# dialpad-connector
Create venv (first time):
```
python -m venv dialpad-connector     
```

Activate venv:
```
source dialpad-connector/bin/activate
```

To run server:
```
uvicorn main:app --reload
```

Run Redis docker image
```
docker run --name redis -p 6379:6379 -d redis
```