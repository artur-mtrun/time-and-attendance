<template>
    <div class="p-4">
        <div class="flex justify-between items-center mb-4">
            <h2 class="text-2xl font-bold">Lista obecności</h2>
            <div class="flex space-x-4">
                <div class="flex items-center space-x-2">
                    <label class="text-sm font-medium text-gray-700">Pracownik:</label>
                    <select 
                        v-model="filter.employeeId"
                        class="rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                        @change="fetchData"
                    >
                        <option value="">Wszyscy</option>
                        <option 
                            v-for="employee in employeesStore.employees" 
                            :key="employee.id" 
                            :value="employee.id"
                        >
                            {{ employee.name }}
                        </option>
                    </select>
                </div>

                <div class="flex items-center space-x-2">
                    <label class="text-sm font-medium text-gray-700">Od:</label>
                    <input
                        type="date"
                        v-model="filter.startDate"
                        class="rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    />
                </div>
                <div class="flex items-center space-x-2">
                    <label class="text-sm font-medium text-gray-700">Do:</label>
                    <input
                        type="date"
                        v-model="filter.endDate"
                        class="rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    />
                </div>
                <button
                    @click="fetchData"
                    class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                >
                    Filtruj
                </button>
            </div>
        </div>

        <div v-if="attendanceStore.loading" class="text-center py-4">
            Ładowanie...
        </div>

        <div v-else-if="attendanceStore.error" class="text-red-500 text-center py-4">
            {{ attendanceStore.error }}
        </div>

        <div v-else class="bg-white shadow-md rounded-lg">
            <table class="min-w-full">
                <thead>
                    <tr class="bg-gray-50">
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data i czas</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Pracownik</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Czytnik</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Typ</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Weryfikacja</th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="log in attendanceStore.attendanceLogs" :key="log.id">
                        <td class="px-6 py-4 whitespace-nowrap">
                            {{ new Date(log.event_timestamp).toLocaleString() }}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">{{ log.employee_name }}</td>
                        <td class="px-6 py-4 whitespace-nowrap">{{ log.terminal_name }}</td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span :class="{
                                'text-green-600': log.in_out_mode === 1,
                                'text-red-600': log.in_out_mode === 2,
                                'text-yellow-600': log.in_out_mode === 3 || log.in_out_mode === 4
                            }">
                                {{ InOutModes[log.in_out_mode as InOutMode] }}
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">{{ VerifyModes[log.verify_mode as VerifyMode] }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useAttendanceStore } from '@/stores/attendance';
import { useEmployeesStore } from '@/stores/employees';
import { InOutModes, VerifyModes, type InOutMode, type VerifyMode } from '@/types/attendance';

const attendanceStore = useAttendanceStore();
const employeesStore = useEmployeesStore();

const getCurrentMonthRange = () => {
    const now = new Date();
    const startDate = new Date(now.getFullYear(), now.getMonth(), 1);
    const endDate = new Date(now.getFullYear(), now.getMonth() + 1, 0);
    
    return {
        startDate: startDate.toISOString().split('T')[0],
        endDate: endDate.toISOString().split('T')[0]
    };
};

const filter = ref({
    employeeId: '',
    ...getCurrentMonthRange()
});

const fetchData = async () => {
    const employeeId = Number(filter.value.employeeId);
    if (employeeId) {
        await attendanceStore.fetchEmployeeAttendance(employeeId, filter.value);
    } else {
        await attendanceStore.fetchAttendanceLogs(filter.value);
    }
};

onMounted(async () => {
    console.log('Mounting AttendanceList...');
    await employeesStore.fetchActiveEmployees();
    console.log('Active employees:', employeesStore.employees);
    await fetchData();
});
</script> 