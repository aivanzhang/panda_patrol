from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from panda_patrol.backend.database.models import *
from panda_patrol.backend.models import *

app = FastAPI()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create a new user
@app.post("/users/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

app = FastAPI()


@app.post("/patrol/run", response_model=SuccessResponse)
def create_patrol_run(patrol_run: PatrolRunCreate, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter_by(id=patrol_run.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    # Create or get patrol_group
    patrol_group = (
        db.query(PatrolGroup)
        .filter_by(name=patrol_run.patrol_group, user_id=patrol_run.user_id)
        .first()
    )
    if not patrol_group:
        patrol_group = PatrolGroup(
            name=patrol_run.patrol_group, user_id=patrol_run.user_id
        )
        db.add(patrol_group)
        db.commit()

    # Create or get patrol
    patrol = (
        db.query(Patrol)
        .filter_by(name=patrol_run.patrol, group_id=patrol_group.id)
        .first()
    )
    if not patrol:
        patrol = Patrol(name=patrol_run.patrol, group_id=patrol_group.id)
        db.add(patrol)
        db.commit()

    # Create or get patrol_settings
    patrol_setting = db.query(PatrolSetting).filter_by(patrol_id=patrol.id).first()
    if not patrol_setting:
        patrol_setting = PatrolSetting(patrol_id=patrol.id)
        db.add(patrol_setting)
        db.commit()

    # Create patrol_run
    patrol_run_instance = PatrolRun(
        patrol_id=patrol.id,
        status=patrol_run.status,
        severity=patrol_run.severity,
        patrol_code=patrol_run.patrol_code,
        logs=patrol_run.logs,
        return_value=patrol_run.return_value,
        start_time=patrol_run.start_time,
        end_time=patrol_run.end_time,
        exception=patrol_run.exception,
    )
    db.add(patrol_run_instance)
    db.commit()


@app.post("/patrol/{patrol_id}/run/{run_id}/resolve", response_model=SuccessResponse)
def resolve_patrol_run(patrol_id: int, run_id: int, db: Session = Depends(get_db)):
    patrol_run = db.query(PatrolRun).filter_by(id=run_id, patrol_id=patrol_id).first()
    if not patrol_run:
        raise HTTPException(
            status_code=404, detail="Run not found for the given patrol."
        )

    patrol_run.status = "success"
    db.commit()

    return {"success": True}


# @app.get("/summary/{user_id}")
# def get_summary(user_id: str, db: Session = Depends(get_db)):
#     # Subquery for latest runs
#     latest_runs = (
#         db.query(PatrolRun.patrol_id, func.max(PatrolRun.id).label("run_id"))
#         .group_by(PatrolRun.patrol_id)
#         .subquery()
#     )

#     # Main query
#     summary = (
#         db.query(
#             func.count().label("total"),
#             func.sum(case((PatrolRun.status == "success", 1), else_=0)).label(
#                 "success"
#             ),
#             func.sum(case((PatrolRun.status == "failure", 1), else_=0)).label(
#                 "failure"
#             ),
#             func.sum(case((PatrolRun.status == "skipped", 1), else_=0)).label(
#                 "skipped"
#             ),
#             func.sum(case((PatrolRun.severity == "critical", 1), else_=0)).label(
#                 "critical"
#             ),
#             func.sum(case((PatrolRun.severity == "warning", 1), else_=0)).label(
#                 "warning"
#             ),
#             func.sum(case((PatrolRun.severity == "info", 1), else_=0)).label("info"),
#         )
#         .join(Patrol, Patrol.id == PatrolRun.patrol_id)
#         .filter(and_(Patrol.user_id == user_id, PatrolRun.id.in_(latest_runs)))
#         .first()
#     )

#     print(latest_runs)

# return {
#     "total": summary.total,
#     "success": summary.success,
#     "failure": summary.failure,
#     "skipped": summary.skipped,
#     "critical": summary.critical,
#     "warning": summary.warning,
#     "info": summary.info,
# }
