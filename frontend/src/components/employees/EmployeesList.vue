<template>
  <div class="bg-white shadow-md rounded-lg">
    <!-- Wyszukiwarka -->
    <div class="p-4 border-b">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Szukaj pracownika..."
        class="w-full px-3 py-2 border rounded-md"
        @input="handleSearch"
      />
    </div>

    <table class="min-w-full">
      <thead>
        <tr class="bg-gray-50">
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            <input
              type="checkbox"
              :checked="allSelected"
              @change="toggleAll"
              class="rounded border-gray-300 text-blue-600"
            />
          </th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nr ewidencyjny</th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Imię i nazwisko</th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Karta</th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Akcje</th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        <tr v-for="employee in paginatedEmployees" :key="employee.id">
          <td class="px-6 py-4 whitespace-nowrap">
            <input
              type="checkbox"
              :value="employee.id"
              v-model="selectedEmployees"
              class="rounded border-gray-300 text-blue-600"
              @change="emitSelectionChange"
            />
          </td>
          <td class="px-6 py-4 whitespace-nowrap">{{ employee.enroll_number }}</td>
          <td class="px-6 py-4 whitespace-nowrap">{{ employee.name }}</td>
          <td class="px-6 py-4 whitespace-nowrap">{{ employee.card_number }}</td>
          <td class="px-6 py-4 whitespace-nowrap">
            <span :class="employee.is_active ? 'text-green-600' : 'text-red-600'">
              {{ employee.is_active ? 'Aktywny' : 'Nieaktywny' }}
            </span>
          </td>
          <td class="px-6 py-4 whitespace-nowrap">
            <div class="space-x-2">
              <button
                @click="$emit('edit', employee)"
                class="bg-green-500 hover:bg-green-600 text-white px-2 py-1 rounded text-sm"
              >
                Edytuj
              </button>
              <button
                @click="$emit('delete', employee)"
                class="bg-red-500 hover:bg-red-600 text-white px-2 py-1 rounded text-sm"
              >
                Usuń
              </button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Paginacja -->
    <div class="px-6 py-3 flex items-center justify-between border-t">
      <div class="flex-1 flex justify-between items-center">
        <div>
          <select 
            v-model="itemsPerPage" 
            class="border rounded-md px-2 py-1"
            @change="handlePageSizeChange"
          >
            <option :value="10">10</option>
            <option :value="20">20</option>
            <option :value="50">50</option>
            <option :value="100">100</option>
          </select>
          <span class="ml-2 text-sm text-gray-700">
            Pozycji na stronie
          </span>
        </div>
        <div class="space-x-2">
          <button
            @click="currentPage--"
            :disabled="currentPage === 1"
            class="px-3 py-1 border rounded-md"
            :class="currentPage === 1 ? 'bg-gray-100' : 'hover:bg-gray-50'"
          >
            Poprzednia
          </button>
          <span class="text-sm text-gray-700">
            Strona {{ currentPage }} z {{ totalPages }}
          </span>
          <button
            @click="currentPage++"
            :disabled="currentPage === totalPages"
            class="px-3 py-1 border rounded-md"
            :class="currentPage === totalPages ? 'bg-gray-100' : 'hover:bg-gray-50'"
          >
            Następna
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import type { Employee } from '@/types/employee';

const props = defineProps<{
  employees: Employee[];
  loading?: boolean;
}>();

const emit = defineEmits<{
  edit: [employee: Employee];
  delete: [employee: Employee];
  'selection-change': [selectedIds: number[]];
}>();

const searchQuery = ref('');
const currentPage = ref(1);
const itemsPerPage = ref(20);
const selectedEmployees = ref<number[]>([]);

// Filtrowanie pracowników
const filteredEmployees = computed(() => {
  if (!searchQuery.value) return props.employees;
  
  const query = searchQuery.value.toLowerCase();
  return props.employees.filter(employee => 
    employee.name.toLowerCase().includes(query) ||
    employee.enroll_number.toLowerCase().includes(query) ||
    employee.card_number?.toLowerCase().includes(query)
  );
});

// Paginacja
const totalPages = computed(() => 
  Math.ceil(filteredEmployees.value.length / itemsPerPage.value)
);

const paginatedEmployees = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return filteredEmployees.value.slice(start, end);
});

// Reset strony przy zmianie wyszukiwania
watch(searchQuery, () => {
  currentPage.value = 1;
});

const handlePageSizeChange = () => {
  currentPage.value = 1;
};

const handleSearch = () => {
  currentPage.value = 1;
};

// Zaznaczanie
const allSelected = computed(() => {
  return paginatedEmployees.value.length > 0 && 
         paginatedEmployees.value.every(emp => selectedEmployees.value.includes(emp.id));
});

const toggleAll = (e: Event) => {
  const checked = (e.target as HTMLInputElement).checked;
  if (checked) {
    selectedEmployees.value = [...new Set([
      ...selectedEmployees.value,
      ...paginatedEmployees.value.map(e => e.id)
    ])];
  } else {
    selectedEmployees.value = selectedEmployees.value.filter(
      id => !paginatedEmployees.value.find(e => e.id === id)
    );
  }
  emitSelectionChange();
};

const emitSelectionChange = () => {
  emit('selection-change', selectedEmployees.value);
};
</script>