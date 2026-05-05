from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pipelines.answer_query import process_full_query

app = FastAPI()

# Montage des fichiers statiques (HTML/CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

class UserRequest(BaseModel):
    station: str
    question: str

@app.post("/ask")
async def ask_horizon(req: UserRequest):
    answer = process_full_query(req.station, req.question)
    return {"answer": answer}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)