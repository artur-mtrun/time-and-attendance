import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { AttendanceLog, AttendanceFilter } from '@/types/attendance.js';
import { attendanceService } from '@/services/attendance.js';

export const useAttendanceStore = defineStore('attendance', () => {
    const attendanceLogs = ref<AttendanceLog[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    async function fetchAttendanceLogs(filter: AttendanceFilter) {
        loading.value = true;
        error.value = null;
        try {
            attendanceLogs.value = await attendanceService.getAttendanceLogs(filter);
        } catch (e) {
            error.value = 'Nie udało się pobrać listy obecności';
            console.error(e);
        } finally {
            loading.value = false;
        }
    }

    async function fetchEmployeeAttendance(employeeId: number, filter: AttendanceFilter) {
        loading.value = true;
        error.value = null;
        try {
            attendanceLogs.value = await attendanceService.getEmployeeAttendance(employeeId, filter);
        } catch (e) {
            error.value = 'Nie udało się pobrać obecności pracownika';
            console.error(e);
        } finally {
            loading.value = false;
        }
    }

    return {
        attendanceLogs,
        loading,
        error,
        fetchAttendanceLogs,
        fetchEmployeeAttendance
    };
}); 