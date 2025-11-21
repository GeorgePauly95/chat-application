from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users/{user_id}")
async def show_user_details(user_id: int):
    return {"user_id": user_id * 10}
