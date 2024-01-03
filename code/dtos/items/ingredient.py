from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import ClassVar, Optional
from dtos.exceptions import InvalidIngredientError

class Ingredient(BaseModel, ABC):
    subclasses: ClassVar['Ingredient'] = []
    amount: int = 1

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Ingredient.subclasses.append(cls)
        
    @classmethod
    def make(cls, data: dict, *, amount: Optional[int] = None) -> 'Ingredient':
        ingredient = None
        for subclass in cls.subclasses:
            try:
                ingredient = subclass(**data)
                break
            except:
                pass
        if ingredient is None:
            raise InvalidIngredientError(f"Could not make Ingredient from {data}")
        
        if amount is not None:
            ingredient.amount = amount
        return ingredient
    
    @property
    @abstractmethod
    def id(self) -> str:
        pass