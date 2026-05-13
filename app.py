from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks, Request, Response
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
import os
import shutil
import base64
import threading
import time
from datetime import datetime
from typing import Optional
from services.campaign import CampaignEngine
from infra.config import Config
from infra.logger import logger
from infra.database import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start scheduler thread
    threading.Thread(target=scheduler_worker, daemon=True).start()
    yield

app = FastAPI(title="MailForge Web", lifespan=lifespan)

# Ensure directories exist
os.makedirs("static", exist_ok=True)
os.makedirs("temp", exist_ok=True)
os.makedirs("data", exist_ok=True)

# Mount static files for HTML/CSS/JS
app.mount("/ui", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

@app.get("/api/config")
async def get_config():
    return {
        "DISPLAY_NAME": Config.DISPLAY_NAME or "",
        "SENDER_EMAIL": Config.SENDER_EMAIL or "",
        "SMTP_HOST": Config.SMTP_HOST or "smtp.gmail.com",
        "SMTP_PORT": Config.SMTP_PORT or 587,
        "RATE_LIMIT": Config.RATE_LIMIT or 1.0,
        "RETRY_COUNT": Config.RETRY_COUNT or 3
    }

@app.post("/api/config")
async def update_config(
    display_name: str = Form(...),
    sender_email: str = Form(...),
    password: Optional[str] = Form(None),
    smtp_host: str = Form(...),
    smtp_port: int = Form(...),
    rate_limit: float = Form(...),
    retry_count: int = Form(...)
):
    try:
        # Update .env file
        env_lines = []
        if os.path.exists(".env"):
            with open(".env", "r") as f:
                env_lines = f.readlines()
        
        config_map = {
            "DISPLAY_NAME": display_name,
            "SENDER_EMAIL": sender_email,
            "SMTP_HOST": smtp_host,
            "SMTP_PORT": str(smtp_port),
            "RATE_LIMIT": str(rate_limit),
            "RETRY_COUNT": str(retry_count)
        }
        if password:
            config_map["PASSWORD"] = password

        new_lines = []
        processed_keys = set()
        for line in env_lines:
            if "=" in line:
                key = line.split("=")[0].strip()
                if key in config_map:
                    new_lines.append(f"{key}={config_map[key]}\n")
                    processed_keys.add(key)
                    continue
            new_lines.append(line)
        
        for key, value in config_map.items():
            if key not in processed_keys:
                new_lines.append(f"{key}={value}\n")

        with open(".env", "w") as f:
            f.writelines(new_lines)
        
        # Update Config class attributes directly for the current session
        Config.DISPLAY_NAME = display_name
        Config.SENDER_EMAIL = sender_email
        if password:
            Config.PASSWORD = password
        Config.SMTP_HOST = smtp_host
        Config.SMTP_PORT = smtp_port
        Config.RATE_LIMIT = rate_limit
        Config.RETRY_COUNT = retry_count

        return {"message": "Configuration saved successfully"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Error saving config: {str(e)}"})

@app.post("/api/run-campaign")
async def run_campaign(
    background_tasks: BackgroundTasks,
    csv_file: UploadFile = File(...),
    template_file: UploadFile = File(...),
    campaign_name: Optional[str] = Form(None),
    rate_limit: Optional[float] = Form(None),
    scheduled_at: Optional[str] = Form(None)
):
    print(f"DEBUG: run_campaign hit! Name: {campaign_name}, Rate: {rate_limit}")
    try:
        # Save files to temp directory
        csv_path = f"temp/{csv_file.filename}"
        template_path = f"temp/{template_file.filename}"
        
        with open(csv_path, "wb") as buffer:
            shutil.copyfileobj(csv_file.file, buffer)
        
        with open(template_path, "wb") as buffer:
            shutil.copyfileobj(template_file.file, buffer)
        
        with open(template_path, "r", encoding="utf-8") as f:
            template_str = f.read()

        if scheduled_at:
            # Save as scheduled campaign
            db.create_campaign(
                name=campaign_name or f"Scheduled_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                subject="Bulk Email",
                status='scheduled',
                scheduled_at=scheduled_at,
                csv_path=csv_path,
                template_str=template_str
            )
            return {"message": f"Campaign scheduled for {scheduled_at}"}
        else:
            # Run immediately
            def start_campaign_task():
                try:
                    logger.info(f"Starting CampaignEngine task for: {campaign_name}")
                    engine = CampaignEngine(
                        csv_path=csv_path, 
                        template_str=template_str, 
                        campaign_name=campaign_name,
                        rate_limit=rate_limit
                    )
                    logger.info("Engine initialized, starting run...")
                    engine.run()
                except Exception as e:
                    logger.error(f"Web Campaign Error: {e}")
                    print(f"DEBUG CAMPAIGN ERROR: {e}")

            background_tasks.add_task(start_campaign_task)
            return {"message": "Campaign started successfully!"}
            
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Failed to start campaign: {str(e)}"})

# Tracking Endpoints
@app.get("/api/track/open/{recipient_id}")
async def track_open(recipient_id: str, request: Request):
    try:
        logger.info(f"Email opened by recipient: {recipient_id}")
        db.log_event(
            recipient_id=recipient_id,
            event_type="open",
            ip=request.client.host,
            ua=request.headers.get("user-agent")
        )
    except Exception as e:
        logger.error(f"Tracking open failed: {e}")
    
    # Return 1x1 transparent GIF
    pixel_data = base64.b64decode("R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7")
    return Response(content=pixel_data, media_type="image/gif")

@app.get("/api/track/click/{recipient_id}")
async def track_click(recipient_id: str, url: str, request: Request):
    try:
        db.log_event(
            recipient_id=recipient_id,
            event_type="click",
            url=url,
            ip=request.client.host,
            ua=request.headers.get("user-agent")
        )
    except Exception as e:
        logger.error(f"Tracking click failed: {e}")
    
    return RedirectResponse(url=url)

@app.get("/api/analytics")
async def get_analytics():
    try:
        latest = db.get_latest_campaign()
        if not latest:
            return {"message": "No campaigns found", "stats": None}
        
        stats = db.get_campaign_stats(latest["id"])
        ab_stats = db.get_ab_stats(latest["id"])
        
        return {
            "campaign_name": latest["name"],
            "campaign_id": latest["id"],
            "stats": stats,
            "ab_stats": ab_stats
        }
    except Exception as e:
        logger.error(f"Analytics error: {str(e)}")
        print(f"DEBUG ANALYTICS ERROR: {e}")
        return JSONResponse(status_code=500, content={"message": f"Analytics error: {str(e)}"})

@app.get("/api/logs")
async def get_logs():
    if not os.path.exists("logs/app.log"):
        return {"logs": ["No logs available yet."]}
    try:
        with open("logs/app.log", "r") as f:
            lines = f.readlines()
            # Return last 50 lines, cleaned
            return {"logs": [line.strip() for line in lines[-50:]]}
    except Exception as e:
        return {"logs": [f"Error reading logs: {str(e)}"]}

# Scheduler Thread
def scheduler_worker():
    logger.info("Scheduler worker started")
    while True:
        try:
            due_campaigns = db.get_due_campaigns()
            for campaign in due_campaigns:
                logger.info(f"Starting scheduled campaign: {campaign['name']}")
                engine = CampaignEngine(
                    csv_path=campaign['csv_path'],
                    template_str=campaign['template_str'],
                    campaign_name=campaign['name'],
                    campaign_id=campaign['id']
                )
                # Run in a separate thread to not block the scheduler loop
                threading.Thread(target=engine.run, daemon=True).start()
        except Exception as e:
            logger.error(f"Scheduler error: {e}")
        time.sleep(30) # Check every 30 seconds

# Removed deprecated startup_event

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
