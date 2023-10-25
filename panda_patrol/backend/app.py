from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
import json
from panda_patrol.data.patrol_result import Status
from panda_patrol.backend.utils.email_utils import send_failure_email
from panda_patrol.backend.utils.slack_utils import send_slack_message
from panda_patrol.backend.database.models import *
from panda_patrol.backend.models import *

app = FastAPI()
origins = ["*"]
static_dir_path = os.path.join(
    os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))), "./static"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount(
    "/static",
    StaticFiles(directory=static_dir_path),
    name="static",
)


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Get all users
@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(Person).all()
    return users


# Add a new user
@app.post("/user")
def add_user(person: PersonRequest, db: Session = Depends(get_db)):
    if db.query(Person).filter_by(email=person.email).first():
        raise HTTPException(status_code=400, detail="Email already exists.")
    new_user = Person(name=person.name, email=person.email)
    db.add(new_user)
    db.commit()
    return {"success": True}


# Remove a user
@app.delete("/user")
def delete_user(email: str, db: Session = Depends(get_db)):
    user = db.query(Person).filter_by(email=email).first()
    if user:
        db.delete(user)
        db.commit()

    return {"success": True}


# Get patrol details and all its runs
@app.get("/patrol/{patrol_id}/run/{run_id}")
def get_patrol_run(patrol_id: int, run_id: int, db: Session = Depends(get_db)):
    patrol_details = (
        db.query(Patrol, PatrolSetting, PatrolGroup.name)
        .outerjoin(PatrolGroup, Patrol.group_id == PatrolGroup.id)
        .outerjoin(PatrolSetting, Patrol.id == PatrolSetting.patrol_id)
        .filter(Patrol.id == patrol_id)
        .first()
    )
    if not patrol_details:
        raise HTTPException(status_code=404, detail="Patrol not found.")

    all_runs = (
        db.query(
            PatrolRun.id,
            PatrolRun.status,
            PatrolRun.return_value,
            PatrolRun.severity,
            PatrolRun.end_time,
        )
        .filter_by(patrol_id=patrol_id)
        .all()
    )
    latest_run_details = (
        db.query(PatrolRun)
        .filter_by(patrol_id=patrol_id, id=run_id)
        .order_by(PatrolRun.id.desc())
        .first()
    )

    if not latest_run_details:
        raise HTTPException(
            status_code=404, detail="Run not found for the given patrol."
        )

    all_runs_array = []
    for run in all_runs:
        all_runs_array.append(
            {
                "id": run.id,
                "status": run.status,
                "severity": run.severity,
                "return_value": run.return_value,
                "end_time": run.end_time,
            }
        )

    return {
        "patrol": {
            "group_name": patrol_details[2],
            "details": patrol_details[0].__dict__,
            "settings": patrol_details[1].__dict__,
        },
        "allRuns": all_runs_array,
        "currentRunDetails": latest_run_details.__dict__,
    }


# Create a new patrol run
@app.post("/patrol/run", response_model=SuccessResponse)
def create_patrol_run(patrol_run: PatrolRunCreate, db: Session = Depends(get_db)):
    # Create or get patrol_group
    patrol_group = db.query(PatrolGroup).filter_by(name=patrol_run.patrol_group).first()
    if not patrol_group:
        patrol_group = PatrolGroup(name=patrol_run.patrol_group)
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
    else:
        db.query(PatrolSetting).filter_by(patrol_id=patrol.id).update(
            {
                PatrolSetting.silenced_until: None,
            }
        )
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

    # Check if alerts should be sent
    patrol_setting = db.query(PatrolSetting).filter_by(patrol_id=patrol.id).first()
    user_to_alert = None
    if patrol_setting.alerting and patrol_setting.assigned_to_person:
        user_to_alert = (
            db.query(Person).filter_by(id=patrol_setting.assigned_to_person).first()
        )

    # Send email if patrol failed and alerting is enabled
    if patrol_run.status == Status.FAILURE.value:
        patrolInfo = {
            "patrol_group": patrol_run.patrol_group,
            "patrol": patrol_run.patrol,
            "severity": patrol_run.severity,
            "status": patrol_run.status,
            "logs": patrol_run.logs,
            "return_value": patrol_run.return_value,
            "start_time": patrol_run.start_time,
            "end_time": patrol_run.end_time,
            "exception": patrol_run.exception,
        }
        SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK")
        if SLACK_WEBHOOK:
            send_slack_message(patrolInfo)
        if user_to_alert:
            send_failure_email(
                user_to_alert.name,
                user_to_alert.email,
                patrolInfo=patrolInfo,
            )

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


# Get all patrol groups and the number of successes and failures for the latest patrol run
@app.get("/patrol_groups")
def get_patrol_groups(db: Session = Depends(get_db)):
    patrol_groups = db.query(PatrolGroup).all()
    return patrol_groups


# Get information about a group's patrols' latest run
@app.get("/patrol_group/{group_name:path}")
def get_patrol_group(group_name: str, db: Session = Depends(get_db)):
    patrol_group = db.query(PatrolGroup).filter(PatrolGroup.name == group_name).first()
    if not patrol_group:
        raise HTTPException(status_code=404, detail="Patrol group not found.")

    patrols_latest_runs = db.execute(
        text(
            """
                SELECT patrols.id, patrols.name, patrol_runs.status, patrol_runs.end_time, patrol_runs.severity, patrol_runs.return_value
                FROM patrols
                JOIN patrol_runs ON patrol_runs.id = (
                    SELECT MAX(id) FROM patrol_runs WHERE patrol_id = patrols.id
                )
                WHERE patrols.group_id = :group_id
            """
        ),
        {"group_id": patrol_group.id},
    ).fetchall()

    patrol_ids = db.query(Patrol.id).filter(Patrol.group_id == patrol_group.id).all()
    patrol_ids = set([patrol_id[0] for patrol_id in patrol_ids])
    latest_run_date = None
    success_patrols = set()
    failed_patrols = set()
    for patrol in patrols_latest_runs:
        if patrol[2] == "success":
            success_patrols.add(patrol[1])
        elif patrol[2] == "failure":
            failed_patrols.add(patrol[1])

        if not latest_run_date or patrol[3] > latest_run_date:
            latest_run_date = patrol[3]

    return {
        "latestRunDate": latest_run_date,
        "successes": list(success_patrols),
        "fails": list(failed_patrols),
        "patrolIds": list(patrol_ids),
    }


# Delete a patrol group
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

        # Delete associated profiles for the patrol
        db.query(PatrolProfile).filter(PatrolProfile.patrol_id == patrol.id).delete()

        # Delete the patrol itself
        db.query(Patrol).filter(Patrol.id == patrol.id).delete()

    db.query(PatrolGroup).filter(PatrolGroup.id == group_id).delete()
    db.commit()
    return {"success": True}


# Get a patrol and all its runs
@app.get("/patrol/{patrol_id}")
def get_patrol(patrol_id: int, db: Session = Depends(get_db)):
    patrol = db.query(Patrol).filter(Patrol.id == patrol_id).first()
    patrol_settings = (
        db.query(PatrolSetting).filter(PatrolSetting.patrol_id == patrol_id).first()
    )
    profiles = (
        db.query(PatrolProfile.id, PatrolProfile.time)
        .filter(PatrolProfile.patrol_id == patrol_id)
        .all()
    )
    profiles_array = []
    for profile in profiles:
        profiles_array.append(
            {
                "id": profile.id,
                "time": profile.time,
            }
        )

    runs = (
        db.query(
            PatrolRun.id,
            PatrolRun.status,
            PatrolRun.return_value,
            PatrolRun.severity,
            PatrolRun.end_time,
        )
        .filter(PatrolRun.patrol_id == patrol_id)
        .all()
    )
    runs_array = []
    for run in runs:
        runs_array.append(
            {
                "id": run.id,
                "status": run.status,
                "severity": run.severity,
                "return_value": run.return_value,
                "end_time": run.end_time,
            }
        )
    return {
        "patrol": patrol.__dict__ if patrol else {},
        "settings": patrol_settings.__dict__ if patrol_settings else {},
        "runs": runs_array,
        "profiles": profiles_array,
    }


# Delete a patrol
@app.delete("/patrol/{patrol_id}")
def delete_patrol(patrol_id: int, db: Session = Depends(get_db)):
    patrol = db.query(Patrol).filter(Patrol.id == patrol_id).first()
    if not patrol:
        raise HTTPException(status_code=404, detail="Patrol not found.")

    patrol_setting = (
        db.query(PatrolSetting).filter(PatrolSetting.patrol_id == patrol_id).first()
    )
    if patrol_setting:
        db.query(PatrolParameter).filter(
            PatrolParameter.setting_id == patrol_setting.id
        ).delete()

    # Delete the patrol's setting
    db.query(PatrolSetting).filter(PatrolSetting.patrol_id == patrol_id).delete()

    # Delete associated profiles for the patrol
    db.query(PatrolProfile).filter(PatrolProfile.patrol_id == patrol_id).delete()

    # Delete associated runs for the patrol
    db.query(PatrolRun).filter(PatrolRun.patrol_id == patrol_id).delete()

    # Delete the patrol itself
    db.query(Patrol).filter(Patrol.id == patrol_id).delete()

    db.commit()
    return {"success": True}


# Get all patrol parameters for a patrol group and patrol
@app.get("/patrol_parameters/{patrol_group}/{patrol}")
def get_patrol_parameters(
    patrol_group: str,
    patrol: str,
    db: Session = Depends(get_db),
):
    parameters = (
        db.query(PatrolParameter)
        .join(PatrolSetting, PatrolParameter.setting_id == PatrolSetting.id)
        .join(Patrol, PatrolSetting.patrol_id == Patrol.id)
        .join(PatrolGroup, Patrol.group_id == PatrolGroup.id)
        .filter(PatrolGroup.id == patrol_group, Patrol.id == patrol)
        .all()
    )
    return parameters


# Delete a patrol parameter
@app.delete("/patrol_parameters/{parameter_id}")
def delete_patrol_parameter(parameter_id: int, db: Session = Depends(get_db)):
    db.query(PatrolParameter).filter(PatrolParameter.id == parameter_id).delete()
    db.commit()
    return {"success": True}


# Get value for a parameter given the patrol group, patrol, parameter type and parameter id
@app.get("/patrol_parameters/{patrol_group}/{patrol:path}/{type:path}/{parameter_id}")
def get_patrol_parameters(
    patrol_group: str,
    patrol: str,
    type: str,
    parameter_id: str,
    db: Session = Depends(get_db),
):
    parameter = (
        db.query(PatrolParameter)
        .join(PatrolSetting, PatrolParameter.setting_id == PatrolSetting.id)
        .join(Patrol, PatrolSetting.patrol_id == Patrol.id)
        .join(PatrolGroup, Patrol.group_id == PatrolGroup.id)
        .filter(
            PatrolGroup.name == patrol_group,
            Patrol.name == patrol,
            PatrolParameter.type == type,
            PatrolParameter.parameter_id == parameter_id,
        )
        .first()
    )

    return parameter.__dict__ if parameter else {}


# Update patrol parameters for a patrol group and patrol
@app.post("/patrol_parameters")
def update_patrol_parameters(
    patrol_params: PatrolParameterRequest, db: Session = Depends(get_db)
):
    # Check if patrol group exists
    patrol_group = (
        db.query(PatrolGroup).filter_by(name=patrol_params.patrol_group).first()
    )
    if not patrol_group:
        patrol_group = PatrolGroup(name=patrol_params.patrol_group)
        db.add(patrol_group)
        db.commit()

    # Check if patrol exists
    patrol = (
        db.query(Patrol)
        .filter_by(name=patrol_params.patrol, group_id=patrol_group.id)
        .first()
    )
    if not patrol:
        patrol = Patrol(name=patrol_params.patrol, group_id=patrol_group.id)
        db.add(patrol)
        db.commit()

    # Check if patrol settings exist
    patrol_setting = db.query(PatrolSetting).filter_by(patrol_id=patrol.id).first()
    if not patrol_setting:
        patrol_setting = PatrolSetting(patrol_id=patrol.id)
        db.add(patrol_setting)
        db.commit()

    # Check if the parameter exists
    existing_parameter = (
        db.query(PatrolParameter)
        .filter_by(
            parameter_id=patrol_params.parameter_id,
            setting_id=patrol_setting.id,
            type=patrol_params.type,
        )
        .first()
    )
    if existing_parameter:
        # Update existing parameter
        existing_parameter.value = patrol_params.value
        existing_parameter.is_active = patrol_params.is_active
        existing_parameter.type = patrol_params.type
    else:
        # Create new parameter
        new_parameter = PatrolParameter(
            parameter_id=patrol_params.parameter_id,
            setting_id=patrol_setting.id,
            value=patrol_params.value,
            type=patrol_params.type,
            is_active=patrol_params.is_active,
        )
        db.add(new_parameter)

    db.commit()
    return {"success": True}


# Get patrol settings for a patrol id
@app.get("/patrol_settings/{patrol}")
def get_patrol_settings(
    patrol: str,
    db: Session = Depends(get_db),
):
    patrol_settings = (
        db.query(PatrolSetting).filter(PatrolSetting.patrol_id == patrol).first()
    )
    return patrol_settings.__dict__ if patrol_settings else {}


# Get patrol settings for a patrol group name and patrol name
@app.get("/patrol_settings/{patrol_group:path}/{patrol:path}")
def get_patrol_settings(
    patrol_group: str,
    patrol: str,
    db: Session = Depends(get_db),
):
    patrol_settings = (
        db.query(PatrolSetting)
        .join(Patrol, PatrolSetting.patrol_id == Patrol.id)
        .join(PatrolGroup, Patrol.group_id == PatrolGroup.id)
        .filter(PatrolGroup.name == patrol_group, Patrol.name == patrol)
        .first()
    )

    return patrol_settings.__dict__ if patrol_settings else {}


# Update patrol settings for a patrol group and patrol
@app.post("/patrol_settings")
def update_patrol_settings(
    request: PatrolSettingRequest, db: Session = Depends(get_db)
):
    patrol_group = db.query(PatrolGroup).filter_by(id=request.patrol_group).first()
    if not patrol_group:
        patrol_group = PatrolGroup(name=request.patrol_group)
        db.add(patrol_group)
        db.commit()

    patrol = (
        db.query(Patrol).filter_by(id=request.patrol, group_id=patrol_group.id).first()
    )
    if not patrol:
        patrol = Patrol(name=request.patrol, group_id=patrol_group.id)
        db.add(patrol)
        db.commit()

    patrol_setting = db.query(PatrolSetting).filter_by(patrol_id=patrol.id).first()
    if patrol_setting:
        patrol_setting.assigned_to_person = request.assigned_to_person
        patrol_setting.alerting = request.alerting
        patrol_setting.silenced_until = request.silenced_until
    else:
        patrol_setting = PatrolSetting(
            assigned_to_person=request.assigned_to_person,
            alerting=request.alerting,
            silenced_until=request.silenced_until,
            patrol_id=patrol.id,
        )
        db.add(patrol_setting)

    db.commit()
    return {"success": True}


# Set all parameters to inactive for a patrol group and patrol
@app.post("/reset_parameters")
def reset_parameters(
    request: PatrolResetParametersRequest, db: Session = Depends(get_db)
):
    patrol_group = db.query(PatrolGroup).filter_by(name=request.patrol_group).first()
    if not patrol_group:
        patrol_group = PatrolGroup(name=request.patrol_group)
        db.add(patrol_group)
        db.commit()

    patrol = (
        db.query(Patrol)
        .filter_by(name=request.patrol, group_id=patrol_group.id)
        .first()
    )
    if not patrol:
        patrol = Patrol(name=request.patrol, group_id=patrol_group.id)
        db.add(patrol)
        db.commit()

    patrol_setting = db.query(PatrolSetting).filter_by(patrol_id=patrol.id).first()
    if patrol_setting:
        db.query(PatrolParameter).filter(
            PatrolParameter.setting_id == patrol_setting.id
        ).update({PatrolParameter.is_active: False})
        db.commit()

    return {"success": True}


# Get summary of all the latest patrols runs
@app.get("/summary")
def summary(db: Session = Depends(get_db)):
    result = db.execute(
        text(
            """
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as success,
            SUM(CASE WHEN status = 'failure' THEN 1 ELSE 0 END) as failure,
            SUM(CASE WHEN status = 'skipped' THEN 1 ELSE 0 END) as skipped,
            SUM(CASE WHEN severity = 'critical' THEN 1 ELSE 0 END) as critical,
            SUM(CASE WHEN severity = 'warning' THEN 1 ELSE 0 END) as warning,
            SUM(CASE WHEN severity = 'info' THEN 1 ELSE 0 END) as info
        FROM patrol_runs
        JOIN patrols ON patrols.id = patrol_runs.patrol_id
        WHERE patrol_runs.id IN (
            SELECT MAX(id) 
            FROM patrol_runs 
            GROUP BY patrol_id
        )
    """
        )
    ).fetchone()
    return {
        "total": result[0],
        "success": result[1],
        "failure": result[2],
        "skipped": result[3],
        "critical": result[4],
        "warning": result[5],
        "info": result[6],
    }


# Get a stored data profile
@app.get("/profile/{profile_id}")
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = db.query(PatrolProfile).filter_by(id=profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found.")

    return profile.__dict__


# Store a data profile
@app.post("/profile")
def save_profile(request: PatrolProfileCreate, db: Session = Depends(get_db)):
    patrol_group = db.query(PatrolGroup).filter_by(name=request.patrol_group).first()
    if not patrol_group:
        patrol_group = PatrolGroup(name=request.patrol_group)
        db.add(patrol_group)
        db.commit()

    patrol = (
        db.query(Patrol)
        .filter_by(name=request.patrol, group_id=patrol_group.id)
        .first()
    )
    if not patrol:
        patrol = Patrol(name=request.patrol, group_id=patrol_group.id)
        db.add(patrol)
        db.commit()

    patrol_profile = PatrolProfile(
        patrol_id=patrol.id,
        report=request.report,
        time=request.time,
        format=request.format,
    )
    db.add(patrol_profile)
    db.commit()

    return {"success": True}


@app.get("/config.json")
def config():
    return JSONResponse(json.load(open(os.path.join(static_dir_path, "./config.json"))))


@app.get("/{full_path:path}")
def serve_static(full_path: str):
    return HTMLResponse(open(os.path.join(static_dir_path, "./index.html")).read())
