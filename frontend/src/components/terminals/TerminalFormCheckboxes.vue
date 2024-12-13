<template>
    <div class="space-y-4">
        <label class="flex items-center">
            <input
                :checked="isActive"
                @change="e => $emit('update:isActive', (e.target as HTMLInputElement).checked)"
                type="checkbox"
                class="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
            <span class="ml-2 text-sm text-gray-600">Aktywny</span>
        </label>
        <label class="flex items-center">
            <input
                :checked="isMain"
                @change="e => $emit('update:isMain', (e.target as HTMLInputElement).checked)"
                type="checkbox"
                class="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
            <span class="ml-2 text-sm text-gray-600">Terminal główny</span>
        </label>
    </div>
</template>

<script setup lang="ts">
defineProps<{
    isActive: boolean;
    isMain: boolean;
}>();

defineEmits<{
    'update:isActive': [value: boolean];
    'update:isMain': [value: boolean];
}>();
</script> 