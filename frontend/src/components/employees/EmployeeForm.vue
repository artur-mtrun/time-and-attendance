<template>
  <form @submit.prevent="$emit('submit', formData)">
    <div class="mb-4">
      <label class="block text-sm font-medium text-gray-700">Pracownik</label>
      <select
        v-model="formData.enroll_number"
        required
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        @change="handleEmployeeSelect"
      >
        <option value="">Wybierz pracownika</option>
        <option 
          v-for="employee in filteredEmployees" 
          :key="employee.enroll_number"
          :value="employee.enroll_number"
        >
          {{ employee.name }} ({{ employee.enroll_number }})
        </option>
      </select>
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Szukaj pracownika..."
        class="mt-2 block w-full rounded-md border-gray-300 shadow-sm"
      />
    </div>

    <div class="mb-4">
      <label class="block text-sm font-medium text-gray-700">Numer karty</label>
      <input
        v-model="formData.card_number"
        type="text"
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
      />
    </div>

    <div class="mb-4">
      <label class="flex items-center">
        <input
          v-model="formData.is_active"
          type="checkbox"
          class="rounded border-gray-300"
        />
        <span class="ml-2 text-sm text-gray-600">Aktywny</span>
      </label>
    </div>

    <div class="flex justify-end space-x-2">
      <button
        type="button"
        @click="$emit('cancel')"
        class="px-4 py-2 border border-gray-300 rounded-md"
      >
        Anuluj
      </button>
      <button
        type="submit"
        class="px-4 py-2 bg-blue-600 text-white rounded-md"
      >
        {{ isEdit ? 'Zapisz' : 'Dodaj' }}
      </button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import type { Employee } from '@/types/employee';

const props = defineProps<{
  formData: Partial<Employee>;
  isEdit: boolean;
}>();

const emit = defineEmits<{
  submit: [formData: Partial<Employee>];
  cancel: [];
}>();

const searchQuery = ref('');
const employees = ref<Employee[]>([]); // Tu trzeba będzie pobrać listę pracowników

const filteredEmployees = computed(() => {
  if (!searchQuery.value) return employees.value;
  const query = searchQuery.value.toLowerCase();
  return employees.value.filter(employee => employee.name.toLowerCase().includes(query));
});

const handleEmployeeSelect = (event: Event) => {
  const selectedValue = (event.target as HTMLSelectElement).value;
  const selected = employees.value.find(emp => emp.enroll_number === selectedValue);
  if (selected) {
    props.formData.name = selected.name;
  }
};
</script> 