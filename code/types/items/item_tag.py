from types.items.ingredient import Ingredient

class ItemTag(Ingredient):
    tag: str
    amount: int = 1