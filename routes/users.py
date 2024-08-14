from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from sqlmodel import Session, select, func
from utils.auth import get_current_active_client, verify_password, hash_password
from database import get_session
from models import User, SubscriptionPlan, Payment, Notification, Files, DataAnalysis, Visualization
from datetime import datetime
from utils.analysis import insights
import mimetypes
import os
import shutil
from utils.automate_graph import create_visuals
from PIL import Image, ImageTk
import io
from schemas.users import UserUpdate, PasswordChange

users_router = APIRouter()

MAX_TRIAL_USES = 7
UPLOAD_DIRECTORY = './uploads'
ALLOWED_MIMETYPES = {
    "text/csv",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-excel"
}

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

def check_and_update_trial_usage(user: User, session: Session) -> bool:
    if user.subscription_plan_id is None and user.trial_uses < MAX_TRIAL_USES:
        user.trial_uses += 1
        session.commit()
        return True
    return user.subscription_plan_id is not None

@users_router.get("/user/info")
async def read_users_me(current_user: User = Depends(get_current_active_client)):
    return current_user

@users_router.put("/user/info")
async def update_user_info(
    user_update: UserUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_client)
):
    current_user.email = user_update.email
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return {"message": "User information updated successfully"}

@users_router.post("/user/change-password")
async def change_password(
    password_change: PasswordChange,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_client)
):
    if not verify_password(password_change.current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect current password")
    
    current_user.password_hash = hash_password(password_change.new_password)
    session.add(current_user)
    session.commit()
    return {"message": "Password changed successfully"}

@users_router.post("/me/uploadfile")
async def upload_file(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_client)
):
    if not check_and_update_trial_usage(current_user, session):
        raise HTTPException(status_code=403, detail="Trial limit reached. Please upgrade your plan.")

    mimetype, _ = mimetypes.guess_type(file.filename)
    if mimetype not in ALLOWED_MIMETYPES:
        raise HTTPException(status_code=400, detail="Only CSV or Excel files are allowed.")
    
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    
    existing_file = session.exec(select(Files).where(Files.file_name == file.filename, Files.user_id == current_user.user_id)).first()
    if existing_file:
        raise HTTPException(status_code=400, detail="File already exists")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    new_file = Files(
        user_id=current_user.user_id,
        file_name=file.filename,
        file_path=file_path,
        status="uploaded"
    )
    session.add(new_file)
    session.commit()
    session.refresh(new_file)
    
    return {"message": "File added successfully.", "filename": file.filename}

@users_router.get("/user/getfiles")
async def get_all_files(session: Session = Depends(get_session), 
                        current_user: User = Depends(get_current_active_client)):
    files = session.exec(select(Files.file_name).where(Files.user_id == current_user.user_id)).all()
    return [{"filename": file_name} for file_name in files]

@users_router.post("/user/analysis/{file_name}")
async def analysis_create(
    file_name: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_client),
):
    if not check_and_update_trial_usage(current_user, session):
        raise HTTPException(status_code=403, detail="Trial limit reached. Please upgrade your plan.")

    file = session.exec(select(Files).where(Files.file_name == file_name, Files.user_id == current_user.user_id)).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    summary = insights(file.file_path)
    new_analysis = DataAnalysis(file_id=file.file_id, summary_statistics=summary)
    session.add(new_analysis)
    session.commit()
    session.refresh(new_analysis)
    return new_analysis

@users_router.get("/user/analysis")
async def get_analyzed_files(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_client)
):
    analyzed_files = session.exec(
        select(Files.file_name, DataAnalysis.analysis_id, DataAnalysis.summary_statistics, DataAnalysis.analysis_date)
        .join(DataAnalysis, Files.file_id == DataAnalysis.file_id)
        .where(Files.user_id == current_user.user_id)
    ).all()

    return [
        {
            "file_name": file_name,
            "analysis_id": analysis_id,
            "summary": summary_statistics[:100] + "..." if len(summary_statistics) > 100 else summary_statistics,
            "created_at": analysis_date
        }
        for file_name, analysis_id, summary_statistics, analysis_date in analyzed_files
    ]

@users_router.get("/user/analysis/{analysis_id}")
async def get_full_analysis(
    analysis_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_client)
):
    analysis = session.exec(
        select(DataAnalysis, Files.file_name)
        .join(Files, DataAnalysis.file_id == Files.file_id)
        .where(DataAnalysis.analysis_id == analysis_id, Files.user_id == current_user.user_id)
    ).first()

    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    analysis, file_name = analysis
    return {
        "analysis_id": analysis.analysis_id,
        "file_name": file_name,
        "summary_statistics": analysis.summary_statistics,
        "created_at": analysis.analysis_date
    }

@users_router.post('/user/visuals/{file_name}')
async def visualisation_create(
    file_name: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_client),
):
    if not check_and_update_trial_usage(current_user, session):
        raise HTTPException(status_code=403, detail="Trial limit reached. Please upgrade your plan.")

    file = session.exec(select(Files).where(Files.file_name == file_name, Files.user_id == current_user.user_id)).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    analysis = session.exec(select(DataAnalysis).where(DataAnalysis.file_id == file.file_id)).first()
    if not analysis:
        analysis = await analysis_create(file_name, session, current_user)

    existing_visualizations = session.exec(select(Visualization).where(Visualization.analysis_id == analysis.analysis_id)).all()
    
    if existing_visualizations:
        return {
            "message": "Existing visualizations found",
            "visualizations": [
                {
                    "visualization_id": viz.visualization_id,
                    "analysis_id": viz.analysis_id,
                    "visualization_type": viz.visualization_type,
                    "parameters": viz.parameters,
                    "image_path": viz.image_path,
                    "created_at": viz.created_at.isoformat() if viz.created_at else None
                }
                for viz in existing_visualizations
            ]
        }

    image_paths = create_visuals(file.file_path, current_user.username)

    if isinstance(image_paths, str):
        raise HTTPException(status_code=500, detail=image_paths)

    db_visualizations = []
    for image_path in image_paths:
        new_viz = Visualization(
            analysis_id=analysis.analysis_id,
            visualization_type=os.path.basename(image_path).split('.')[0],
            parameters="Generated by AI",
            image_path=image_path
        )
        session.add(new_viz)
        db_visualizations.append(new_viz)
    
    session.commit()
    
    for viz in db_visualizations:
        session.refresh(viz)

    return {
        "message": "New visualizations created successfully",
        "visualizations": [
            {
                "visualization_id": viz.visualization_id,
                "analysis_id": viz.analysis_id,
                "visualization_type": viz.visualization_type,
                "parameters": viz.parameters,
                "image_path": viz.image_path,
                "created_at": viz.created_at.isoformat() if viz.created_at else None
            }
            for viz in db_visualizations
        ]
    }

@users_router.get("/dashboard/file_count")
async def get_file_count(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_client)
):
    total_files, analyzed_files = session.exec(
        select(
            func.count(Files.file_id),
            func.count(DataAnalysis.analysis_id)
        )
        .outerjoin(DataAnalysis, Files.file_id == DataAnalysis.file_id)
        .where(Files.user_id == current_user.user_id)
    ).first()

    return {
        "total_files": total_files,
        "analyzed_files": analyzed_files
    }

@users_router.get("/dashboard/analysis_list")
async def get_analysis_list(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_client)
):
    analyses = session.exec(
        select(DataAnalysis.analysis_id, Files.file_name, DataAnalysis.analysis_date, DataAnalysis.summary_statistics)
        .join(Files, DataAnalysis.file_id == Files.file_id)
        .where(Files.user_id == current_user.user_id)
        .order_by(DataAnalysis.analysis_date.desc())
    ).all()

    return [
        {
            "analysis_id": analysis_id,
            "file_name": file_name,
            "created_at": analysis_date,
            "summary_statistics": summary_statistics
        }
        for analysis_id, file_name, analysis_date, summary_statistics in analyses
    ]

@users_router.get("/user/files/{filename}")
async def view_file(
    filename: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_client)
):
    file = session.exec(select(Files).where(Files.file_name == filename, Files.user_id == current_user.user_id)).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    with open(file.file_path, 'r') as f:
        contents = f.read()
    return {"filename": filename, "contents": contents}

@users_router.delete("/user/files/{filename}")
async def delete_file(
    filename: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_client)
):
    file = session.exec(select(Files).where(Files.file_name == filename, Files.user_id == current_user.user_id)).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    session.delete(file)
    session.commit()
    
    os.remove(file.file_path)
    
    return {"message": f"File {filename} deleted successfully"}

@users_router.get("/user/subscription")
async def get_user_subscription(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_client)
):
    if current_user.subscription_plan_id:
        subscription_plan = session.get(SubscriptionPlan, current_user.subscription_plan_id)
        if subscription_plan:
            return {
                "plan_name": subscription_plan.plan_name,
                "end_date": current_user.subscription_end_date
            }
    return {"plan_name": "Free", "end_date": None}