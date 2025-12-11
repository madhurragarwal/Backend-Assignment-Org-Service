from pydantic import BaseModel, EmailStr
from typing import Optional

# --- Input Models (What the user sends) ---

class OrganizationCreate(BaseModel):
    organization_name: str
    email: EmailStr  # Validates email format automatically
    password: str

class OrganizationUpdate(BaseModel):
    organization_name: str
    email: EmailStr
    password: str

class AdminLogin(BaseModel):
    email: EmailStr
    password: str

# --- Output/Response Models (What we send back) ---

class OrganizationResponse(BaseModel):
    organization_name: str
    message: str

class Token(BaseModel):
    access_token: str
    token_type: str
    org_id: Optional[str] = None