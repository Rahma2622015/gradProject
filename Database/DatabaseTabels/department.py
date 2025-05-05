from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    name_arabic = Column(String, nullable=True)

    head_name = Column(String, nullable=True)
    head_name_arabic = Column(String, nullable=True)

    parent_id = Column(Integer, ForeignKey('departments.id'), nullable=True)

    parent = relationship("Department", remote_side=[id], backref="sub_departments")
    courses = relationship("Course", back_populates="department")
