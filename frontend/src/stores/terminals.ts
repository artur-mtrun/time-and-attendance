import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { Terminal, CreateTerminalData, UpdateTerminalData } from '../types/terminal.js';
import { terminalService } from '../services/terminals.js';

export const useTerminalsStore = defineStore('terminals', () => {
    const terminals = ref<Terminal[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    async function fetchTerminals() {
        loading.value = true;
        error.value = null;
        try {
            terminals.value = await terminalService.getTerminals();
        } catch (e) {
            error.value = 'Nie udało się pobrać listy czytników';
            console.error(e);
        } finally {
            loading.value = false;
        }
    }

    async function createTerminal(data: CreateTerminalData) {
        try {
            const terminal = await terminalService.createTerminal(data);
            terminals.value.push(terminal);
            return true;
        } catch (e) {
            error.value = 'Nie udało się utworzyć czytnika';
            console.error(e);
            return false;
        }
    }

    async function updateTerminal(id: number, data: UpdateTerminalData) {
        try {
            const updatedTerminal = await terminalService.updateTerminal(id, data);
            const index = terminals.value.findIndex(t => t.id === id);
            if (index !== -1) {
                terminals.value[index] = updatedTerminal;
            }
            return true;
        } catch (e) {
            error.value = 'Nie udało się zaktualizować czytnika';
            console.error(e);
            return false;
        }
    }

    async function deleteTerminal(id: number) {
        try {
            await terminalService.deleteTerminal(id);
            terminals.value = terminals.value.filter(t => t.id !== id);
            return true;
        } catch (e) {
            error.value = 'Nie udało się usunąć czytnika';
            console.error(e);
            return false;
        }
    }

    async function syncTerminal(id: number) {
        try {
            await terminalService.syncTerminal(id);
            // Odśwież dane czytnika po synchronizacji
            await fetchTerminals();
            return true;
        } catch (e) {
            error.value = 'Nie udało się zsynchronizować czytnika';
            console.error(e);
            return false;
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