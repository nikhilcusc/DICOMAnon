from pydantic import BaseModel
from typing import List, Optional

class ServerPing(BaseModel):
    message: str
    version: str