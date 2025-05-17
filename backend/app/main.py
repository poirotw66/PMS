from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World from FastAPI backend!"}

@app.get("/api/v1/health")
async def health_check():
    return {"status": "ok"}