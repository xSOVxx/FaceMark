from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, Boolean, Text, TIMESTAMP, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Admin(Base):
    __tablename__ = "administradores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(150), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    creado_en = Column(TIMESTAMP, server_default=func.now())

class Professor(Base):
    __tablename__ = "profesores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(150), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    creado_en = Column(TIMESTAMP, server_default=func.now())

    clases = relationship("Class", back_populates="profesor")
    asistencias = relationship("Attendance", back_populates="profesor")

class Student(Base):
    __tablename__ = "alumnos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    codigo = Column(String(50), unique=True, nullable=False)
    embedding = Column(Text, nullable=True) # Storing as JSON string or longtext
    creado_en = Column(TIMESTAMP, server_default=func.now())

    clases = relationship("ClassStudent", back_populates="alumno")
    asistencias_detalle = relationship("AttendanceDetail", back_populates="alumno")

class Class(Base):
    __tablename__ = "clases"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    profesor_id = Column(Integer, ForeignKey("profesores.id"), nullable=False)

    profesor = relationship("Professor", back_populates="clases")
    alumnos = relationship("ClassStudent", back_populates="clase")
    asistencias = relationship("Attendance", back_populates="clase")

class ClassStudent(Base):
    __tablename__ = "clase_alumnos"

    id = Column(Integer, primary_key=True, index=True)
    clase_id = Column(Integer, ForeignKey("clases.id"), nullable=False)
    alumno_id = Column(Integer, ForeignKey("alumnos.id"), nullable=False)

    clase = relationship("Class", back_populates="alumnos")
    alumno = relationship("Student", back_populates="clases")

    __table_args__ = (UniqueConstraint('clase_id', 'alumno_id', name='_clase_alumno_uc'),)

class Attendance(Base):
    __tablename__ = "asistencias"

    id = Column(Integer, primary_key=True, index=True)
    clase_id = Column(Integer, ForeignKey("clases.id"), nullable=False)
    profesor_id = Column(Integer, ForeignKey("profesores.id"), nullable=False)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, server_default=func.now(), nullable=False)

    clase = relationship("Class", back_populates="asistencias")
    profesor = relationship("Professor", back_populates="asistencias")
    detalles = relationship("AttendanceDetail", back_populates="asistencia")

class AttendanceDetail(Base):
    __tablename__ = "asistencia_detalle"

    id = Column(Integer, primary_key=True, index=True)
    asistencia_id = Column(Integer, ForeignKey("asistencias.id"), nullable=False)
    alumno_id = Column(Integer, ForeignKey("alumnos.id"), nullable=False)
    presente = Column(Boolean, default=True)

    asistencia = relationship("Attendance", back_populates="detalles")
    alumno = relationship("Student", back_populates="asistencias_detalle")
