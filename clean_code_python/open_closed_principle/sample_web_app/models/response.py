from dataclasses import dataclass 

@dataclass
class Response:
    """An HTTP response"""
    status: int 
    content_type: str 
    body: str 