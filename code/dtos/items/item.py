from dtos.items.ingredient import Ingredient

class Item(Ingredient):
    item: str

    @property
    def id(self) -> str:
        return self.item