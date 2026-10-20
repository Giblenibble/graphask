from fastapi import FastAPI

app = FastAPI(title="GraphAsk")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
