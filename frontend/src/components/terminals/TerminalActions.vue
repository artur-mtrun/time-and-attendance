<template>
    <div class="space-x-2">
        <button
            @click="$emit('sync')"
            class="bg-blue-500 hover:bg-blue-600 text-white px-2 py-1 rounded text-sm"
            :disabled="isSyncing"
        >
            {{ isSyncing ? 'Synchronizacja...' : 'Synchronizuj' }}
        </button>
        <button
            @click="$emit('edit')"
            class="bg-green-500 hover:bg-green-600 text-white px-2 py-1 rounded text-sm"
        >
            Edytuj
        </button>
        <button
            @click="$emit('delete')"
            class="bg-red-500 hover:bg-red-600 text-white px-2 py-1 rounded text-sm"
        >
            Usuń
        </button>
    </div>
</template>

<script setup lang="ts">
defineProps<{
    isSyncing: boolean;
}>();

defineEmits<{
    sync: [];
    edit: [];
    delete: [];
}>();
</script> 