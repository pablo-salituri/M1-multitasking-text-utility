from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="Multitasking Text Utility (LEGACY API - see CLI)",
    description="This API is kept for compatibility. Preferred usage is CLI via run_query.py"
)

app.include_router(router)