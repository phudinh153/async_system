from fastapi import APIRouter
import sys
from pathlib import Path
from infrastructure.utils.authentication import authenticate

# Add project root to Python path
root_path = Path(__file__).parent.parent.parent
sys.path.append(str(root_path))

router = APIRouter(prefix="/posts")

@router.get("/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.post("/")
async def create_post():
    # create post
    # fanout to followers
    return {"title": "ABS", "content": "XYZ"}


@authenticate
def create_posts():
    print("Post creating")
    return "Post Created"

if __name__ == "__main__":
    # This will only run when file is executed directly
    print(create_posts())
