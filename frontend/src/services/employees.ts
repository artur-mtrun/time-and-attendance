import axios from '../plugins/axios.js';
import type { Employee, CreateEmployeeData, UpdateEmployeeData } from '../types/employee.js';

export const employeeService = {
    async getEmployees(): Promise<Employee[]> {
        const response = await axios.get<Employee[]>('/employees');
        return response.data;
    },

    async createEmployee(data: CreateEmployeeData): Promise<Employee> {
        const response = await axios.post<Employee>('/employees', data);
        return response.data;
    },

    async updateEmployee(id: number, data: UpdateEmployeeData): Promise<Employee> {
        const response = await axios.put<Employee>(`/employees/${id}`, data);
        return response.data;
    },

    async deleteEmployee(id: number): Promise<void> {
        await axios.delete(`/employees/${id}`);
    },

    async fetchFromMainTerminal(): Promise<Employee[]> {
        const response = await axios.post<Employee[]>('/Employee/get-all');
        return response.data;
    },

    async syncFromMainTerminal(): Promise<void> {
        await this.checkSync();
    },

    async checkSync() {
        const response = await axios.post('/employees/sync-from-main');
        return response.data;
    },

    async confirmSync() {
        const response = await axios.post('/employees/sync-from-main/confirm');
        return response.data;
    },

    async sendToTerminals(data: { terminalIds: number[], employeeIds: number[] }) {
        const response = await axios.post('/api/employees/send-to-terminals', data);
        return response.data;
    }
}; 