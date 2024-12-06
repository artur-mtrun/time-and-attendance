import axios from '../plugins/axios.js';
import type { Terminal, CreateTerminalData, UpdateTerminalData } from '../types/terminal.js';

export const terminalService = {
    async getTerminals(): Promise<Terminal[]> {
        try {
            const response = await axios.get<Terminal[]>('/api/terminals');
            return response.data;
        } catch (error) {
            console.error('Błąd getTerminals:', error);
            throw error;
        }
    },

    async createTerminal(data: CreateTerminalData): Promise<Terminal> {
        const response = await axios.post<Terminal>('/api/terminals', data);
        return response.data;
    },

    async updateTerminal(id: number, data: UpdateTerminalData): Promise<Terminal> {
        const response = await axios.put<Terminal>(`/api/terminals/${id}`, data);
        return response.data;
    },

    async deleteTerminal(id: number): Promise<void> {
        await axios.delete(`/api/terminals/${id}`);
    },

    async syncTerminal(id: number): Promise<void> {
        await axios.post(`/api/ terminals/${id}/sync`);
    }
}; 