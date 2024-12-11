<template>
    <div>
        <h1>Rejestracja czasu pracy (wszystkie)</h1>
        <attendance-table 
            :records="records" 
            :loading="loading"
            @filter="handleFilter"
        />
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import AttendanceTable from '@/components/AttendanceTable.vue';
import { attendanceAllService } from '@/services/attendance_all';
import type { AttendanceRecord } from '@/types/attendance_all';

const records = ref<AttendanceRecord[]>([]);
const loading = ref(false);

const loadRecords = async (filter?: { startDate: string; endDate: string }) => {
    loading.value = true;
    try {
        records.value = await attendanceAllService.getAttendanceAll(filter);
    } catch (error) {
        console.error('Błąd podczas ładowania rekordów:', error);
    } finally {
        loading.value = false;
    }
};

const handleFilter = (filter: { startDate: string; endDate: string }) => {
    loadRecords(filter);
};

onMounted(() => {
    loadRecords();
});
</script> 