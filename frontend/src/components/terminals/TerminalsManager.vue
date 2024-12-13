<template>
  <div>
    <TerminalsDashboard
      :selected-count="selectedTerminalIds.length"
      @add="showCreateModal = true"
      @sync-selected="syncSelectedTerminals"
      @delete-selected="confirmDeleteSelected"
    />

    <TerminalsList 
      :loading="loading"
      :syncingTerminal="syncingTerminal"
      @sync="syncTerminal"
      @edit="editTerminal"
      @delete="confirmDelete"
      @selection-change="handleSelectionChange"
    />

    <!-- Modale pozostają w ManagerComponent -->
    <!-- Modal do tworzenia/edycji czytnika -->
    <div v-if="showCreateModal || editedTerminal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div class="bg-white p-6 rounded-lg w-96">
        <h3 class="text-lg font-bold mb-4">
          {{ editedTerminal ? 'Edytuj czytnik' : 'Dodaj czytnik' }}
        </h3>
        <form @submit.prevent="handleSubmit">
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
          <div class="mb-4">
            <label class="flex items-center">
              <input
                v-model="formData.is_active"
                type="checkbox"
                class="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              />
              <span class="ml-2 text-sm text-gray-600">Aktywny</span>
            </label>
          </div>
          <div class="mb-4">
            <label class="flex items-center">
              <input
                v-model="formData.is_main"
                type="checkbox"
                class="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              />
              <span class="ml-2 text-sm text-gray-600">Terminal główny</span>
            </label>
          </div>
          <div class="flex justify-end space-x-2">
            <button
              type="button"
              @click="closeModal"
              class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              Anuluj
            </button>
            <button
              type="submit"
              class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
            >
              {{ editedTerminal ? 'Zapisz' : 'Dodaj' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal potwierdzenia usunięcia -->
    <div v-if="terminalToDelete" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div class="bg-white p-6 rounded-lg w-96">
        <h3 class="text-lg font-bold mb-4">Potwierdź usunięcie</h3>
        <p class="mb-4">Czy na pewno chcesz usunąć czytnik "{{ terminalToDelete?.name }}"?</p>
        <div class="flex justify-end space-x-2">
          <button
            @click="terminalToDelete = null"
            class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            Anuluj
          </button>
          <button
            @click="deleteTerminal"
            class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700"
          >
            Usuń
          </button>
        </div>
      </div>
    </div>


  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useTerminalsStore } from '@/stores/terminals';
import type { Terminal, SyncResult, SyncChange } from '@/types/terminal';
import TerminalsList from '@/components/terminals/TerminalsList.vue';
import TerminalModal from '@/components/terminals/TerminalModal.vue';
import DeleteConfirmationModal from '@/components/terminals/DeleteConfirmationModal.vue';
import TerminalsDashboard from '@/components/terminals/TerminalsDashboard.vue';

const emit = defineEmits<{
  alert: [message: string, type: 'error' | 'success' | 'warning']
}>();

const terminalsStore = useTerminalsStore();
const showCreateModal = ref(false);
const editedTerminal = ref<Terminal | null>(null);
const terminalToDelete = ref<Terminal | null>(null);
const syncingTerminal = ref<number | null>(null);
const loading = ref(false);
const formData = ref({
    number: 0,
    name: '',
    ip_address: '',
    port: 4370,
    is_active: true,
    is_main: false
});
const selectedTerminalIds = ref<number[]>([]);
const syncingTerminals = ref<number[]>([]);

async function loadTerminals() {
  loading.value = true;
  try {
    await terminalsStore.fetchTerminals();
  } catch (error: any) {
    emit('alert', error.response?.data?.detail || 'Nie udało się pobrać listy czytników', 'error');
  } finally {
    loading.value = false;
  }
}

async function handleSubmit() {
  try {
    if (editedTerminal.value) {
      await terminalsStore.updateTerminal(editedTerminal.value.id, formData.value);
      emit('alert', 'Czytnik został zaktualizowany', 'success');
    } else {
      await terminalsStore.createTerminal(formData.value);
      emit('alert', 'Czytnik został dodany', 'success');
    }
    closeModal();
    await loadTerminals();
  } catch (error: any) {
    emit('alert', error.response?.data?.detail || 'Wystąpił błąd podczas zapisywania czytnika', 'error');
  }
}

async function syncTerminal(terminal: Terminal) {
  syncingTerminal.value = terminal.id;
  try {
    const result: SyncResult = await terminalsStore.syncTerminal(terminal.id);
    emit('alert', `Synchronizacja terminala "${terminal.name}" zakończona pomyślnie`, 'success');
    await loadTerminals();
  } catch (error: any) {
    emit('alert', `Błąd synchronizacji terminala "${terminal.name}": ${error.response?.data?.detail || error.message}`, 'error');
  } finally {
    syncingTerminal.value = null;
  }
}

function closeModal() {
    showCreateModal.value = false;
    editedTerminal.value = null;
    formData.value = {
        number: 0,
        name: '',
        ip_address: '',
        port: 4370,
        is_active: true,
        is_main: false
    };
}

function editTerminal(terminal: Terminal) {
    editedTerminal.value = terminal;
    formData.value = {
        number: terminal.number,
        name: terminal.name,
        ip_address: terminal.ip_address,
        port: terminal.port,
        is_active: terminal.is_active,
        is_main: terminal.is_main
    };
    showCreateModal.value = true;
}

function confirmDelete(terminal: Terminal) {
    terminalToDelete.value = terminal;
}

async function deleteTerminal() {
    if (terminalToDelete.value) {
        try {
            await terminalsStore.deleteTerminal(terminalToDelete.value.id);
            emit('alert', 'Czytnik został usunięty', 'success');
            terminalToDelete.value = null;
            await loadTerminals();
        } catch (error: any) {
            emit('alert', error.response?.data?.detail || 'Wystąpił błąd podczas usuwania czytnika', 'error');
        }
    }
}

const handleSelectionChange = (ids: number[]) => {
  selectedTerminalIds.value = ids;
};

async function syncSelectedTerminals() {
  if (selectedTerminalIds.value.length === 0) {
    emit('alert', 'Nie wybrano żadnych terminali do synchronizacji', 'warning');
    return;
  }

  for (const id of selectedTerminalIds.value) {
    syncingTerminals.value.push(id);
    const terminal = terminalsStore.terminals.find(t => t.id === id);
    
    try {
      const result: SyncResult = await terminalsStore.syncTerminal(id);
      
      // Tworzenie szczegółowego raportu
      let detailMessage = `Synchronizacja terminala "${terminal?.name}":\n`;
      detailMessage += `Zsynchronizowano ${result.synced_employees} z ${result.total_employees} pracowników\n\n`;
      
      // Dodawanie szczegółów zmian
      if (result.changes.length > 0) {
        result.changes.forEach((change: SyncChange) => {
          if (change.type === 'add') {
            detailMessage += `➕ ${change.employee} (${change.enroll_number}): ${change.message}\n`;
          } else if (change.type === 'update') {
            detailMessage += `📝 ${change.employee} (${change.enroll_number}):\n`;
            change.changes?.forEach(changeDetail => {
              detailMessage += `   - ${changeDetail}\n`;
            });
          }
        });
      } else {
        detailMessage += "Brak zmian do synchronizacji";
      }
      
      emit('alert', detailMessage, 'success');
    } catch (error: any) {
      emit('alert', `Błąd synchronizacji terminala "${terminal?.name}": ${error.response?.data?.detail || error.message}`, 'error');
    } finally {
      syncingTerminals.value = syncingTerminals.value.filter(t => t !== id);
    }
  }
  
  await loadTerminals();
}

function confirmDeleteSelected() {
  if (selectedTerminalIds.value.length === 0) return;
  
  // Możesz utworzyć nowy modal do potwierdzenia masowego usuwania
  // lub użyć istniejącego terminalToDelete w inny sposób
}

onMounted(() => {
    loadTerminals();
});

// Reszta metod pozostaje bez zmian
</script> 