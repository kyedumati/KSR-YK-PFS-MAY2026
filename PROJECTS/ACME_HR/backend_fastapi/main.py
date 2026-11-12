from fastapi import FastAPI
from routers import employees, departments, auth



app = FastAPI(title="Acme HR Backend API")

app.include_router(employees.router)
app.include_router(departments.router)
app.include_router(auth.router)

@app.get("/")
def home():
    return {"Hello": "World, welcome to Acme HR Backend API"}








