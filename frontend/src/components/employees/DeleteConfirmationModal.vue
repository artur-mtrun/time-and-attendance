<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
    <div class="bg-white p-6 rounded-lg w-96">
      <h3 class="text-lg font-bold mb-4">Potwierdź usunięcie</h3>
      <p class="mb-4">
        Czy na pewno chcesz usunąć pracownika "{{ employee.name }}"?
      </p>
      <div class="flex justify-end space-x-2">
        <button
          @click="$emit('cancel')"
          class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
        >
          Anuluj
        </button>
        <button
          @click="$emit('confirm')"
          class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700"
        >
          Usuń
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Employee } from '@/types/employee';

defineProps<{
  employee: Employee;
}>();

defineEmits<{
  confirm: [];
  cancel: [];
}>();
</script>
