from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.db import get_session_factory
from app.routers import attendance, auth, employees, leave, operations, organization

app = FastAPI(title="AcmeHR API")
app.include_router(auth.router)
app.include_router(organization.router)
app.include_router(employees.router)
app.include_router(leave.router)
app.include_router(attendance.router)
app.include_router(operations.router)


@app.middleware("http")
async def session_middleware(request: Request, call_next):
    session = get_session_factory()()
    request.state.session = session
    try:
        response = await call_next(request)
        if response.status_code >= 400:
            session.rollback()
        else:
            session.commit()
        return response
    except IntegrityError:
        session.rollback()
        return JSONResponse(status_code=409, content={"detail": "That record conflicts with an existing one."})
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


@app.get("/")
def health() -> dict[str, str]:
    return {"status": "ok"}
