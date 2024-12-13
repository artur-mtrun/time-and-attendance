<template>
  <div class="mb-6">
    <!-- Statystyki -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      <div class="bg-white rounded-lg shadow p-4">
        <h3 class="text-sm font-semibold text-gray-600">Wszystkie czytniki</h3>
        <p class="text-2xl font-bold">{{ totalTerminals }}</p>
      </div>
      <div class="bg-white rounded-lg shadow p-4">
        <h3 class="text-sm font-semibold text-gray-600">Aktywne</h3>
        <p class="text-2xl font-bold text-green-600">{{ activeTerminals }}</p>
      </div>
      <div class="bg-white rounded-lg shadow p-4">
        <h3 class="text-sm font-semibold text-gray-600">Online</h3>
        <p class="text-2xl font-bold text-blue-600">{{ onlineTerminals }}</p>
      </div>
      <div class="bg-white rounded-lg shadow p-4">
        <h3 class="text-sm font-semibold text-gray-600">Zaznaczone</h3>
        <p class="text-2xl font-bold text-purple-600">{{ selectedCount }}</p>
      </div>
    </div>

    <!-- Menu akcji -->
    <div class="bg-white rounded-lg shadow p-4">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <button
          @click="$emit('add')"
          class="flex items-center justify-center p-4 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors"
        >
          <div class="text-center">
            <h4 class="font-semibold text-blue-700">Dodaj czytnik</h4>
            <p class="text-sm text-blue-600">Nowy czytnik</p>
          </div>
        </button>

        <button
          @click="$emit('sync-selected')"
          :disabled="!selectedCount"
          :class="[
            'flex items-center justify-center p-4 rounded-lg transition-colors',
            selectedCount 
              ? 'bg-green-50 hover:bg-green-100' 
              : 'bg-gray-50 cursor-not-allowed'
          ]"
        >
          <div class="text-center">
            <h4 class="font-semibold" :class="selectedCount ? 'text-green-700' : 'text-gray-700'">
              Synchronizuj zaznaczone
            </h4>
            <p class="text-sm" :class="selectedCount ? 'text-green-600' : 'text-gray-600'">
              {{ selectedCount }} czytników
            </p>
          </div>
        </button>

        <button
          @click="$emit('delete-selected')"
          :disabled="!selectedCount"
          :class="[
            'flex items-center justify-center p-4 rounded-lg transition-colors',
            selectedCount 
              ? 'bg-red-50 hover:bg-red-100' 
              : 'bg-gray-50 cursor-not-allowed'
          ]"
        >
          <div class="text-center">
            <h4 class="font-semibold" :class="selectedCount ? 'text-red-700' : 'text-gray-700'">
              Usuń zaznaczone
            </h4>
            <p class="text-sm" :class="selectedCount ? 'text-red-600' : 'text-gray-600'">
              {{ selectedCount }} czytników
            </p>
          </div>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useTerminalsStore } from '@/stores/terminals';

const props = defineProps<{
  selectedCount: number;
}>();

const terminalsStore = useTerminalsStore();

const totalTerminals = computed(() => terminalsStore.terminals.length);
const activeTerminals = computed(() => terminalsStore.terminals.filter(t => t.is_active).length);
const onlineTerminals = computed(() => 0); // TODO: Zaimplementować logikę online

defineEmits<{
  add: [];
  'sync-selected': [];
  'delete-selected': [];
}>();
</script> 