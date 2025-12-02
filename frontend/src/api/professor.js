import api from './axios';

export const getMyClasses = async () => {
    // In a real app, filter by logged-in professor ID.
    // For now, fetching all classes or assuming backend filters based on token (if implemented)
    // Since our backend /clases/ returns all, we might need to filter client-side or update backend.
    const response = await api.get('/clases/');
    return response.data;
};

export const markAttendance = async (classId, professorId, imageFile) => {
    const formData = new FormData();
    formData.append('clase_id', classId);
    formData.append('profesor_id', professorId);
    formData.append('file', imageFile);

    const response = await api.post('/asistencia/marcar', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};
