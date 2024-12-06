<template>
    <div class="p-4">
        <div class="flex justify-between items-center mb-4">
            <h2 class="text-2xl font-bold">Lista czytników</h2>
            <button
                @click="showCreateModal = true"
                class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
            >
                Dodaj czytnik
            </button>
        </div>

        <div v-if="terminalsStore.loading" class="text-center py-4">
            Ładowanie...
        </div>

        <div v-else-if="terminalsStore.error" class="text-red-500 text-center py-4">
            {{ terminalsStore.error }}
        </div>

        <div v-else class="bg-white shadow-md rounded-lg">
            <table class="min-w-full">
                <thead>
                    <tr class="bg-gray-50">
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nr</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nazwa</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">IP</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Port</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ostatnia synchronizacja</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Akcje</th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="terminal in terminalsStore.terminals" :key="terminal.id">
                        <td class="px-6 py-4 whitespace-nowrap">{{ terminal.number }}</td>
                        <td class="px-6 py-4 whitespace-nowrap">{{ terminal.name }}</td>
                        <td class="px-6 py-4 whitespace-nowrap">{{ terminal.ip_address }}</td>
                        <td class="px-6 py-4 whitespace-nowrap">{{ terminal.port }}</td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span :class="terminal.is_active ? 'text-green-600' : 'text-red-600'">
                                {{ terminal.is_active ? 'Aktywny' : 'Nieaktywny' }}
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            {{ terminal.last_sync_at ? new Date(terminal.last_sync_at).toLocaleString() : 'Nigdy' }}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap space-x-2">
                            <button
                                @click="syncTerminal(terminal)"
                                class="text-blue-600 hover:text-blue-900"
                                :disabled="syncingTerminal === terminal.id"
                            >
                                {{ syncingTerminal === terminal.id ? 'Synchronizacja...' : 'Synchronizuj' }}
                            </button>
                            <button
                                @click="editTerminal(terminal)"
                                class="text-green-600 hover:text-green-900"
                            >
                                Edytuj
                            </button>
                            <button
                                @click="confirmDelete(terminal)"
                                class="text-red-600 hover:text-red-900"
                            >
                                Usuń
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Modal do tworzenia/edycji czytnika -->
        <div v-if="showCreateModal || editedTerminal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
            <div class="bg-white p-6 rounded-lg w-96">
                <h3 class="text-lg font-bold mb-4">
                    {{ editedTerminal ? 'Edytuj czytnik' : 'Dodaj czytnik' }}
                </h3>
                <form @submit.prevent="handleSubmit">
                    <div class="mb-4">
                        <label class="block text-sm font-medium text-gray-700">Numer czytnika</label>
                        <input
                            v-model.number="formData.number"
                            type="number"
                            required
                            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                        />
                    </div>
                    <div class="mb-4">
                        <label class="block text-sm font-medium text-gray-700">Nazwa</label>
                        <input
                            v-model="formData.name"
                            type="text"
                            required
                            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                        />
                    </div>
                    <div class="mb-4">
                        <label class="block text-sm font-medium text-gray-700">Adres IP</label>
                        <input
                            v-model="formData.ip_address"
                            type="text"
                            required
                            pattern="^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
                            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                        />
                    </div>
                    <div class="mb-4">
                        <label class="block text-sm font-medium text-gray-700">Port</label>
                        <input
                            v-model.number="formData.port"
                            type="number"
                            required
                            min="1"
                            max="65535"
                            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                        />
                    </div>
                    <div class="mb-4">
                        <label class="flex items-center">
                            <input
                                v-model="formData.is_active"
                                type="checkbox"
                                class="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                            />
                            <span class="ml-2 text-sm text-gray-600">Aktywny</span>
                        </label>
                    </div>
                    <div class="flex justify-end space-x-2">
                        <button
                            type="button"
                            @click="closeModal"
                            class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
                        >
                            Anuluj
                        </button>
                        <button
                            type="submit"
                            class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
                        >
                            {{ editedTerminal ? 'Zapisz' : 'Dodaj' }}
                        </button>
                    </div>
                </form>
            </div>
        </div>

        <!-- Modal potwierdzenia usunięcia -->
        <div v-if="terminalToDelete" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
            <div class="bg-white p-6 rounded-lg w-96">
                <h3 class="text-lg font-bold mb-4">Potwierdź usunięcie</h3>
                <p class="mb-4">Czy na pewno chcesz usunąć czytnik "{{ terminalToDelete.name }}"?</p>
                <div class="flex justify-end space-x-2">
                    <button
                        @click="terminalToDelete = null"
                        class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
                    >
                        Anuluj
                    </button>
                    <button
                        @click="deleteTerminal"
                        class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700"
                    >
                        Usuń
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useTerminalsStore } from '@/stores/terminals';
import type { Terminal } from '@/types/terminal';

const terminalsStore = useTerminalsStore();
const showCreateModal = ref(false);
const editedTerminal = ref<Terminal | null>(null);
const terminalToDelete = ref<Terminal | null>(null);
const syncingTerminal = ref<number | null>(null);

const formData = ref({
    number: 0,
    name: '',
    ip_address: '',
    port: 4370,
    is_active: true
});

onMounted(() => {
    terminalsStore.fetchTerminals();
});

function editTerminal(terminal: Terminal) {
    editedTerminal.value = terminal;
    formData.value = {
        number: terminal.number,
        name: terminal.name,
        ip_address: terminal.ip_address,
        port: terminal.port,
        is_active: terminal.is_active
    };
    showCreateModal.value = true;
}

function confirmDelete(terminal: Terminal) {
    terminalToDelete.value = terminal;
}

async function deleteTerminal() {
    if (terminalToDelete.value) {
        await terminalsStore.deleteTerminal(terminalToDelete.value.id);
        terminalToDelete.value = null;
    }
}

async function syncTerminal(terminal: Terminal) {
    syncingTerminal.value = terminal.id;
    try {
        await terminalsStore.syncTerminal(terminal.id);
    } finally {
        syncingTerminal.value = null;
    }
}

function closeModal() {
    showCreateModal.value = false;
    editedTerminal.value = null;
    formData.value = {
        number: 0,
        name: '',
        ip_address: '',
        port: 4370,
        is_active: true
    };
}

async function handleSubmit() {
    try {
        if (editedTerminal.value) {
            await terminalsStore.updateTerminal(editedTerminal.value.id, formData.value);
        } else {
            await terminalsStore.createTerminal(formData.value);
        }
        closeModal();
    } catch (error) {
        console.error('Failed to save terminal:', error);
    }
}
</script> 