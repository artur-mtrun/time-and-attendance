<template>
    <div class="mb-6">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div class="bg-white rounded-lg shadow p-4">
          <h3 class="text-sm font-semibold text-gray-600">Wszyscy pracownicy</h3>
          <p class="text-2xl font-bold">{{ totalEmployees }}</p>
        </div>
        <div class="bg-white rounded-lg shadow p-4">
          <h3 class="text-sm font-semibold text-gray-600">Aktywni</h3>
          <p class="text-2xl font-bold text-green-600">{{ activeEmployees }}</p>
        </div>
        <div class="bg-white rounded-lg shadow p-4">
          <h3 class="text-sm font-semibold text-gray-600">Zaznaczeni</h3>
          <p class="text-2xl font-bold text-purple-600">{{ selectedCount }}</p>
        </div>
      </div>
      <!-- Przyciski akcji -->
    </div>
  </template>

<script setup lang="ts">
import { computed } from 'vue';
import { useEmployeesStore } from '@/stores/employees';

const employeesStore = useEmployeesStore();

const totalEmployees = computed(() => employeesStore.employees.length);
const activeEmployees = computed(() => employeesStore.employees.filter(e => e.is_active).length);

defineProps<{
  selectedCount: number;
}>();

defineEmits<{
  add: [];
  'sync-selected': [];
  'delete-selected': [];
}>();
</script>