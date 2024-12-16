<template>
  <div class="p-4">
    <AlertMessage
      :message="alertMessage"
      :type="alertType"
      @close="alertMessage = ''"
    />
    <EmployeesManager
      @alert="handleAlert"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import AlertMessage from '@/components/AlertMessage.vue';
import EmployeesManager from '@/components/employees/EmployeesManager.vue';

const alertMessage = ref('');
const alertType = ref<'error' | 'success' | 'warning'>('error');

const handleAlert = (message: string, type: 'error' | 'success' | 'warning') => {
  alertMessage.value = message;
  alertType.value = type;
};
</script> 