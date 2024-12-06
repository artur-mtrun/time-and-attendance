import axios from '../plugins/axios.js';
import type { User } from '../types/auth.js';

export interface CreateUserData {
    username: string;
    password: string;
    is_admin: boolean;
}

export interface UpdateUserData {
    password?: string;
    is_admin?: boolean;
}

export const userService = {
    async getUsers(): Promise<User[]> {
        const response = await axios.get<User[]>('/users');
        return response.data;
    },

    async createUser(userData: CreateUserData): Promise<User> {
        const response = await axios.post<User>('/users', userData);
        return response.data;
    },

    async updateUser(userId: number, userData: UpdateUserData): Promise<User> {
        const response = await axios.put<User>(`/users/${userId}`, userData);
        return response.data;
    },

    async deleteUser(userId: number): Promise<void> {
        await axios.delete(`/users/${userId}`);
    }
}; 