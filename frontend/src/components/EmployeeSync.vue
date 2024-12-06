<template>
    <div>
        <v-card>
            <v-card-title>Synchronizacja pracowników</v-card-title>
            
            <v-card-text v-if="loading">
                <v-progress-circular indeterminate></v-progress-circular>
                Sprawdzanie różnic...
            </v-card-text>

            <v-card-text v-else-if="syncData">
                <v-alert type="info" class="mb-4">
                    {{ syncData.message }}
                    <ul class="mt-2">
                        <li>Nowi pracownicy: {{ syncData.summary.new_employees }}</li>
                        <li>Zmodyfikowani pracownicy: {{ syncData.summary.modified_employees }}</li>
                        <li>W czytniku: {{ syncData.summary.total_in_reader }}</li>
                        <li>W bazie: {{ syncData.summary.total_in_db }}</li>
                    </ul>
                </v-alert>

                <div v-if="syncData.to_add.length > 0" class="mb-4">
                    <h3 class="text-h6 mb-2">Nowi pracownicy do dodania:</h3>
                    <v-list>
                        <v-list-item v-for="emp in syncData.to_add" :key="emp.enroll_number">
                            {{ emp.name }} ({{ emp.enroll_number }})
                        </v-list-item>
                    </v-list>
                </div>

                <div v-if="syncData.to_update.length > 0">
                    <h3 class="text-h6 mb-2">Pracownicy do aktualizacji:</h3>
                    <v-list>
                        <v-list-item v-for="emp in syncData.to_update" :key="emp.enroll_number">
                            {{ emp.old.name }} → {{ emp.new.name }} ({{ emp.enroll_number }})
                        </v-list-item>
                    </v-list>
                </div>
            </v-card-text>

            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="error" @click="$router.push('/employees')">Anuluj</v-btn>
                <v-btn 
                    color="success" 
                    @click="confirmSync"
                    :disabled="!syncData || loading || confirming"
                    :loading="confirming"
                >
                    Zapisz zmiany
                </v-btn>
            </v-card-actions>
        </v-card>

        <v-snackbar v-model="showSnackbar" :color="snackbarColor">
            {{ snackbarText }}
        </v-snackbar>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { employeeService } from '../services/employees';

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

const loading = ref(false);
const confirming = ref(false);
const syncData = ref<SyncData | null>(null);
const showSnackbar = ref(false);
const snackbarText = ref('');
const snackbarColor = ref('');

const showMessage = (text: string, color: string = 'success') => {
    snackbarText.value = text;
    snackbarColor.value = color;
    showSnackbar.value = true;
};

onMounted(async () => {
    try {
        loading.value = true;
        syncData.value = await employeeService.checkSync();
    } catch (error) {
        showMessage('Błąd podczas sprawdzania różnic', 'error');
        console.error(error);
    } finally {
        loading.value = false;
    }
});

const confirmSync = async () => {
    try {
        confirming.value = true;
        await employeeService.confirmSync();
        showMessage('Pomyślnie zsynchronizowano dane');
        await new Promise(resolve => setTimeout(resolve, 1500)); // Poczekaj na wyświetlenie komunikatu
        window.location.href = '/employees'; // Przekieruj do listy pracowników
    } catch (error) {
        showMessage('Błąd podczas synchronizacji', 'error');
        console.error(error);
    } finally {
        confirming.value = false;
    }
};
</script>