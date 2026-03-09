from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from routers.users import router as UsersRouter
from routers.posts import router as PostsRouter

app = FastAPI(title="Blog")


@app.get("/", status_code=200)
def home():
    return FileResponse("static/index.html")


app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(UsersRouter)
app.include_router(PostsRouter)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8888)
