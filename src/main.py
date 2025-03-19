from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

from src.routes import router

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
