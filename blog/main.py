from fastapi import FastAPI

app = FastAPI(title="Blog")

@app.get("/")
def home():
    return {
        "Message": "Welcome Home"
    }