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

## Salesforce preview:
![image](https://github.com/user-attachments/assets/fbe4028b-086c-4c95-84cc-9665410dc638)

<img width="1337" alt="Screenshot 2025-03-15 at 8 32 31 AM" src="https://github.com/user-attachments/assets/de9fb03c-55c3-4787-8eee-3d91c5cef068" />
