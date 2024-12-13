<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
    <div class="bg-white rounded-lg shadow-xl w-full max-w-2xl">
      <!-- Nagłówek -->
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-xl font-semibold text-gray-900">Wynik synchronizacji</h3>
      </div>
      
      <!-- Treść -->
      <div class="px-6 py-4 max-h-[60vh] overflow-y-auto modal-content">
        <div class="space-y-4">
          <!-- Podsumowanie -->
          <div class="p-4 bg-blue-50 rounded-lg">
            <p class="text-blue-700 font-medium">{{ getSummary() }}</p>
          </div>
          
          <!-- Szczegóły zmian -->
          <div class="space-y-2 font-mono text-sm">
            <pre class="whitespace-pre-wrap">{{ getDetails() }}</pre>
          </div>
        </div>
      </div>
      
      <!-- Stopka -->
      <div class="px-6 py-4 bg-gray-50 rounded-b-lg flex justify-end">
        <button
          @click="$emit('close')"
          class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
        >
          Zamknij
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  show: boolean;
  message: string;
}>();

defineEmits<{
  close: [];
}>();

function getSummary() {
  const lines = props.message.split('\n');
  return lines[0] + '\n' + lines[1];
}

function getDetails() {
  const lines = props.message.split('\n').slice(2);
  return lines.join('\n');
}
</script>

<style scoped>
.modal-content {
  scrollbar-width: thin;
  scrollbar-color: #CBD5E0 #EDF2F7;
}

.modal-content::-webkit-scrollbar {
  width: 8px;
}

.modal-content::-webkit-scrollbar-track {
  background: #EDF2F7;
  border-radius: 4px;
}

.modal-content::-webkit-scrollbar-thumb {
  background-color: #CBD5E0;
  border-radius: 4px;
  border: 2px solid #EDF2F7;
}
</style> 