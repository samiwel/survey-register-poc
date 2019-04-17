import json

from attr import dataclass


@dataclass
class Version:
    id: str
    form_type: str
    data: dict
    created_by: str
    lang: str
    variant: str
    description: str

    def to_json(self):
        return json.dumps(self.__dict__)
