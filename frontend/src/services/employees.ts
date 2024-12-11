import axiosInstance from '../plugins/axios.js';
import type { Employee, CreateEmployeeData, UpdateEmployeeData } from '../types/employee.js';
import axios from 'axios';

export const employeeService = {
    async getEmployees(): Promise<Employee[]> {
        console.log('Wywołanie getEmployees');
        try {
            const response = await axiosInstance.get('/api/employees');
            console.log('Odpowiedź getEmployees:', response.data);
            return response.data;
        } catch (error) {
            console.error('Błąd getEmployees:', error);
            throw error;
        }
    },

    async createEmployee(data: CreateEmployeeData): Promise<Employee> {
        const response = await axiosInstance.post<Employee>('/api/employees', data);
        return response.data;
    },

    async updateEmployee(id: number, data: UpdateEmployeeData): Promise<Employee> {
        const response = await axiosInstance.put<Employee>(`/api/employees/${id}`, data);
        return response.data;
    },

    async deleteEmployee(id: number): Promise<void> {
        await axiosInstance.delete(`/api/employees/${id}`);
    },

    async fetchFromMainTerminal(): Promise<Employee[]> {
        const response = await axiosInstance.post<Employee[]>('/api/employees/get-all');
        return response.data;
    },

    async syncFromMainTerminal(): Promise<void> {
        await this.checkSync();
    },

    async checkSync() {
        console.log('Wywołanie checkSync');
        try {
            const response = await axiosInstance.post('/api/employees/sync-from-main');
            console.log('Odpowiedź checkSync:', response.data);
            return response.data;
        } catch (error) {
            if (axios.isAxiosError(error) && error.code === 'ECONNABORTED') {
                console.error('Timeout podczas synchronizacji');
                throw new Error('Przekroczono czas oczekiwania na odpowiedź serwera');
            }
            console.error('Błąd checkSync:', error);
            throw error;
        }
    },

    async confirmSync() {
        console.log('Wywołanie confirmSync');
        try {
            const response = await axiosInstance.post('/api/employees/sync-from-main/confirm');
            console.log('Odpowiedź confirmSync:', response.data);
            await this.getEmployees();
            return response.data;
        } catch (error) {
            console.error('Błąd confirmSync:', error);
            throw error;
        }
    },

    async sendToTerminals(data: { terminalIds: number[], employeeIds: number[] }) {
        const response = await axiosInstance.post('/api/employees/send-to-terminals', data);
        return response.data;
    },

    async fetchAttendanceFromTerminals(terminalIds: number[]) {
        console.log('Wywołanie fetchAttendanceFromTerminals');
        try {
            const response = await axiosInstance.post('/api/attendance-all/fetch-from-terminals', {
                terminal_ids: terminalIds
            });
            console.log('Odpowiedź fetchAttendanceFromTerminals:', response.data);
            return response.data;
        } catch (error: any) {
            console.error('Błąd fetchAttendanceFromTerminals:', error);
            if (error.response?.data?.detail) {
                throw new Error(error.response.data.detail);
            }
            throw error;
        }
    }
}; 