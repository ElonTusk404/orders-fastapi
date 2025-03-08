from pydantic import BaseModel
from typing import List


class DecodedToken(BaseModel):
    user_id: str
    scopes: List[str]