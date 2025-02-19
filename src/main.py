from typing import Union, Annotated, Literal
from loguru import logger
from fastapi import APIRouter
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from dataclasses import dataclass
from config import settings
from infrastructure.application import create
from presentation import rest

logger.add(
    "".join(
        [
            str(settings.root_dir),
            "/logs/",
            settings.logging.file.lower(),
            ".log",
        ]
    ),
    format=settings.logging.format,
    rotation=settings.logging.rotation,
    compression=settings.logging.compression,
    level="INFO",
)


app = create(
    debug=settings.debug,
    rest_routers=(rest.posts.router, rest.users.router),
    startup_tasks=None,
    shutdown_tasks=None,
)

router = APIRouter()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Annotated[str | None, Query(max_length=50)] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.price, "item_id": item_id}


class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}
    limit: int = Field(10, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"


@app.get("/items/")
async def read_items(filter_query: FilterParams):
    return {"data": filter_query}


@dataclass
class Feed:
    id: int
    content: str
    user_id: int

    def create_feed(self, id, content, user_id):
        return Feed(id=id, content=content, user_id=user_id)

    def get_feed(self, feed_id: int) -> "Feed":
        return Feed(id=feed_id, content="Hello", user_id=1)


class User:
    id: int
    name: str

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def get_feed(self, feed_id: int) -> Feed:
        return Feed(id=feed_id, content="Hello", user_id=self.id)

