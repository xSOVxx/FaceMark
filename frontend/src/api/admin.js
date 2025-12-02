import api from './axios';

export const getProfessors = async () => {
    const response = await api.get('/profesores/');
    return response.data;
};

export const createProfessor = async (professorData) => {
    const response = await api.post('/profesores/', professorData);
    return response.data;
};

export const getStudents = async () => {
    const response = await api.get('/alumnos/');
    return response.data;
};

export const createStudent = async (studentData) => {
    const response = await api.post('/alumnos/', studentData);
    return response.data;
};

export const getClasses = async () => {
    const response = await api.get('/clases/');
    return response.data;
};

export const createClass = async (classData) => {
    const response = await api.post('/clases/', classData);
    return response.data;
};

export const assignStudentToClass = async (classId, studentId) => {
    const response = await api.post(`/clases/${classId}/assign-student`, { alumno_id: studentId });
    return response.data;
};
