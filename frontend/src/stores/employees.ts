import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { Employee, CreateEmployeeData, UpdateEmployeeData } from '../types/employee.js';
import { employeeService } from '../services/employees.js';

export const useEmployeesStore = defineStore('employees', () => {
    const employees = ref<Employee[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    async function fetchEmployees() {
        loading.value = true;
        error.value = null;
        try {
            employees.value = await employeeService.getEmployees();
        } catch (e) {
            error.value = 'Nie udało się pobrać listy pracowników';
            console.error(e);
        } finally {
            loading.value = false;
        }
    }

    async function createEmployee(data: CreateEmployeeData) {
        try {
            const employee = await employeeService.createEmployee(data);
            employees.value.push(employee);
            return true;
        } catch (e) {
            error.value = 'Nie udało się utworzyć pracownika';
            console.error(e);
            return false;
        }
    }

    async function updateEmployee(id: number, data: UpdateEmployeeData) {
        try {
            const updatedEmployee = await employeeService.updateEmployee(id, data);
            const index = employees.value.findIndex(e => e.id === id);
            if (index !== -1) {
                employees.value[index] = updatedEmployee;
            }
            return true;
        } catch (e) {
            error.value = 'Nie udało się zaktualizować pracownika';
            console.error(e);
            return false;
        }
    }

    async function deleteEmployee(id: number) {
        try {
            await employeeService.deleteEmployee(id);
            employees.value = employees.value.filter(e => e.id !== id);
            return true;
        } catch (e) {
            error.value = 'Nie udało się usunąć pracownika';
            console.error(e);
            return false;
        }
    }

    return {
        employees,
        loading,
        error,
        fetchEmployees,
        createEmployee,
        updateEmployee,
        deleteEmployee
    };
}); 