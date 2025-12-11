# Organization Management Service (Backend Intern Assignment)

## Overview
This is a backend service built with **FastAPI** and **MongoDB** that manages organizations in a multi-tenant architecture. It separates data logic using a **Master Database** for metadata and **Dynamic Collections** for each organization's isolated data.

## 🛠 Tech Stack
* **Language:** Python 3.10+
* **Framework:** FastAPI
* **Database:** MongoDB
* **Authentication:** JWT (JSON Web Tokens) with BCrypt hashing
* **Validation:** Pydantic

## 🚀 Setup Instructions

1.  **Clone the repository**
    ```bash
    git clone <your-repo-url>
    cd org-service
    ```

2.  **Create Virtual Environment & Install Dependencies**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    pip install fastapi uvicorn pymongo python-dotenv pydantic email-validator passlib[bcrypt] python-jose[cryptography]
    ```

3.  **Environment Configuration**
    Create a `.env` file in the root directory:
    ```properties
    MONGO_URL=mongodb://localhost:27017
    MASTER_DB_NAME=master_org_db
    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ```

4.  **Run the Application**
    ```bash
    uvicorn app.main:app --reload
    ```
    Access the interactive API docs at: `http://127.0.0.1:8000/docs`

## 📐 Architecture & Design Decisions

### High-Level Architecture
[Client] -> [FastAPI Server] -> [Database Manager]
                                      |
                            ---------------------
                            |                   |
                     [Master DB]         [Dynamic Org Collections]
                     (Metadata)          (org_tesla, org_google, etc.)

### 🧠 Theoretical Questions & Answers

**1. Is this a good architecture with a scalable design?**
This architecture (One Collection Per Tenant) is **moderately scalable** and excellent for data isolation.
* **Pros:** It provides strict physical separation of data. If one organization has millions of records, it does not impact the query performance of other organizations. It also simplifies "Dropping" an organization (just drop the collection).
* **Cons:** MongoDB has a limit on the number of namespaces (collections). If we scale to 50,000+ organizations, managing that many collections becomes resource-heavy for the database engine.

**2. What are the trade-offs with the tech stack and design choices?**
* **FastAPI vs Django:** We chose FastAPI for speed and async capabilities, but we traded off the "batteries-included" admin panel that Django provides.
* **Dynamic Collections:** The trade-off is **Complexity vs. Security**. We added complexity in the code (`DatabaseManager`) to ensure we route to the correct collection, but we gained security by ensuring a coding error is less likely to leak Data A to Organization B.

**3. Could you design something better?**
For a massive-scale system (SaaS like Slack or Jira), I would propose **Sharding with Logical Separation**:
Instead of a new collection for every user, use a single huge collection sharded by `organization_id`.
* **Why:** This allows MongoDB to distribute data across multiple servers efficiently without the overhead of managing thousands of distinct collections. We would then enforce strict **Row-Level Security** at the application layer to ensure tenants only see their own data.