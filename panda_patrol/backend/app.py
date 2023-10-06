from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from panda_patrol.backend.database.models import *

app = FastAPI()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/summary/{user_id}")
def get_summary(user_id: str, db: Session = Depends(get_db)):
    # Subquery for latest runs
    latest_runs = (
        db.query(PatrolRun.patrol_id, func.max(PatrolRun.id).label("run_id"))
        .group_by(PatrolRun.patrol_id)
        .subquery()
    )

    # Main query
    summary = (
        db.query(
            func.count().label("total"),
            func.sum(func.case([(PatrolRun.status == "success", 1)], else_=0)).label(
                "success"
            ),
            func.sum(func.case([(PatrolRun.status == "failure", 1)], else_=0)).label(
                "failure"
            ),
            func.sum(func.case([(PatrolRun.status == "skipped", 1)], else_=0)).label(
                "skipped"
            ),
            func.sum(func.case([(PatrolRun.severity == "critical", 1)], else_=0)).label(
                "critical"
            ),
            func.sum(func.case([(PatrolRun.severity == "warning", 1)], else_=0)).label(
                "warning"
            ),
            func.sum(func.case([(PatrolRun.severity == "info", 1)], else_=0)).label(
                "info"
            ),
        )
        .join(Patrol, Patrol.id == PatrolRun.patrol_id)
        .filter(and_(Patrol.user_id == user_id, PatrolRun.id.in_(latest_runs)))
        .first()
    )

    return {
        "total": summary.total,
        "success": summary.success,
        "failure": summary.failure,
        "skipped": summary.skipped,
        "critical": summary.critical,
        "warning": summary.warning,
        "info": summary.info,
    }
