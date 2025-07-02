from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict
from utils.suggestion_engine import suggest_plans
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends
import jwt
from datetime import datetime, timedelta

app = FastAPI(title="MyLICAdvisor Backend")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ManualInput(BaseModel):
    # Accept any validated input keys dynamically
    # pydantic won't enforce strict schema here so frontend config drives validation
    __root__: Dict[str, Any]

@app.post("/api/manual_suggestion")
async def manual_suggestion(input_data: ManualInput):
    try:
        recommended = suggest_plans(input_data.__root__)
        return {"recommended_plans": recommended}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

@app.post("/api/guided_suggestion")
async def guided_suggestion(input_data: Dict[str, Any]):
    """
    Accepts user-selected life goal and returns suggested plans mapped to that goal.
    """
    try:
        goal = input_data.get("goal")
        if not goal:
            raise HTTPException(status_code=400, detail="Missing 'goal' in request body.")

        # Placeholder logic: when you create goal-plan mappings later, replace this with real logic.
        if goal == "child_education":
            plans = [plan for plan in PLANS_CONFIG if "child" in plan["plan_name"].lower()]
        else:
            plans = PLANS_CONFIG  # fallback: return all plans

        return {"recommended_plans": plans}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import Body

@app.get("/api/admin/plans")
async def get_all_plans():
    """
    Returns all plans for admin panel.
    """
    return {"plans": PLANS_CONFIG}

@app.post("/api/admin/plans")
async def create_plan(new_plan: Dict[str, Any] = Body(...)):
    """
    Add a new plan (in-memory only for now).
    """
    PLANS_CONFIG.append(new_plan)
    return {"message": "Plan added", "plan": new_plan}

@app.put("/api/admin/plans/{plan_id}")
async def update_plan(plan_id: str, updated_plan: Dict[str, Any] = Body(...)):
    """
    Update existing plan by plan_id.
    """
    for idx, plan in enumerate(PLANS_CONFIG):
        if plan["plan_id"] == plan_id:
            PLANS_CONFIG[idx] = updated_plan
            return {"message": "Plan updated", "plan": updated_plan}
    raise HTTPException(status_code=404, detail="Plan not found")

@app.delete("/api/admin/plans/{plan_id}")
async def delete_plan(plan_id: str):
    """
    Delete plan by plan_id.
    """
    global PLANS_CONFIG
    new_plans = [p for p in PLANS_CONFIG if p["plan_id"] != plan_id]
    if len(new_plans) == len(PLANS_CONFIG):
        raise HTTPException(status_code=404, detail="Plan not found")
    PLANS_CONFIG = new_plans
    return {"message": "Plan deleted"}

GOALS_CONFIG = [
    {
        "goal_id": "child_education",
        "goal_name": "Child Education",
        "description": "Save for your child's education."
    },
    {
        "goal_id": "retirement",
        "goal_name": "Retirement Planning",
        "description": "Plan for a comfortable retirement."
    }
]

@app.get("/api/admin/goals")
async def get_all_goals():
    """
    Returns all life goals for admin panel.
    """
    return {"goals": GOALS_CONFIG}

@app.post("/api/admin/goals")
async def create_goal(new_goal: Dict[str, Any] = Body(...)):
    """
    Add a new goal (in-memory only for now).
    """
    GOALS_CONFIG.append(new_goal)
    return {"message": "Goal added", "goal": new_goal}

@app.put("/api/admin/goals/{goal_id}")
async def update_goal(goal_id: str, updated_goal: Dict[str, Any] = Body(...)):
    """
    Update existing goal by goal_id.
    """
    for idx, goal in enumerate(GOALS_CONFIG):
        if goal["goal_id"] == goal_id:
            GOALS_CONFIG[idx] = updated_goal
            return {"message": "Goal updated", "goal": updated_goal}
    raise HTTPException(status_code=404, detail="Goal not found")

@app.delete("/api/admin/goals/{goal_id}")
async def delete_goal(goal_id: str):
    """
    Delete goal by goal_id.
    """
    global GOALS_CONFIG
    new_goals = [g for g in GOALS_CONFIG if g["goal_id"] != goal_id]
    if len(new_goals) == len(GOALS_CONFIG):
        raise HTTPException(status_code=404, detail="Goal not found")
    GOALS_CONFIG = new_goals
    return {"message": "Goal deleted"}

@app.post("/api/download_plan_pdf")
async def download_plan_pdf(plan_id: str = Body(...)):
    """
    Generate a PDF for given plan_id and return file.
    """
    plan = next((p for p in PLANS_CONFIG if p["plan_id"] == plan_id), None)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    pdf_path = generate_plan_pdf(plan)
    return FileResponse(pdf_path, media_type="application/pdf", filename=f"{plan_id}_illustration.pdf")

SECRET_KEY = "your-secret-key"  # TODO: store securely in env var later

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/admin/login")

ADMIN_USER = {"username": "admin", "password": "admin123"}  # TODO: move to db or env

def create_jwt(data: dict, expires_delta: timedelta):
    payload = data.copy()
    expire = datetime.utcnow() + expires_delta
    payload.update({"exp": expire})
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@app.post("/api/admin/login")
async def admin_login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != ADMIN_USER["username"] or form_data.password != ADMIN_USER["password"]:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_jwt({"sub": form_data.username}, timedelta(hours=1))
    return {"access_token": token, "token_type": "bearer"}    