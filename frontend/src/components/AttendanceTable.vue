<template>
    <div class="p-4">
        <div class="flex justify-between items-center mb-4">
            <h2 class="text-2xl font-bold">Lista obecności</h2>
            <div class="flex space-x-4">
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
                    @click="$emit('filter', filter)"
                    class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                >
                    Filtruj
                </button>
            </div>
        </div>
        <div v-if="loading" class="text-center py-4">
            Ładowanie...
        </div>
        <div v-else-if="records.length === 0" class="text-center py-4">
            Brak danych do wyświetlenia.
        </div>
        <div v-else class="bg-white shadow-md rounded-lg">
            <table class="min-w-full">
                <thead>
                    <tr class="bg-gray-50">
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data i czas</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Numer pracownika</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Pracownik</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Czytnik</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Typ</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Weryfikacja</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="record in records" :key="record.id">
                        <td class="px-6 py-4 whitespace-nowrap">
                            {{ new Date(record.event_timestamp).toLocaleString() }}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">{{ record.enroll_number }}</td>
                        <td class="px-6 py-4 whitespace-nowrap">{{ record.employee_name || '-' }}</td>
                        <td class="px-6 py-4 whitespace-nowrap">{{ record.terminal_id }}</td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span :class="{
                                'text-green-600': record.in_out_mode === 1,
                                'text-red-600': record.in_out_mode === 2,
                                'text-yellow-600': record.in_out_mode === 3 || record.in_out_mode === 4
                            }">
                                {{ InOutModes[record.in_out_mode as InOutMode] }}
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">{{ VerifyModes[record.verify_mode as VerifyMode] }}</td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span :class="{
                                'px-2 py-1 rounded text-sm': true,
                                'bg-green-100 text-green-800': record.is_sync,
                                'bg-yellow-100 text-yellow-800': !record.is_sync
                            }">
                                {{ record.is_sync ? 'Zsynchronizowano' : 'Niezsynchornizowano' }}
                            </span>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script setup lang="ts">
import { defineProps, ref } from 'vue';
import { formatDateTime } from '@/utils/formatters';
import type { AttendanceRecord } from '@/types/attendance_all';
import { InOutModes, VerifyModes, InOutMode, VerifyMode } from '@/types/attendance';

const filter = ref({
    startDate: '',
    endDate: ''
});

defineProps<{
    records: AttendanceRecord[];
    loading?: boolean;
}>();
</script> 