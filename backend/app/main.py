from fastapi import FastAPI

app = FastAPI(title="Trader Lab API")


@app.get("/")
def health_check():
    return {"message": "Trader Lab API is running"}
