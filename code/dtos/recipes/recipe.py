from typing import Callable, ClassVar, Optional
from pydantic import BaseModel
from dtos.items import Ingredient, Item


class Recipe(BaseModel):
    interpreters: ClassVar[dict[str, Callable]] = {}
    ingredients: list[Ingredient]
    result: list[Item]

    @classmethod
    def register(cls, id: str, interpreter: Callable):
        cls.interpreters[id] = interpreter

    @classmethod
    def make(cls, data: dict) -> Optional['Recipe']:
        if data["type"] not in cls.interpreters:
            return None
        return cls.interpreters[data["type"]](data)
    
    def __repr__(self) -> str:
        return f"Recipe({self.ingredients} -> {self.result})"