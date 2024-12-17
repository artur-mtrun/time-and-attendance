<template>
  <form @submit.prevent="$emit('submit', formData)">
    <div class="mb-4">
      <label class="block text-sm font-medium text-gray-700">Numer ewidencyjny</label>
      <input
        v-model="formData.enroll_number"
        type="text"
        required
        :disabled="isEdit"
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
      />
    </div>

    <div class="mb-4">
      <label class="block text-sm font-medium text-gray-700">Imię i nazwisko</label>
      <input
        v-model="formData.name"
        type="text"
        required
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
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
      <label class="block text-sm font-medium text-gray-700">PIN</label>
      <input
        v-model="formData.password"
        type="text"
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
      />
    </div>

    <div class="mb-4">
      <label class="block text-sm font-medium text-gray-700">Uprawnienia</label>
      <select
        v-model.number="formData.privileges"
        required
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
      >
        <option :value="0">Użytkownik</option>
        <option :value="1">Register</option>
        <option :value="2">SysAdmin</option>
        <option :value="3">Superadmin</option>
      </select>
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
        class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
      >
        {{ isEdit ? 'Zapisz' : 'Dodaj' }}
      </button>
    </div>
  </form>
</template>

<script setup lang="ts">
import type { Employee } from '@/types/employee';

defineProps<{
  formData: Partial<Employee> & { privileges?: number };
  isEdit: boolean;
}>();

defineEmits<{
  submit: [formData: Partial<Employee>];
  cancel: [];
}>();
</script> 