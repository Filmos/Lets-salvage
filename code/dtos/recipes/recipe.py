from typing import Optional
from dtos.items import Ingredient, Item


class Recipe:
    interpreters = {}

    def __init__(self, ingredients: list[Ingredient], result: Item):
        self.ingredients = ingredients
        self.result = result

    @classmethod
    def register(cls, id: str, interpreter: callable):
        cls.interpreters[id] = interpreter

    @classmethod
    def make(cls, data: dict) -> Optional['Recipe']:
        if data["type"] not in cls.interpreters:
            return None
        return cls.interpreters[data["type"]](data)
    
    def __repr__(self) -> str:
        return f"Recipe({self.ingredients} -> {self.result})"