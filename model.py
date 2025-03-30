from pydantic import BaseModel
import enum
from typing import List

class FeedbackType(enum.Enum):
    brilliant = "brilliant"
    blunder = "blunder"
    book_move = "book_move"
    missed_win = "missed_win"


class Feedback(BaseModel):
    file_name: str
    line_number: int
    line_text: str
    feedback: str
    type:FeedbackType

class Artifact(BaseModel):
    feedbacks: List[Feedback]
