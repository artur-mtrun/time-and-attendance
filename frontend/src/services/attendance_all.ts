import axiosInstance from '../plugins/axios.js';
import type { AttendanceRecord } from '@/types/attendance_all.js';

export const attendanceAllService = {
    async getAttendanceAll(filter?: { startDate: string; endDate: string }) {
        try {
            const params = new URLSearchParams();
            if (filter) {
                params.append('start_date', filter.startDate);
                params.append('end_date', filter.endDate);
            }
            
            const response = await axiosInstance.get<AttendanceRecord[]>('/api/attendance-all', { 
                params
            });
            
            return response.data;
        } catch (error) {
            console.error('Error fetching attendance:', error);
            throw error;
        }
    }
}; 