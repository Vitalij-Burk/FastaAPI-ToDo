from pydantic import BaseModel
from pydantic import ConfigDict


class TunedModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
