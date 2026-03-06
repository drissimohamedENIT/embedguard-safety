from pydantic import BaseModel

class RepositoryScan(BaseModel):
    repo_url: str