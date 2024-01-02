from types.items.ingredient import Ingredient

class Item(Ingredient):
    item: str
    amount: int = 1