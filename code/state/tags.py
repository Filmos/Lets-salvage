import json
import re
from typing import Union
import itertools
from dtos.items import Ingredient


class Tag:
    def __init__(self, name: str):
        self.name = name
        self.values: list[Union[str, 'Tag']] = []
        self.parents: list['Tag'] = []

    def add(self, value: Union[str, 'Tag']) -> 'Tag':
        self.values.append(value)
        return self

    def add_parent(self, parent: 'Tag') -> 'Tag':
        self.parents.append(parent)
        return self
    
    def all(self) -> list[Union[str, 'Tag']]:
        return list(itertools.chain.from_iterable([[v] if isinstance(v, str) else v.all() for v in self.values]))
    
    @property
    def subtags(self) -> list['Tag']:
        return [v for v in self.values if isinstance(v, Tag)]

    def __contains__(self, item: Union[str, 'Tag', Ingredient]) -> bool:
        if isinstance(item, Ingredient):
            item = item.id
        if item == f"#{self.name}" or item == self or item in self.values:
            return True
        for subtag in self.subtags:
            if item in subtag:
                return True
        return False

    def __repr__(self) -> str:
        return f"#{self.name}({', '.join([str(v) for v in self.values])})"

class TagsManager:
    def __init__(self):
        self.tags = {}

    def parse(self, filename: str, data: str) -> None:
        data = json.loads(data)
        if "values" not in data:
            raise Exception("Invalid item tag file: " + filename)
        
        tag_id = self._get_name_from_path(filename)
        for item in data["values"]:
            self.add(tag_id, item)

    def add(self, tag_id: str, item: str) -> None:
        if tag_id not in self.tags:
            self.tags[tag_id] = Tag(tag_id)
        item = self._parse_tag_string(item)
        self.tags[tag_id].add(item)
        if not isinstance(item, str):
            item.add_parent(self.tags[tag_id])

    def create_temporary_tag(self, items: list[str]) -> Tag:
        tag = Tag("temporary")
        for item in items:
            tag.add(self._parse_tag_string(item))
        return tag
    
    def _parse_tag_string(self, item: str) -> Tag:
        if not isinstance(item, str):
            item = item["id"]
        if item[0] != "#":
            return item

        item = item[1:]
        if item not in self.tags:
            self.tags[item] = Tag(item)
        return self.tags[item]

    def _get_name_from_path(self, filename: str) -> str:
        regex = re.search("data\/([^\/]+)\/tags\/items\/(.+)\.json", filename)
        if not regex:
            raise Exception("Invalid item tag filename: " + filename)
        return regex.group(1)+":"+regex.group(2)
    
    def __getitem__(self, key: int) -> Union[str, 'Tag']:
        return self.tags[key]