CABROS para correrlo 

descarguen las dependencias escribiendo en terminal
pip install -r requirements.txt


despues creen la base de datos en mariadb, si no usan, modifquen init_db.py  para mysql
despues corrarn el archivo init_db.py

despues de eso ejecuten test_api.py para verificar si funcionan los endpoints

si ya funciona todo corran el proyecto
en el backend escriban en el terminal
cd backend/face_api
.\venv\Scripts\activate

debe salir ahora (venv)mas cosas
despues escriban uvicorn main:app --reload

despues corran el frontend



























CREATE DATABASE asistencia_control;
USE asistencia_control;

CREATE TABLE administradores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE profesores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE alumnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    codigo VARCHAR(50) NOT NULL UNIQUE,
    embedding LONGTEXT,  -- o JSON si prefieres
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE clases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    profesor_id INT NOT NULL,
    FOREIGN KEY (profesor_id) REFERENCES profesores(id)
);

CREATE TABLE clase_alumnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    clase_id INT NOT NULL,
    alumno_id INT NOT NULL,
    UNIQUE(clase_id, alumno_id),
    FOREIGN KEY (clase_id) REFERENCES clases(id),
    FOREIGN KEY (alumno_id) REFERENCES alumnos(id)
);

CREATE TABLE asistencias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    clase_id INT NOT NULL,
    profesor_id INT NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL DEFAULT CURRENT_TIME(),
    FOREIGN KEY (clase_id) REFERENCES clases(id),
    FOREIGN KEY (profesor_id) REFERENCES profesores(id)
);

CREATE TABLE asistencia_detalle (
    id INT AUTO_INCREMENT PRIMARY KEY,
    asistencia_id INT NOT NULL,
    alumno_id INT NOT NULL,
    presente TINYINT(1) DEFAULT 1,
    FOREIGN KEY (asistencia_id) REFERENCES asistencias(id),
    FOREIGN KEY (alumno_id) REFERENCES alumnos(id)
);

SELECT *FROM administradores

