from dtos.items.ingredient import Ingredient

class ItemTag(Ingredient):
    tag: str

    @property
    def id(self) -> str:
        return "#"+self.tag