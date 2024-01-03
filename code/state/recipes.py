from collections import defaultdict
import json
from dtos.exceptions import InvalidIngredientError
from dtos.recipes import Recipe


class RecipesManager:
    def __init__(self):
        self.recipes = defaultdict(list)

    def parse(self, filename: str, data: str) -> None:
        data = json.loads(data)
        if "type" not in data:
            raise Exception("Invalid recipe file: " + filename)

        try:
            recipe = Recipe.make(data)
        except InvalidIngredientError:
            return
        if recipe is None:
            return

        for result in recipe.result:
            self.recipes[result.item].append(recipe)

    def of(self, item: str) -> list[Recipe]:
        return self.recipes[item]