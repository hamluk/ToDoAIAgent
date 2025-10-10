from pydantic import BaseModel, field_validator
import re


class TrelloCard(BaseModel):
    idList: str
    name: str
    desc: str | None = None
    due: str | None = None
    idLabels: list[str] = []

    @field_validator("idList")
    @classmethod
    def validate_idList(cls, idList: str) -> str:
        pattern = re.compile("^[0-9a-fA-F]{24}$")
        if pattern.match(idList):
            return idList
        
        raise ValueError("idList must match pattern: '^[0-9a-fA-F]{24}$'")
    
    def __str__(self):
        return f"""TrelloCard {self.name} with description {self.desc} is due at {self.due} and has the labels {self.idLabels} attached to it."""