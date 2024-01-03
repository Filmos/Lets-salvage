from dtos.items import Item, Ingredient
from dtos.recipes import Recipe
from state.state_manager import StateManager

REPRESENTATIONS = {
    "#c:wood_sticks": "minecraft:stick"
}

class SalvageModule:
    def __init__(self, *, targets: list[str], valid_ingredients: list[str]):
        self.targets = targets
        self.valid_ingredients = valid_ingredients

    def run(self, state: StateManager) -> None:
        valid_ingredients = state.tags.create_temporary_tag(self.valid_ingredients)
        targets = state.tags.create_temporary_tag(self.targets)

        for item in set(targets.all()):
            recipes = state.recipes.of(item)
            if len(recipes) != 1:
                continue
            recipe = recipes[0]

            for ingredient in recipe.ingredients:
                if ingredient not in valid_ingredients:
                    break
            else:
                new_recipe = Recipe(
                    ingredients=[Item(item=item, amount=1)], 
                    result=[self._get_representation(i) for i in recipe.ingredients]
                )
                print(f"[Salvaging] {new_recipe}")
            
    def _get_representation(self, item: Ingredient) -> Item:
        if isinstance(item, Item):
            return item
        if item.id in REPRESENTATIONS:
            return Item(item=REPRESENTATIONS[item.id], amount=item.amount)
        raise Exception(f"No known representation for {item}")
        