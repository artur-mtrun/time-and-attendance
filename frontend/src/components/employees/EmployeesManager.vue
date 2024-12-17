<template>
    <div>
      <EmployeesDashboard
        :selected-count="selectedEmployeeIds.length"
        @add="showCreateModal = true"
        @sync-selected="syncSelectedEmployees"
        @delete-selected="confirmDeleteSelected"
      />
  
      <EmployeesList 
        :loading="loading"
        :employees="employeesStore.employees"
        @edit="editEmployee"
        @delete="confirmDelete"
        @release="releaseEmployee"
        @selection-change="handleSelectionChange"
      />
  
      <EmployeeModal
        v-if="showCreateModal || editedEmployee"
        :form-data="formData"
        :is-edit="!!editedEmployee"
        @submit="handleSubmit"
        @cancel="closeModal"
      />
  
      <DeleteConfirmationModal
        v-if="employeeToDelete"
        :employee="employeeToDelete"
        @confirm="deleteEmployee"
        @cancel="employeeToDelete = null"
      />
    </div>
  </template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useEmployeesStore } from '@/stores/employees';
import EmployeesDashboard from './EmployeesDashboard.vue';
import EmployeesList from './EmployeesList.vue';
import EmployeeModal from './EmployeeModal.vue';
import DeleteConfirmationModal from '@/components/employees/DeleteConfirmationModal.vue';
import type { Employee, CreateEmployeeData } from '@/types/employee';

const emit = defineEmits<{
  alert: [message: string, type: 'error' | 'success' | 'warning']
}>();

const employeesStore = useEmployeesStore();
const loading = ref(false);
const showCreateModal = ref(false);
const editedEmployee = ref<Employee | null>(null);
const employeeToDelete = ref<Employee | null>(null);
const selectedEmployeeIds = ref<number[]>([]);
const formData = ref<CreateEmployeeData>({
  name: '',
  enroll_number: '',
  card_number: '',
  password: '',
  privileges: 0,
  is_active: true
});

async function loadEmployees() {
  loading.value = true;
  try {
    await employeesStore.fetchEmployees();
  } catch (error: any) {
    emit('alert', error.response?.data?.detail || 'Nie udało się pobrać listy pracowników', 'error');
  } finally {
    loading.value = false;
  }
}

async function handleSubmit() {
  try {
    if (editedEmployee.value) {
      await employeesStore.updateEmployee(editedEmployee.value.id, formData.value);
      emit('alert', 'Pracownik został zaktualizowany', 'success');
    } else {
      await employeesStore.createEmployee(formData.value);
      emit('alert', 'Pracownik został dodany', 'success');
    }
    closeModal();
    await loadEmployees();
  } catch (error: any) {
    emit('alert', error.response?.data?.detail || 'Wystąpił błąd podczas zapisywania pracownika', 'error');
  }
}

function closeModal() {
  showCreateModal.value = false;
  editedEmployee.value = null;
  formData.value = {
    name: '',
    enroll_number: '',
    card_number: '',
    password: '',
    privileges: 0,
    is_active: true
  };
}

function editEmployee(employee: Employee) {
  formData.value = {
    name: employee.name,
    enroll_number: employee.enroll_number ?? '',
    card_number: employee.card_number ?? '',
    password: employee.password ?? '',
    privileges: Number(employee.privileges),
    is_active: employee.is_active
  };
  editedEmployee.value = employee;
  showCreateModal.value = true;
}

function confirmDelete(employee: Employee) {
  employeeToDelete.value = employee;
}

async function deleteEmployee() {
  if (employeeToDelete.value) {
    try {
      await employeesStore.deleteEmployee(employeeToDelete.value.id);
      emit('alert', 'Pracownik został usunięty', 'success');
      employeeToDelete.value = null;
      await loadEmployees();
    } catch (error: any) {
      emit('alert', error.response?.data?.detail || 'Wystąpił błąd podczas usuwania pracownika', 'error');
    }
  }
}

const handleSelectionChange = (ids: number[]) => {
  selectedEmployeeIds.value = ids;
};

const syncSelectedEmployees = async () => {
  try {
    await employeesStore.sendToTerminals({
      employeeIds: selectedEmployeeIds.value,
      terminalIds: [] // lub przekaż odpowiednie ID terminali
    });
    emit('alert', 'Synchronizacja zakończona pomyślnie', 'success');
  } catch (error: any) {
    emit('alert', error.response?.data?.detail || 'Błąd synchronizacji', 'error');
  }
};

const confirmDeleteSelected = () => {
  // Implementacja usuwania zaznaczonych
};

async function releaseEmployee(employee: Employee) {
  try {
    await employeesStore.updateEmployee(employee.id, {
      ...employee,
      card_number: '0',
      password: '',
      is_active: false
    });
    emit('alert', 'Pracownik został zwolniony', 'success');
    await loadEmployees();
  } catch (error: any) {
    emit('alert', error.response?.data?.detail || 'Wystąpił błąd podczas zwalniania pracownika', 'error');
  }
}

onMounted(() => {
  loadEmployees();
});
</script>