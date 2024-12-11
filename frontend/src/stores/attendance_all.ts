import { defineStore } from 'pinia';
import { attendanceAllService } from '@/services/attendance_all.js';
import type { AttendanceRecord } from '@/types/attendance_all.js';

export const useAttendanceAllStore = defineStore('attendanceAll', {
    state: () => ({
        records: [] as AttendanceRecord[],
        loading: false,
        error: null as string | null,
    }),

    actions: {
        async fetchAttendanceAll() {
            this.loading = true;
            try {
                const data = await attendanceAllService.getAttendanceAll();
                this.records = data || []; // Upewnij się, że zawsze mamy tablicę
                this.error = null;
            } catch (error: any) {
                this.error = error.message;
                this.records = [];
                console.error('Błąd podczas pobierania rekordów:', error);
            } finally {
                this.loading = false;
            }
        },
    },
});