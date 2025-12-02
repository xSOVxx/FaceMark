import api from './axios';

export const login = async (username, password) => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    const response = await api.post('/token', formData, {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    });
    return response.data;
};

export const getMe = async () => {
    // Implement an endpoint to get current user details if needed
    // For now, we decode token or store user info on login
    return {};
};
