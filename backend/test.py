from app.db.database import SessionLocal
from app.models.project import Project

db = SessionLocal()

project = db.query(Project).filter(Project.id == 2).first()

print(project.project_directory)