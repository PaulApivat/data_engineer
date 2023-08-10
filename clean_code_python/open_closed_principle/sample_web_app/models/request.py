from dataclasses import dataclass

@dataclass
class HttpRequest:
    method: str 
    path: str 
    headers: str 
    body: str = "Making a HTTP Request"