from fastapi import FastAPI
from app.api.upload import router as upload_router

app = FastAPI()
app.include_router(upload_router)





if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', reload=True)