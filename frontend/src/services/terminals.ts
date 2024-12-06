import axios from '../plugins/axios.js';
import type { Terminal, CreateTerminalData, UpdateTerminalData } from '../types/terminal.js';

export const terminalService = {
    async getTerminals(): Promise<Terminal[]> {
        const response = await axios.get<Terminal[]>('/terminals');
        return response.data;
    },

    async createTerminal(data: CreateTerminalData): Promise<Terminal> {
        const response = await axios.post<Terminal>('/terminals', data);
        return response.data;
    },

    async updateTerminal(id: number, data: UpdateTerminalData): Promise<Terminal> {
        const response = await axios.put<Terminal>(`/terminals/${id}`, data);
        return response.data;
    },

    async deleteTerminal(id: number): Promise<void> {
        await axios.delete(`/terminals/${id}`);
    },

    async syncTerminal(id: number): Promise<void> {
        await axios.post(`/terminals/${id}/sync`);
    }
}; 