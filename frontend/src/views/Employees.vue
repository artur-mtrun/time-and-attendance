<template>
    <div>
        <h1>Pracownicy</h1>
        <employee-list 
            :employees="employees" 
            @refresh="loadEmployees"
        />
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import EmployeeList from '@/components/EmployeesList.vue';
import { employeeService } from '../services/employees';
import type { Employee } from '@/types/employee';

const employees = ref<Employee[]>([]);

const loadEmployees = async () => {
    try {
        employees.value = await employeeService.getEmployees();
    } catch (error) {
        console.error('Błąd podczas ładowania pracowników:', error);
    }
};

onMounted(() => {
    loadEmployees();
});
</script> 