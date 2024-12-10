<template>
    <v-data-table
        v-model="selectedEmployees"
        :items="employees"
        show-select
        item-value="id"
        return-object
    ></v-data-table>

    <v-data-table
        v-model="selectedTerminals"
        :items="terminals"
        show-select
        item-value="id"
        return-object
    ></v-data-table>

    <!-- Modal z raportem wysyłania -->
    <div v-if="showSendReport" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
        <div class="bg-white p-6 rounded-lg w-96">
            <h3 class="text-lg font-bold mb-4">Raport wysyłania</h3>
            <div class="mb-4">
                <div v-for="result in sendReport.details" :key="result.terminal_id" 
                     class="mb-2 p-2 rounded"
                     :class="result.status === 'success' ? 'bg-green-50' : 'bg-red-50'">
                    <div class="font-medium" 
                         :class="result.status === 'success' ? 'text-green-700' : 'text-red-700'">
                        Terminal #{{ result.terminal_id }}
                    </div>
                    <div class="text-sm" 
                         :class="result.status === 'success' ? 'text-green-600' : 'text-red-600'">
                        {{ result.message }}
                    </div>
                </div>
            </div>
            <div class="text-sm text-gray-600 mb-4">
                {{ sendReport.message }}
            </div>
            <div class="flex justify-end">
                <button
                    @click="showSendReport = false"
                    class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                >
                    Zamknij
                </button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, type Ref } from 'vue';
import { employeeService } from '../services/employees';
import { useEmployeesStore } from '../stores/employees';
import { useTerminalsStore } from '../stores/terminals';
import type { Terminal } from '@/types/terminal';
import type { Employee } from '@/types/employee';

// Interfejsy
interface SyncData {
    summary: {
        new_employees: number;
        modified_employees: number;
        total_in_reader: number;
        total_in_db: number;
    };
    message: string;
    to_add: Array<{ name: string; enroll_number: string }>;
    to_update: Array<{
        old: { name: string };
        new: { name: string };
        enroll_number: string;
    }>;
}

interface SendReportDetail {
    terminal_id: number;
    status: 'success' | 'error';
    message: string;
}

interface SendReport {
    message: string;
    details: SendReportDetail[];
}

interface ApiResponse {
    message: string;
    details: SendReportDetail[];
}

interface SendToTerminalsResponse {
    status: number;
    data: {
        message: string;
        details: SendReportDetail[];
    };
    headers: {
        'content-length': string;
        'content-type': string;
    };
}

interface SelectedEmployee {
    id: number;
}

interface SelectedTerminal {
    id: number;
}

// Zmienne
const loading = ref(false);
const confirming = ref(false);
const sending = ref(false);
const syncData = ref<SyncData | null>(null);
const showSnackbar = ref(false);
const snackbarText = ref('');
const snackbarColor = ref('');
const showSendReport = ref(false);
const alertMessage = ref('');
const alertType = ref<'error' | 'success'>('error');

const employeesStore = useEmployeesStore();
const terminalsStore = useTerminalsStore();

const employees = computed(() => employeesStore.employees);
const terminals = computed(() => terminalsStore.terminals);

const selectedEmployees = ref<SelectedEmployee[]>([]);
const selectedTerminals = ref<SelectedTerminal[]>([]);

const sendReport = ref<SendReport>({
    message: '',
    details: []
}) as Ref<SendReport>;

const sendToTerminals = async () => {
    try {
        const result = await employeesStore.sendToTerminals({
            terminalIds: selectedTerminals.value.map((t: SelectedTerminal) => t.id),
            employeeIds: selectedEmployees.value.map((e: SelectedEmployee) => e.id)
        }) as unknown as SendToTerminalsResponse;
        
        sendReport.value = {
            message: result.data.message,
            details: result.data.details
        };
        showSendReport.value = true;
    } catch (error: any) {
        alertMessage.value = error.response?.data?.detail || 'Wystąpił błąd podczas wysyłania do terminali';
        alertType.value = 'error';
    } finally {
        sending.value = false;
    }
};

// ... reszta kodu (headers, computed, methods) bez zmian ...
</script> 