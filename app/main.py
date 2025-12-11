from fastapi import FastAPI
from app.routes import organization, admin  # Import the new route files

app = FastAPI(
    title="Organization Management Service",
    description="Backend Intern Assignment",
    version="1.0.0"
)

# Register the routers
app.include_router(organization.router)
app.include_router(admin.router)

@app.get("/")
def read_root():
    return {"message": "Service is up and running!", "status": "active"}