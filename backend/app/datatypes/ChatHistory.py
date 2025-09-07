from pydantic import BaseModel
from typing import List, Literal

class Message(BaseModel):
    role: Literal['system', 'user', 'assistant']
    content: str

    @classmethod
    def from_str(cls, input_message: str) -> "Message":
        return cls(
            role = 'user',
            content = input_message
        )

class ChatHistory(BaseModel):
    messages: List[Message]
    
    @classmethod
    def from_str(cls, input_message: str) -> "ChatHistory":
        return cls(
            messages = [Message.from_str(input_message)]
        )