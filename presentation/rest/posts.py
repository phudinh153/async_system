from fastapi import APIRouter

router = APIRouter(prefix="/posts")

@router.get("/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.post("/")
async def create_post():
    # create post
    # fanout to followers
    return {"title": "ABS", "content": "XYZ"}