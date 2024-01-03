from collections import defaultdict
from dtos.items import Ingredient, Item
from dtos.recipes.recipe import Recipe


class ShapedRecipe:
    @classmethod
    def make(cls, data: dict) -> 'ShapedRecipe':
        keys = defaultdict(int)
        for line in data["pattern"]:
            for char in line:
                if char != " ":
                    keys[char] += 1

        ingredients = []
        for ingredient in keys.keys():
            ingredients.append(Ingredient.make(data["key"][ingredient], amount=keys[ingredient]))
        
        return Recipe(ingredients=ingredients, result=[Item(**data["result"])])
    

class ShapelessRecipe:
    @classmethod
    def make(cls, data: dict) -> 'ShapelessRecipe':
        ingredients = {}
        for item in data["ingredients"]:
            item = Ingredient.make(item)
            if item.id not in ingredients:
                ingredients[item.id] = item
            else:
                ingredients[item.id].amount += item.amount
        
        return Recipe(ingredients=list(ingredients.values()), result=[Item(**data["result"])])
    
Recipe.register("minecraft:crafting_shaped", ShapedRecipe.make)
Recipe.register("minecraft:crafting_shapeless", ShapelessRecipe.make)