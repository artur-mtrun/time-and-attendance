<template>
    <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
        <div class="bg-white p-6 rounded-lg w-96">
            <h3 class="text-lg font-bold mb-4">
                {{ isEdit ? 'Edytuj czytnik' : 'Dodaj czytnik' }}
            </h3>
            <TerminalForm
                :form-data="formData"
                :is-edit="isEdit"
                @submit="$emit('submit', $event)"
                @cancel="$emit('cancel')"
            />
        </div>
    </div>
</template>

<script setup lang="ts">
import TerminalForm from '@/components/terminals/TerminalForm.vue';
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