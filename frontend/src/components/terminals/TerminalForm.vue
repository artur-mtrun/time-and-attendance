<template>
    <form @submit.prevent="$emit('submit', formData)">
        <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700">Numer czytnika</label>
            <input
                v-model.number="formData.number"
                type="number"
                required
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
        </div>
        <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700">Nazwa</label>
            <input
                v-model="formData.name"
                type="text"
                required
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
        </div>
        <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700">Adres IP</label>
            <input
                v-model="formData.ip_address"
                type="text"
                required
                pattern="^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
        </div>
        <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700">Port</label>
            <input
                v-model.number="formData.port"
                type="number"
                required
                min="1"
                max="65535"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
        </div>
        <TerminalFormCheckboxes
            v-model:is-active="formData.is_active"
            v-model:is-main="formData.is_main"
        />
        <div class="flex justify-end space-x-2">
            <button
                type="button"
                @click="$emit('cancel')"
                class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
                Anuluj
            </button>
            <button
                type="submit"
                class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
            >
                {{ isEdit ? 'Zapisz' : 'Dodaj' }}
            </button>
        </div>
    </form>
</template>

<script setup lang="ts">
import TerminalFormCheckboxes from '@/components/terminals/TerminalFormCheckboxes.vue';
import type { TerminalFormData } from '@/types/terminal';

defineProps<{
    formData: TerminalFormData;
    isEdit: boolean;
}>();

defineEmits<{
    submit: [formData: TerminalFormData];
    cancel: [];
}>();
</script> 