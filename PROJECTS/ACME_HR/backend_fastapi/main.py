from fastapi import FastAPI
from routers import employees, departments


app = FastAPI(title="Acme HR Backend API")

app.include_router(employees.router)
app.include_router(departments.router)

@app.get("/")
def home():
    return {"Hello": "World, welcome to Acme HR Backend API"}







