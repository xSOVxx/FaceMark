from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import admin, professors, students, classes, attendance, auth

app = FastAPI(title="FaceMark API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(professors.router)
app.include_router(students.router)
app.include_router(classes.router)
app.include_router(attendance.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to FaceMark API"}
