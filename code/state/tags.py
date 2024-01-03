import json
import re
from typing import Union
import itertools


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
    
    def __repr__(self) -> str:
        return f"#{self.name}({', '.join([str(v) for v in self.values])})"

class Tags:
    def __init__(self):
        self.tags = {}

    def parse(self, filename: str, data: str):
        # print(data)
        data = json.loads(data)
        if "values" not in data:
            raise Exception("Invalid item tag file: " + filename)
        
        tag_id = self._get_name_from_path(filename)
        if tag_id not in self.tags:
            self.tags[tag_id] = Tag(tag_id)
            
        for item in data["values"]:
            if not isinstance(item, str):
                item = item["id"]
            if item[0] != "#":
                self.tags[tag_id].add(item)
                continue

            item = item[1:]
            if item not in self.tags:
                self.tags[item] = Tag(item)
            self.tags[tag_id].add(self.tags[item])
            self.tags[item].add_parent(self.tags[tag_id])

    def _get_name_from_path(self, filename: str) -> str:
        regex = re.search("data\/([^\/]+)\/tags\/items\/(.+)\.json", filename)
        if not regex:
            raise Exception("Invalid item tag filename: " + filename)
        return regex.group(1)+":"+regex.group(2)
    
    def __getitem__(self, key: int) -> Union[str, 'Tag']:
        return self.tags[key]