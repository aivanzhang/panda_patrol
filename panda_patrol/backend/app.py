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


# Create a new patrol run
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

    return {"success": True}


# Resolve a patrol run
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


@app.get("/patrol_groups")
def get_patrol_groups(db: Session = Depends(get_db)):
    patrol_groups = db.query(PatrolGroup).all()
    return patrol_groups


@app.delete("/patrol_group/{group_id}")
def delete_patrol_group(group_id: int, db: Session = Depends(get_db)):
    associated_patrols = db.query(Patrol).filter(Patrol.group_id == group_id).all()

    for patrol in associated_patrols:
        patrol_setting = (
            db.query(PatrolSetting).filter(PatrolSetting.patrol_id == patrol.id).first()
        )
        if patrol_setting:
            db.query(PatrolParameter).filter(
                PatrolParameter.setting_id == patrol_setting.id
            ).delete()

        # Delete the patrol's setting
        db.query(PatrolSetting).filter(PatrolSetting.patrol_id == patrol.id).delete()

        # Delete associated runs for the patrol
        db.query(PatrolRun).filter(PatrolRun.patrol_id == patrol.id).delete()

        # Delete the patrol itself
        db.query(Patrol).filter(Patrol.id == patrol.id).delete()

    db.query(PatrolGroup).filter(PatrolGroup.id == group_id).delete()
    db.commit()
    return {"success": True}


@app.get("/patrol/{patrol_id}")
def get_patrol(patrol_id: int, db: Session = Depends(get_db)):
    patrol = db.query(Patrol).filter(Patrol.id == patrol_id).first()
    runs = (
        db.query(PatrolRun.status, PatrolRun.return_value)
        .filter(PatrolRun.patrol_id == patrol_id)
        .all()
    )
    runs_array = []
    for run in runs:
        runs_array.append({"status": run.status, "return_value": run.return_value})
    return {"patrol": patrol.__dict__, "runs": runs_array}


@app.get("/patrol_parameters/")
def get_patrol_parameters(
    group_name: str,
    patrol_name: str,
    db: Session = Depends(get_db),
):
    parameters = (
        db.query(PatrolParameter)
        .join(PatrolSetting, PatrolParameter.setting_id == PatrolSetting.id)
        .join(Patrol, PatrolSetting.patrol_id == Patrol.id)
        .join(PatrolGroup, Patrol.group_id == PatrolGroup.id)
        .filter(PatrolGroup.name == group_name, Patrol.name == patrol_name)
        .all()
    )
    return parameters


# @app.get("/patrol_parameters/{param_id}")
# def get_specific_patrol_parameter(
#     param_id: int,
#     user_id: int = Header(...),
#     group_name: str = Query(...),
#     patrol_name: str = Query(...),
#     type: str = Query(...),
#     db: Session = Depends(get_db),
# ):
#     parameter = (
#         db.query(PatrolParameter)
#         .join(PatrolSetting, PatrolParameter.setting_id == PatrolSetting.id)
#         .join(Patrol, PatrolSetting.patrol_id == Patrol.id)
#         .join(PatrolGroup, Patrol.group_id == PatrolGroup.id)
#         .filter(
#             PatrolGroup.name == group_name,
#             Patrol.name == patrol_name,
#             Patrol.user_id == user_id,
#             PatrolParameter.parameter_id == param_id,
#             PatrolParameter.type == type,
#         )
#         .first()
#     )
#     if not parameter:
#         raise HTTPException(status_code=404, detail="Parameter not found.")
#     return {"value": parameter}
