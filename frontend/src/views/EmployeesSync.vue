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
            
            <button 
                @click="fetchAttendanceFromTerminals"
                :disabled="isFetchingAttendance || !selectedTerminals.length"
                class="bg-purple-500 text-white px-6 py-2 rounded hover:bg-purple-600 disabled:bg-gray-300 disabled:cursor-not-allowed flex items-center"
            >
                <svg v-if="isFetchingAttendance" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>{{ isFetchingAttendance ? 'Pobieranie...' : 'Pobierz zdarzenia z zaznaczonych' }}</span>
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

        <div v-if="showSyncDialog" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div class="bg-white rounded-lg shadow-xl p-6 max-w-2xl w-full mx-4">
                <h2 class="text-xl font-bold mb-4">Potwierdzenie synchronizacji</h2>
                
                <div v-if="syncData">
                    <div class="bg-blue-50 border-l-4 border-blue-400 p-4 mb-4">
                        {{ syncData.message }}
                        <ul class="mt-2 list-disc list-inside">
                            <li>Nowi pracownicy: {{ syncData.summary.new_employees }}</li>
                            <li>Zmodyfikowani pracownicy: {{ syncData.summary.modified_employees }}</li>
                            <li>W czytniku: {{ syncData.summary.total_in_reader }}</li>
                            <li>W bazie: {{ syncData.summary.total_in_db }}</li>
                        </ul>
                    </div>

                    <div v-if="syncData.to_add.length > 0" class="mb-4">
                        <h3 class="font-semibold mb-2">Nowi pracownicy do dodania:</h3>
                        <ul class="list-disc list-inside">
                            <li v-for="emp in syncData.to_add" :key="emp.enroll_number">
                                {{ emp.name }} ({{ emp.enroll_number }})
                            </li>
                        </ul>
                    </div>

                    <div v-if="syncData.to_update.length > 0">
                        <h3 class="font-semibold mb-2">Pracownicy do aktualizacji:</h3>
                        <ul class="list-disc list-inside">
                            <li v-for="emp in syncData.to_update" :key="emp.enroll_number">
                                {{ emp.old.name }} → {{ emp.new.name }} ({{ emp.enroll_number }})
                            </li>
                        </ul>
                    </div>
                </div>

                <div class="flex justify-end space-x-4 mt-6">
                    <button 
                        @click="showSyncDialog = false"
                        class="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300"
                    >
                        Anuluj
                    </button>
                    <button 
                        @click="confirmSync"
                        :disabled="isFetching"
                        class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 disabled:bg-gray-300 disabled:cursor-not-allowed"
                    >
                        {{ isFetching ? 'Zapisywanie...' : 'Zatwierdź zmiany' }}
                    </button>
                </div>
            </div>
        </div>

        <div v-if="showSendReport" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div class="bg-white rounded-lg shadow-xl p-6 max-w-2xl w-full mx-4">
                <h2 class="text-xl font-bold mb-4">Raport wysyłania</h2>
                
                <div class="bg-blue-50 border-l-4 border-blue-400 p-4 mb-4">
                    {{ sendReport.message }}
                </div>

                <div class="mb-4">
                    <h3 class="font-semibold mb-2">Szczegóły wysyłania:</h3>
                    <div class="space-y-2">
                        <div v-for="detail in sendReport.details" 
                             :key="detail.terminal_id"
                             :class="[
                                 'p-3 rounded',
                                 detail.status === 'success' ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'
                             ]"
                        >
                            <div class="font-medium">
                                Terminal #{{ getTerminalInfo(detail.terminal_id).number }} - 
                                {{ getTerminalInfo(detail.terminal_id).name }}
                            </div>
                            <div class="text-sm">{{ detail.message }}</div>
                        </div>
                    </div>
                </div>

                <div class="flex justify-end space-x-4 mt-6">
                    <button 
                        @click="showSendReport = false"
                        class="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300"
                    >
                        Zamknij
                    </button>
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
import axios from 'axios';

const terminalsStore = useTerminalsStore();
const employeesStore = useEmployeesStore();

const selectedTerminals = ref<number[]>([]);
const selectedEmployees = ref<number[]>([]);
const isFetching = ref(false);
const isSending = ref(false);
const isFetchingAttendance = ref(false);
const alertMessage = ref('');
const alertType = ref<'success' | 'error'>('success');
const syncData = ref<any>(null);
const showSyncDialog = ref(false);
const showSendReport = ref(false);
const sendReport = ref<{
    message: string;
    details: Array<{
        terminal_id: number;
        status: 'success' | 'error';
        message: string;
    }>;
}>({ message: '', details: [] });

// Załaduj dane przy montowaniu komponentu
onMounted(async () => {
    try {
        await Promise.all([
            terminalsStore.fetchTerminals(),
            employeesStore.fetchEmployees()
        ]);
        console.log('Załadowane terminale:', terminalsStore.terminals);
    } catch (error) {
        console.error('Błąd podczas ładowania danych:', error);
    }
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
    try {
        isFetching.value = true;
        console.log('Rozpoczynam synchronizację');
        const result = await employeeService.checkSync();
        console.log('Otrzymane dane:', result);
        console.log('Struktura danych:', {
            message: result.message,
            summary: result.summary,
            to_add: result.to_add?.length,
            to_update: result.to_update?.length
        });
        
        // Tutaj powinien pojawić się dialog z różnicami
        // Dodaj wyświetlanie danych
        syncData.value = result;
        showSyncDialog.value = true;
        
        console.log('Dialog powinien być widoczny:', showSyncDialog.value);
        console.log('Dane synchronizacji:', syncData.value);
        
    } catch (error) {
        console.error('Błąd:', error);
        alertMessage.value = 'Wystąpił błąd podczas synchronizacji';
        alertType.value = 'error';
    } finally {
        isFetching.value = false;
    }
}

async function sendToTerminals() {
    if (!canSynchronize.value) return;
    
    isSending.value = true;
    try {
        const response = await employeesStore.sendToTerminals({
            terminalIds: selectedTerminals.value,
            employeeIds: selectedEmployees.value
        });
        
        // Ustaw dane raportu
        sendReport.value = response;
        showSendReport.value = true;
        
    } catch (error: any) {
        console.error('Błąd podczas wysyłania danych do terminali:', error);
        alertMessage.value = error.response?.data?.detail || 'Wystąpił błąd podczas wysyłania do terminali';
        alertType.value = 'error';
    } finally {
        isSending.value = false;
    }
}

async function confirmSync() {
    try {
        isFetching.value = true;
        await employeeService.confirmSync();
        showSyncDialog.value = false;
        alertMessage.value = 'Pomyślnie zsynchronizowano dane';
        alertType.value = 'success';
        await employeesStore.fetchEmployees(); // Odśwież listę pracowników
    } catch (error) {
        console.error('Błąd podczas zatwierdzania synchronizacji:', error);
        alertMessage.value = 'Wystąpił błąd podczas zatwierdzania zmian';
        alertType.value = 'error';
    } finally {
        isFetching.value = false;
    }
}

function getTerminalInfo(terminalId: number) {
    const terminal = terminalsStore.terminals.find(t => t.id === terminalId);
    if (!terminal) {
        console.warn(`Nie znaleziono terminala o ID: ${terminalId}`);
    }
    return {
        number: terminal?.number || terminalId,
        name: terminal?.name || `Terminal ${terminalId}`
    };
}

async function fetchAttendanceFromTerminals() {
    if (!selectedTerminals.value.length) return;
    
    isFetchingAttendance.value = true;
    try {
        const response = await employeeService.fetchAttendanceFromTerminals(selectedTerminals.value);
        
        alertMessage.value = response.message;
        alertType.value = 'success';
        
        // Wyświetl szczegółowy raport
        sendReport.value = {
            message: response.message,
            details: response.details
        };
        showSendReport.value = true;
        
    } catch (error: any) {
        console.error('Błąd podczas pobierania zdarzeń:', error);
        alertMessage.value = error.response?.data?.detail || 'Wystąpił błąd podczas pobierania zdarzeń';
        alertType.value = 'error';
    } finally {
        isFetchingAttendance.value = false;
    }
}
</script> 