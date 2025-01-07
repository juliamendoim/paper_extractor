from pydantic import BaseModel
from typing import Optional

class DFSchema(BaseModel):
    name: str
    statement_text: Optional[str] = None
    section_level_0: Optional[str] = None
    section_level_1: Optional[str] = None
    section_level_2: Optional[str] = None
    outcome_measure: Optional[str] = None

class LLMSchema(BaseModel):
    statement_text: str
    section_level_1: str
    section_level_2: str
    outcome_measure: str

class LLMOutput(BaseModel):
    data: list[LLMSchema]