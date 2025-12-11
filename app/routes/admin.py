from fastapi import APIRouter, HTTPException, Depends
from app.models import AdminLogin, Token
from app.database import db_manager
from app.auth import verify_password, create_access_token

router = APIRouter()

@router.post("/admin/login", response_model=Token)
def login_admin(login_data: AdminLogin):
    # 1. Find the admin. 
    # Strategy: We need to know WHICH organization they belong to. 
    # Since the input is just email/pass, we might need to search or ask for Org Name.
    # However, often emails are unique across the system. 
    
    # For this assignment, we will search the Master Metadata to find which Org this email belongs to.
    master_collection = db_manager.get_master_collection()
    org_metadata = master_collection.find_one({"admin_email": login_data.email})
    
    if not org_metadata:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # 2. Verify Password in the Dynamic Collection
    # Now that we know the Org, we go to THAT collection to check the password.
    org_name = org_metadata["organization_name"]
    org_collection = db_manager.get_org_collection(org_name)
    
    user = org_collection.find_one({"email": login_data.email})
    
    if not user or not verify_password(login_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 3. Generate Token
    access_token = create_access_token(
        data={"sub": login_data.email, "org": org_name}
    )
    
    return {"access_token": access_token, "token_type": "bearer", "org_id": org_name}