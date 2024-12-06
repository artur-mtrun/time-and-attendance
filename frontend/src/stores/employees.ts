import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { Employee, CreateEmployeeData, UpdateEmployeeData } from '../types/employee.js';
import { employeeService } from '../services/employees.js';
import axios from 'axios';

export const useEmployeesStore = defineStore('employees', () => {
    const employees = ref<Employee[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    async function fetchEmployees() {
        try {
            const data = await employeeService.getEmployees();
            employees.value = data;
            return data;
        } catch (error) {
            console.error('Błąd podczas pobierania pracowników:', error);
            throw error;
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

    async function fetchFromMainTerminal() {
        loading.value = true;
        error.value = null;
        try {
            const syncResult = await employeeService.checkSync();
            
            if (syncResult.to_add.length > 0 || syncResult.to_update.length > 0) {
                return {
                    message: 'Znaleziono różnice w danych pracowników',
                    to_add: syncResult.to_add,
                    to_update: syncResult.to_update,
                    summary: syncResult.summary
                };
            }
            
            return null;
        } catch (err: any) {
            error.value = err.response?.data?.detail || 'Nie udało się pobrać pracowników z terminala wzorcowego';
            throw err;
        } finally {
            loading.value = false;
        }
    }

    async function addEmployee(employeeData: Partial<Employee>) {
        try {
            const response = await axios.post('/api/employees', employeeData);
            await fetchEmployees();
            return response.data;
        } catch (error) {
            console.error('Błąd podczas dodawania pracownika:', error);
            throw error;
        }
    }

    async function sendToTerminals(data: { terminalIds: number[], employeeIds: number[] }) {
        try {
            await employeeService.sendToTerminals(data);
            return true;
        } catch (error) {
            console.error('Błąd podczas wysyłania do terminali:', error);
            throw error;
        }
    }

    async function checkSync() {
        try {
            const result = await employeeService.checkSync();
            return {
                message: result.message,
                summary: result.summary,
                to_add: result.to_add,
                to_update: result.to_update
            };
        } catch (e) {
            error.value = 'Nie udało się sprawdzić zmian';
            throw e;
        }
    }

    async function confirmSync() {
        loading.value = true;
        try {
            await employeeService.confirmSync();
            await fetchEmployees();
            return true;
        } catch (e) {
            error.value = 'Nie udało się zatwierdzić zmian';
            throw e;
        } finally {
            loading.value = false;
        }
    }

    return {
        employees,
        loading,
        error,
        fetchEmployees,
        createEmployee,
        updateEmployee,
        deleteEmployee,
        fetchFromMainTerminal,
        addEmployee,
        sendToTerminals,
        checkSync,
        confirmSync
    };
}); 