from reading.reader import Reader
from state.recipes import RecipesManager
from state.tags import TagsManager


class StateManager:
    def __init__(self):
        self.tags = TagsManager()
        self.recipes = RecipesManager()
    
    def load(self, reader: Reader) -> 'StateManager':
        reader.clone()\
              .bind("data/*/tags/items/**/*.json", self.tags.parse)\
              .bind("data/*/recipes/**/*.json", self.recipes.parse)\
              .read()
        return self