import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { Terminal, CreateTerminalData, SyncResult } from '@/types/terminal.js';
import { terminalService } from '@/services/terminals.js';
import axios from 'axios';

export const useTerminalsStore = defineStore('terminals', () => {
    const terminals = ref<Terminal[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);
    const isSyncing = ref(false);

    async function fetchTerminals() {
        try {
            const data = await terminalService.getTerminals();
            terminals.value = data;
            return data;
        } catch (error) {
            console.error('Błąd podczas pobierania terminali:', error);
            throw error;
        }
    }

    async function createTerminal(data: CreateTerminalData) {
        loading.value = true;
        error.value = null;
        try {
            const newTerminal = await terminalService.createTerminal(data);
            terminals.value.push(newTerminal);
            return newTerminal;
        } catch (err: any) {
            error.value = err.response?.data?.detail || 'Nie udało się utworzyć czytnika';
            throw err;
        } finally {
            loading.value = false;
        }
    }

    async function updateTerminal(id: number, data: Partial<CreateTerminalData>) {
        loading.value = true;
        error.value = null;
        try {
            const updatedTerminal = await terminalService.updateTerminal(id, data);
            const index = terminals.value.findIndex(t => t.id === id);
            if (index !== -1) {
                terminals.value[index] = updatedTerminal;
            }
            return updatedTerminal;
        } catch (err: any) {
            error.value = err.response?.data?.detail || 'Nie udało się zaktualizować czytnika';
            throw err;
        } finally {
            loading.value = false;
        }
    }

    async function deleteTerminal(id: number) {
        loading.value = true;
        error.value = null;
        try {
            await terminalService.deleteTerminal(id);
            terminals.value = terminals.value.filter(t => t.id !== id);
        } catch (err: any) {
            error.value = err.response?.data?.detail || 'Nie udało się usunąć czytnika';
            throw err;
        } finally {
            loading.value = false;
        }
    }

    async function syncTerminal(id: number): Promise<SyncResult> {
        isSyncing.value = true;
        try {
            return await terminalService.syncTerminal(id);
        } catch (error) {
            throw error;
        } finally {
            isSyncing.value = false;
        }
    }

    async function fetchActiveTerminals() {
        try {
            const data = await terminalService.getActiveTerminals();
            terminals.value = data;
            return data;
        } catch (error) {
            console.error('Błąd podczas pobierania aktywnych terminali:', error);
            throw error;
        }
    }

    return {
        terminals,
        loading,
        error,
        fetchTerminals,
        createTerminal,
        updateTerminal,
        deleteTerminal,
        syncTerminal,
        fetchActiveTerminals,
        isSyncing,
    };
}); 