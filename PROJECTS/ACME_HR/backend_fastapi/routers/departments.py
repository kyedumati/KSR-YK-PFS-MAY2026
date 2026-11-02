from fastapi import APIRouter



router = APIRouter(prefix="/departments", tags=["deptartments"])

@router.get("/departments")
def departments():
    return "departments"