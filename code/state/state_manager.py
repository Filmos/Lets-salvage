from reading.reader import Reader
from state.tags import Tags


class StateManager:
    def __init__(self):
        self.tags = Tags()
    
    def load(self, reader: Reader) -> 'StateManager':
        reader.clone()\
              .bind("data/*/tags/items/**/*.json", self.tags.parse)\
              .read()
        return self