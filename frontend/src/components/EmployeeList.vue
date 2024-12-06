<template>
    <div>
        <router-link 
            to="/employees/sync"
            class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
            Synchronizacja z terminalem
        </router-link>
        
        <v-data-table
            :headers="headers"
            :items="employees"
            class="elevation-1"
        >
            <template v-slot:top>
                <v-toolbar flat>
                    <v-toolbar-title>Lista pracowników</v-toolbar-title>
                    <v-divider class="mx-4" inset vertical></v-divider>
                    <v-spacer></v-spacer>
                    <v-btn 
                        color="primary" 
                        @click="checkSync"
                        :loading="loading"
                    >
                        Pobierz z terminala wzorcowego
                    </v-btn>
                </v-toolbar>
            </template>
        </v-data-table>

        <!-- Dialog potwierdzenia synchronizacji -->
        <v-dialog v-model="showSyncDialog" max-width="600px">
            <v-card>
                <v-card-title>Potwierdzenie synchronizacji</v-card-title>
                <v-card-text v-if="syncData">
                    <v-alert type="info">
                        Znaleziono różnice w danych pracowników:
                        <ul>
                            <li>Nowi pracownicy: {{ syncData.summary.new_employees }}</li>
                            <li>Zmodyfikowani pracownicy: {{ syncData.summary.modified_employees }}</li>
                        </ul>
                    </v-alert>

                    <div v-if="syncData.to_add.length > 0">
                        <h3>Nowi pracownicy do dodania:</h3>
                        <v-list>
                            <v-list-item v-for="emp in syncData.to_add" :key="emp.enroll_number">
                                {{ emp.name }} ({{ emp.enroll_number }})
                            </v-list-item>
                        </v-list>
                    </div>

                    <div v-if="syncData.to_update.length > 0">
                        <h3>Pracownicy do aktualizacji:</h3>
                        <v-list>
                            <v-list-item v-for="emp in syncData.to_update" :key="emp.enroll_number">
                                {{ emp.old.name }} → {{ emp.new.name }} ({{ emp.enroll_number }})
                            </v-list-item>
                        </v-list>
                    </div>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="error" @click="showSyncDialog = false">Anuluj</v-btn>
                    <v-btn 
                        color="success" 
                        @click="confirmSync"
                        :loading="confirming"
                    >
                        Zatwierdź zmiany
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useEmployeesStore } from '@/stores/employees';
import { storeToRefs } from 'pinia';

interface SyncData {
  summary: {
    new_employees: number;
    modified_employees: number;
  };
  to_add: Array<{ name: string; enroll_number: string }>;
  to_update: Array<{
    old: { name: string };
    new: { name: string };
    enroll_number: string;
  }>;
}

const employeesStore = useEmployeesStore();
const { employees } = storeToRefs(employeesStore);
const showSyncDialog = ref(false);
const syncData = ref<SyncData | null>(null);
const confirming = ref(false);
const loading = ref(false);

const headers = [
    { title: 'ID', key: 'id' },
    { title: 'Numer', key: 'enroll_number' },
    { title: 'Imię i nazwisko', key: 'name' },
    { title: 'Numer karty', key: 'card_number' },
    { title: 'Uprawnienia', key: 'privileges' },
    { title: 'Status', key: 'is_active' }
];

async function checkSync() {
    try {
        loading.value = true;
        syncData.value = await employeesStore.checkSync();
        showSyncDialog.value = true;
    } catch (error) {
        console.error('Błąd podczas sprawdzania synchronizacji:', error);
    } finally {
        loading.value = false;
    }
}

async function confirmSync() {
    try {
        confirming.value = true;
        await employeesStore.confirmSync();
        showSyncDialog.value = false;
        // Odśwież listę pracowników
        await employeesStore.fetchEmployees();
    } catch (error) {
        console.error('Błąd podczas zatwierdzania synchronizacji:', error);
    } finally {
        confirming.value = false;
    }
}
</script> 