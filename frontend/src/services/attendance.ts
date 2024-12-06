import axios from '../plugins/axios';
import type { AttendanceLog, AttendanceFilter } from '@/types/attendance';

export const attendanceService = {
    async getAttendanceLogs(filter: AttendanceFilter): Promise<AttendanceLog[]> {
        const response = await axios.get<AttendanceLog[]>('/attendance', {
            params: {
                start_date: filter.startDate,
                end_date: filter.endDate
            }
        });
        return response.data;
    },

    async getEmployeeAttendance(employeeId: number, filter: AttendanceFilter): Promise<AttendanceLog[]> {
        const response = await axios.get<AttendanceLog[]>(`/attendance/employee/${employeeId}`, {
            params: {
                start_date: filter.startDate,
                end_date: filter.endDate
            }
        });
        return response.data;
    }
}; 