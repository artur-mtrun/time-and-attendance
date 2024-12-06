<template>
    <div class="p-4">
        <div class="flex justify-between items-center mb-4">
            <h2 class="text-2xl font-bold">Lista pracowników</h2>
            <button
                @click="showCreateModal = true"
                class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
            >
                Dodaj pracownika
            </button>
        </div>

        <div v-if="employeesStore.loading" class="text-center py-4">
            Ładowanie...
        </div>

        <div v-else-if="employeesStore.error" class="text-red-500 text-center py-4">
            {{ employeesStore.error }}
        </div>

        <div v-else class="bg-white shadow-md rounded-lg">
            <table class="min-w-full">
                <thead>
                    <tr class="bg-gray-50">
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nr</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Imię i nazwisko</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Karta</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Akcje</th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="employee in employeesStore.employees" :key="employee.id">
                        <td class="px-6 py-4 whitespace-nowrap">{{ employee.enroll_number }}</td>
                        <td class="px-6 py-4 whitespace-nowrap">{{ employee.name }}</td>
                        <td class="px-6 py-4 whitespace-nowrap">{{ employee.card_number || '-' }}</td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span :class="employee.is_active ? 'text-green-600' : 'text-red-600'">
                                {{ employee.is_active ? 'Aktywny' : 'Nieaktywny' }}
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap space-x-2">
                            <button
                                @click="editEmployee(employee)"
                                class="text-green-600 hover:text-green-900"
                            >
                                Edytuj
                            </button>
                            <button
                                @click="confirmDelete(employee)"
                                class="text-red-600 hover:text-red-900"
                            >
                                Usuń
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Modal do tworzenia/edycji pracownika -->
        <div v-if="showCreateModal || editedEmployee" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
            <div class="bg-white p-6 rounded-lg w-96">
                <h3 class="text-lg font-bold mb-4">
                    {{ editedEmployee ? 'Edytuj pracownika' : 'Dodaj pracownika' }}
                </h3>
                <form @submit.prevent="handleSubmit">
                    <div class="mb-4">
                        <label class="block text-sm font-medium text-gray-700">Numer</label>
                        <input
                            v-model="formData.enroll_number"
                            type="text"
                            required
                            :disabled="!!editedEmployee"
                            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                        />
                    </div>
                    <div class="mb-4">
                        <label class="block text-sm font-medium text-gray-700">Imię i nazwisko</label>
                        <input
                            v-model="formData.name"
                            type="text"
                            required
                            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                        />
                    </div>
                    <div class="mb-4">
                        <label class="block text-sm font-medium text-gray-700">PIN (opcjonalnie)</label>
                        <input
                            v-model="formData.password"
                            type="text"
                            maxlength="4"
                            pattern="[0-9]*"
                            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                        />
                    </div>
                    <div class="mb-4">
                        <label class="block text-sm font-medium text-gray-700">Numer karty (opcjonalnie)</label>
                        <input
                            v-model="formData.card_number"
                            type="text"
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
                            {{ editedEmployee ? 'Zapisz' : 'Dodaj' }}
                        </button>
                    </div>
                </form>
            </div>
        </div>

        <!-- Modal potwierdzenia usunięcia -->
        <div v-if="employeeToDelete" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
            <div class="bg-white p-6 rounded-lg w-96">
                <h3 class="text-lg font-bold mb-4">Potwierdź usunięcie</h3>
                <p class="mb-4">Czy na pewno chcesz usunąć pracownika "{{ employeeToDelete.name }}"?</p>
                <div class="flex justify-end space-x-2">
                    <button
                        @click="employeeToDelete = null"
                        class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
                    >
                        Anuluj
                    </button>
                    <button
                        @click="deleteEmployee"
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
import { useEmployeesStore } from '@/stores/employees';
import type { Employee } from '@/types/employee';

const employeesStore = useEmployeesStore();
const showCreateModal = ref(false);
const editedEmployee = ref<Employee | null>(null);
const employeeToDelete = ref<Employee | null>(null);

const formData = ref({
    enroll_number: '',
    name: '',
    password: '',
    card_number: '',
    privileges: 0,
    is_active: true
});

onMounted(() => {
    employeesStore.fetchEmployees();
});

function editEmployee(employee: Employee) {
    editedEmployee.value = employee;
    formData.value = {
        enroll_number: employee.enroll_number,
        name: employee.name,
        password: employee.password || '',
        card_number: employee.card_number || '',
        privileges: employee.privileges,
        is_active: employee.is_active
    };
    showCreateModal.value = true;
}

function confirmDelete(employee: Employee) {
    employeeToDelete.value = employee;
}

async function deleteEmployee() {
    if (employeeToDelete.value) {
        await employeesStore.deleteEmployee(employeeToDelete.value.id);
        employeeToDelete.value = null;
    }
}

function closeModal() {
    showCreateModal.value = false;
    editedEmployee.value = null;
    formData.value = {
        enroll_number: '',
        name: '',
        password: '',
        card_number: '',
        privileges: 0,
        is_active: true
    };
}

async function handleSubmit() {
    try {
        if (editedEmployee.value) {
            await employeesStore.updateEmployee(editedEmployee.value.id, formData.value);
        } else {
            await employeesStore.addEmployee(formData.value);
        }
        showCreateModal.value = false;
        editedEmployee.value = null;
        formData.value = {
            enroll_number: '',
            name: '',
            password: '',
            card_number: '',
            privileges: 0,
            is_active: true
        };
    } catch (error) {
        console.error('Wystąpił błąd podczas zapisu pracownika:', error);
    }
}
</script> 