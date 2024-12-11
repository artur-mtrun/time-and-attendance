<template>
  <div>
    <h2 class="text-2xl font-bold mb-6">Dashboard</h2>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <!-- Statystyki czytników -->
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-semibold mb-4">Czytniki</h3>
        <div class="flex justify-between items-center">
          <div>
            <p class="text-gray-600">Aktywne</p>
            <p class="text-2xl font-bold text-green-600">{{ activeTerminals }}</p>
          </div>
          <div>
            <p class="text-gray-600">Wszystkie</p>
            <p class="text-2xl font-bold">{{ totalTerminals }}</p>
          </div>
        </div>
      </div>

      <!-- Statystyki pracowników -->
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-semibold mb-4">Pracownicy</h3>
        <div class="flex justify-between items-center">
          <div>
            <p class="text-gray-600">Aktywni</p>
            <p class="text-2xl font-bold text-green-600">{{ activeEmployees }}</p>
          </div>
          <div>
            <p class="text-gray-600">Wszyscy</p>
            <p class="text-2xl font-bold">{{ totalEmployees }}</p>
          </div>
        </div>
      </div>

      <!-- Ostatnie synchronizacje -->
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-semibold mb-4">Ostatnie synchronizacje</h3>
        <div v-if="lastSyncs.length > 0">
          <div v-for="sync in lastSyncs" :key="sync.id" class="mb-2">
            <p class="text-sm text-gray-600">
              {{ sync.terminal_name }} - {{ formatDate(sync.sync_date) }}
            </p>
          </div>
        </div>
        <p v-else class="text-gray-500">Brak ostatnich synchronizacji</p>
      </div>
    </div>

    <!-- Menu szybkiego dostępu -->
    <div class="mt-6 bg-white rounded-lg shadow p-6">
      <h3 class="text-lg font-semibold mb-4">Szybki dostęp</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        <router-link 
          to="/employees"
          class="flex items-center p-4 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors"
        >
          <div class="flex-1">
            <h4 class="font-semibold text-blue-700">Lista pracowników</h4>
            <p class="text-sm text-blue-600">Zarządzaj pracownikami</p>
          </div>
        </router-link>

        <router-link 
          to="/employees/sync"
          class="flex items-center p-4 bg-green-50 rounded-lg hover:bg-green-100 transition-colors"
        >
          <div class="flex-1">
            <h4 class="font-semibold text-green-700">Synchronizacja</h4>
            <p class="text-sm text-green-600">Synchronizuj z czytnikami</p>
          </div>
        </router-link>

        <router-link 
          to="/terminals"
          class="flex items-center p-4 bg-purple-50 rounded-lg hover:bg-purple-100 transition-colors"
        >
          <div class="flex-1">
            <h4 class="font-semibold text-purple-700">Czytniki</h4>
            <p class="text-sm text-purple-600">Zarządzaj czytnikami</p>
          </div>
        </router-link>

        <router-link 
          to="/attendance"
          class="flex items-center p-4 bg-orange-50 rounded-lg hover:bg-orange-100 transition-colors"
        >
          <div class="flex-1">
            <h4 class="font-semibold text-orange-700">Obecności</h4>
            <p class="text-sm text-orange-600">Zobacz obecności</p>
          </div>
        </router-link>

        <router-link 
          to="/attendance-all"
          class="flex items-center p-4 bg-indigo-50 rounded-lg hover:bg-indigo-100 transition-colors"
        >
          <div class="flex-1">
            <h4 class="font-semibold text-indigo-700">Wszystkie obecności</h4>
            <p class="text-sm text-indigo-600">Lista przed synchronizacją</p>
          </div>
        </router-link>
      </div>
    </div>

    <!-- Wykres obecności -->
    <div class="mt-6 bg-white rounded-lg shadow p-6">
      <h3 class="text-lg font-semibold mb-4">Obecności w tym tygodniu</h3>
      <div class="h-64">
        <!-- Tu możemy dodać wykres, np. używając Chart.js -->
        <p class="text-gray-500">Wykres obecności (do zaimplementowania)</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useTerminalsStore } from '@/stores/terminals';
import { useEmployeesStore } from '@/stores/employees';

interface SyncRecord {
  id: number;
  terminal_name: string;
  sync_date: string;
}

const terminalsStore = useTerminalsStore();
const employeesStore = useEmployeesStore();

const activeTerminals = ref(0);
const totalTerminals = ref(0);
const activeEmployees = ref(0);
const totalEmployees = ref(0);
const lastSyncs = ref<SyncRecord[]>([]);

function formatDate(date: string) {
  return new Date(date).toLocaleString('pl-PL', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

onMounted(async () => {
  try {
    await Promise.all([
      terminalsStore.fetchTerminals(),
      employeesStore.fetchEmployees()
    ]);

    // Oblicz statystyki
    totalTerminals.value = terminalsStore.terminals.length;
    activeTerminals.value = terminalsStore.terminals.filter(t => t.is_active).length;
    
    totalEmployees.value = employeesStore.employees.length;
    activeEmployees.value = employeesStore.employees.filter(e => e.is_active).length;

    // TODO: Pobierz ostatnie synchronizacje
    // lastSyncs.value = await syncService.getLastSyncs();
  } catch (error) {
    console.error('Błąd podczas ładowania danych:', error);
  }
});
</script> 