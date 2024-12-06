import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { Terminal, CreateTerminalData } from '@/types/terminal.js';
import { terminalService } from '@/services/terminals.js';

export const useTerminalsStore = defineStore('terminals', () => {
    const terminals = ref<Terminal[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    async function fetchTerminals() {
        loading.value = true;
        error.value = null;
        try {
            terminals.value = await terminalService.getTerminals();
        } catch (err: any) {
            error.value = err.response?.data?.detail || 'Nie udało się pobrać listy czytników';
            throw err;
        } finally {
            loading.value = false;
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

    async function syncTerminal(id: number) {
        loading.value = true;
        error.value = null;
        try {
            await terminalService.syncTerminal(id);
            await fetchTerminals(); // Odświeżamy listę po synchronizacji
        } catch (err: any) {
            error.value = err.response?.data?.detail || 'Nie udało się zsynchronizować czytnika';
            throw err;
        } finally {
            loading.value = false;
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
        syncTerminal
    };
}); 