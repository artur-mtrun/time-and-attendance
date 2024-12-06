<template>
    <div class="p-4">
        <h1 class="text-2xl font-bold mb-6">Synchronizacja pracowników</h1>
        
        <!-- Alert Message -->
        <AlertMessage
            v-if="alertMessage"
            :message="alertMessage"
            :type="alertType"
            @close="alertMessage = ''"
            class="mb-4"
        />
        
        <!-- Przyciski akcji -->
        <div class="mb-6 flex space-x-4">
            <button 
                @click="handleSyncFromMain"
                :disabled="isFetching || employeesStore.loading"
                class="bg-green-500 text-white px-6 py-2 rounded hover:bg-green-600 disabled:bg-gray-300 disabled:cursor-not-allowed flex items-center"
            >
                <svg v-if="isFetching || employeesStore.loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>{{ (isFetching || employeesStore.loading) ? 'Pobieranie...' : 'Pobierz z terminala wzorcowego' }}</span>
            </button>
            
            <button 
                @click="sendToTerminals"
                :disabled="isSending || !canSynchronize"
                class="bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed flex items-center"
            >
                <svg v-if="isSending" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>{{ isSending ? 'Wysyłanie...' : 'Wyślij do zaznaczonych terminali' }}</span>
            </button>
        </div>

        <div class="grid grid-cols-2 gap-6">
            <!-- Lewa kolumna - Czytniki -->
            <div class="bg-white rounded-lg shadow p-4">
                <h2 class="text-lg font-semibold mb-4">Czytniki</h2>
                <div class="overflow-x-auto">
                    <table class="min-w-full">
                        <thead>
                            <tr class="bg-gray-50">
                                <th class="w-10 px-4 py-2">
                                    <input 
                                        type="checkbox" 
                                        v-model="allTerminalsSelected"
                                        @change="toggleAllTerminals"
                                        class="rounded border-gray-300"
                                    >
                                </th>
                                <th class="px-4 py-2 text-left">Nr</th>
                                <th class="px-4 py-2 text-left">Nazwa</th>
                                <th class="px-4 py-2 text-left">IP</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="terminal in terminalsStore.terminals" :key="terminal.id" class="border-t">
                                <td class="px-4 py-2">
                                    <input 
                                        type="checkbox" 
                                        v-model="selectedTerminals"
                                        :value="terminal.id"
                                        class="rounded border-gray-300"
                                    >
                                </td>
                                <td class="px-4 py-2">{{ terminal.number }}</td>
                                <td class="px-4 py-2">{{ terminal.name }}</td>
                                <td class="px-4 py-2">{{ terminal.ip_address }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Prawa kolumna - Pracownicy -->
            <div class="bg-white rounded-lg shadow p-4">
                <h2 class="text-lg font-semibold mb-4">Pracownicy</h2>
                <div class="overflow-x-auto">
                    <table class="min-w-full">
                        <thead>
                            <tr class="bg-gray-50">
                                <th class="w-10 px-4 py-2">
                                    <input 
                                        type="checkbox" 
                                        v-model="allEmployeesSelected"
                                        @change="toggleAllEmployees"
                                        class="rounded border-gray-300"
                                    >
                                </th>
                                <th class="px-4 py-2 text-left">Nr</th>
                                <th class="px-4 py-2 text-left">Imię i nazwisko</th>
                                <th class="px-4 py-2 text-left">Nr karty</th>
                                <th class="px-4 py-2 text-left">Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="employee in employeesStore.employees" :key="employee.id" class="border-t">
                                <td class="px-4 py-2">
                                    <input 
                                        type="checkbox" 
                                        v-model="selectedEmployees"
                                        :value="employee.id"
                                        class="rounded border-gray-300"
                                    >
                                </td>
                                <td class="px-4 py-2">{{ employee.enroll_number }}</td>
                                <td class="px-4 py-2">{{ employee.name }}</td>
                                <td class="px-4 py-2">{{ employee.card_number }}</td>
                                <td class="px-4 py-2">
                                    <span :class="{
                                        'px-2 py-1 rounded text-sm': true,
                                        'bg-green-100 text-green-800': employee.is_active,
                                        'bg-red-100 text-red-800': !employee.is_active
                                    }">
                                        {{ employee.is_active ? 'Aktywny' : 'Nieaktywny' }}
                                    </span>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useTerminalsStore } from '@/stores/terminals';
import { useEmployeesStore } from '@/stores/employees';
import AlertMessage from '@/components/AlertMessage.vue';
import { employeeService } from '@/services/employees';

const terminalsStore = useTerminalsStore();
const employeesStore = useEmployeesStore();

const selectedTerminals = ref<number[]>([]);
const selectedEmployees = ref<number[]>([]);
const isFetching = ref(false);
const isSending = ref(false);
const alertMessage = ref('');
const alertType = ref<'success' | 'error'>('success');

// Załaduj dane przy montowaniu komponentu
onMounted(async () => {
    await Promise.all([
        terminalsStore.fetchTerminals(),
        employeesStore.fetchEmployees()
    ]);
});

const allTerminalsSelected = computed({
    get: () => selectedTerminals.value.length === terminalsStore.terminals.length,
    set: (value) => {
        if (value) {
            selectedTerminals.value = terminalsStore.terminals.map(t => t.id);
        } else {
            selectedTerminals.value = [];
        }
    }
});

const allEmployeesSelected = computed({
    get: () => selectedEmployees.value.length === employeesStore.employees.length,
    set: (value) => {
        if (value) {
            selectedEmployees.value = employeesStore.employees.map(e => e.id);
        } else {
            selectedEmployees.value = [];
        }
    }
});

const canSynchronize = computed(() => 
    selectedTerminals.value.length > 0 && selectedEmployees.value.length > 0
);

function toggleAllTerminals(event: Event) {
    const checked = (event.target as HTMLInputElement).checked;
    if (checked) {
        selectedTerminals.value = terminalsStore.terminals.map(t => t.id);
    } else {
        selectedTerminals.value = [];
    }
}

function toggleAllEmployees(event: Event) {
    const checked = (event.target as HTMLInputElement).checked;
    if (checked) {
        selectedEmployees.value = employeesStore.employees.map(e => e.id);
    } else {
        selectedEmployees.value = [];
    }
}

async function handleSyncFromMain() {
    isFetching.value = true;
    alertMessage.value = '';
    
    try {
        await employeeService.syncFromMainTerminal();
        await employeesStore.fetchEmployees();
        alertMessage.value = 'Pomyślnie pobrano pracowników z terminala wzorcowego';
        alertType.value = 'success';
    } catch (error: any) {
        console.error('Błąd synchronizacji:', error);
        alertMessage.value = error.response?.data?.detail || 'Wystąpił błąd podczas pobierania pracowników';
        alertType.value = 'error';
    } finally {
        isFetching.value = false;
    }
}

async function sendToTerminals() {
    if (!canSynchronize.value) return;
    
    isSending.value = true;
    try {
        // TODO: Implementacja wysyłania do terminali
        await employeesStore.sendToTerminals({
            terminalIds: selectedTerminals.value,
            employeeIds: selectedEmployees.value
        });
    } catch (error) {
        console.error('Błąd podczas wysyłania danych do terminali:', error);
        // TODO: Dodaj obsługę błędów (np. wyświetlenie komunikatu)
    } finally {
        isSending.value = false;
    }
}
</script> 