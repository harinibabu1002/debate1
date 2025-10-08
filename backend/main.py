from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from graph import app as graph_app  # Your compiled graph

load_dotenv()

app = FastAPI(title="AI Tweet Generator API")  # <-- Renamed to 'app'

# CORS for frontend (add your dev/prod URLs)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")  # <-- New root route
async def root():
    return {"message": "AI Tweet Generator API", "docs": "http://localhost:8000/docs", "generate": "POST /generate"}
class PromptRequest(BaseModel):
    prompt: str

class Response(BaseModel):
    output: str

@app.post("/generate", response_model=Response)  # <-- Uses 'app'
async def generate_tweet(request: PromptRequest):
    try:
        response = graph_app.invoke(HumanMessage(content=request.prompt))
        return Response(output=str(response[-1].content))  # Last message (final tweet)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")  # <-- Uses 'app'
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # <-- Renamed to 'app'