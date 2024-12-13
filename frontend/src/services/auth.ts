import axios from 'axios';
import type { LoginRequest, LoginResponse, User } from '../types/auth.js';

const API_URL = 'http://localhost:8000/api';

export const authService = {
    async login(data: LoginRequest): Promise<LoginResponse> {
        const formData = new URLSearchParams();
        formData.append('username', data.username);
        formData.append('password', data.password);

        const response = await axios.post<LoginResponse>(`${API_URL}/auth/login`, formData, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            withCredentials: false
        });
        
        localStorage.setItem('token', response.data.access_token);
        return response.data;
    },

    async getCurrentUser(): Promise<User> {
        const token = localStorage.getItem('token');
        const response = await axios.get<User>(`${API_URL}/auth/me`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return response.data;
    },

    logout(): void {
        localStorage.removeItem('token');
    },

    getToken(): string | null {
        return localStorage.getItem('token');
    }
}; 