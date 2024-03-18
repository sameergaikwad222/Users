from fastapi import FastAPI

from app.routes.userRoutes import router as userRouter



app = FastAPI()

app.include_router(userRouter)


@app.get("/")
async def index():
    return {"status": "Success"}
