from fastapi import FastAPI, Request
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.routes.userRoutes import router as userRouter


app = FastAPI()

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com", "*"]
)

app.include_router(userRouter, prefix="/api/v1/users")


@app.middleware("http")
async def addCustomHeader(request: Request, call_next):
    print(type(request.headers))
    response = await call_next(request)
    response.headers["X-app-type"] = "FastAPI"
    return response


@app.get("/")
async def index():
    return {"status": "Success"}
