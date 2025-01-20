from fastapi import APIRouter

router = APIRouter(prefix="/posts")

@router.get("/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]