<template>
  <div>
    <div v-if="loading" class="flex justify-center py-4">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
    </div>

    <div v-else class="bg-white shadow-md rounded-lg">
      <table class="min-w-full">
        <thead>
          <tr class="bg-gray-50">
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              <input
                type="checkbox"
                :checked="allSelected"
                @change="toggleAll"
                class="rounded border-gray-300 text-blue-600"
              />
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nr</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nazwa</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">IP</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Port</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Główny</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ostatnia synchronizacja</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Akcje</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr 
            v-for="terminal in terminalsStore.terminals" 
            :key="terminal.id"
            :class="{
              'bg-blue-50': terminal.is_main,
              'hover:bg-blue-100': terminal.is_main,
              'hover:bg-gray-50': !terminal.is_main
            }"
          >
            <td class="px-6 py-4 whitespace-nowrap">
              <input
                type="checkbox"
                :value="terminal.id"
                v-model="selectedTerminals"
                class="rounded border-gray-300 text-blue-600"
                @change="$emit('selection-change', selectedTerminals)"
              />
            </td>
            <td class="px-6 py-4 whitespace-nowrap" :class="{ 'font-semibold': terminal.is_main }">
              {{ terminal.number }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap" :class="{ 'font-semibold': terminal.is_main }">
              {{ terminal.name }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">{{ terminal.ip_address }}</td>
            <td class="px-6 py-4 whitespace-nowrap">{{ terminal.port }}</td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span :class="terminal.is_active ? 'text-green-600' : 'text-red-600'">
                {{ terminal.is_active ? 'Aktywny' : 'Nieaktywny' }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span :class="terminal.is_main ? 'text-blue-600 font-semibold' : 'text-gray-600'">
                {{ terminal.is_main ? 'Tak' : 'Nie' }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              {{ terminal.last_sync_at ? new Date(terminal.last_sync_at).toLocaleString() : 'Nigdy' }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <TerminalActions
                :is-syncing="syncingTerminal === terminal.id"
                @sync="$emit('sync', terminal)"
                @edit="$emit('edit', terminal)"
                @delete="$emit('delete', terminal)"
              />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useTerminalsStore } from '@/stores/terminals';
import type { Terminal } from '@/types/terminal';
import TerminalActions from './TerminalActions.vue';

const terminalsStore = useTerminalsStore();
const selectedTerminals = ref<number[]>([]);

const allSelected = computed(() => {
  return terminalsStore.terminals.length > 0 && 
         selectedTerminals.value.length === terminalsStore.terminals.length;
});

const toggleAll = (e: Event) => {
  const checked = (e.target as HTMLInputElement).checked;
  selectedTerminals.value = checked 
    ? terminalsStore.terminals.map(t => t.id)
    : [];
  emit('selection-change', selectedTerminals.value);
};

defineProps<{
  loading: boolean;
  syncingTerminal: number | null;
}>();

const emit = defineEmits<{
  sync: [terminal: Terminal];
  edit: [terminal: Terminal];
  delete: [terminal: Terminal];
  'selection-change': [selectedIds: number[]];
}>();
</script> 