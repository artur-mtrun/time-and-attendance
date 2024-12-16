<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
    <div class="bg-white p-6 rounded-lg w-96">
      <h3 class="text-lg font-bold mb-4">
        {{ isEdit ? 'Edytuj pracownika' : 'Dodaj pracownika' }}
      </h3>
      <EmployeeForm
        :form-data="formData"
        :is-edit="isEdit"
        @submit="$emit('submit', $event)"
        @cancel="$emit('cancel')"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import EmployeeForm from '@/components/employees/EmployeeForm.vue';
import type { Employee } from '@/types/employee';

defineProps<{
  formData: Partial<Employee>;
  isEdit: boolean;
}>();

defineEmits<{
  submit: [formData: Partial<Employee>];
  cancel: [];
}>();
</script>