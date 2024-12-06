import axios from '../plugins/axios.js';
import type { AttendanceLog, AttendanceFilter } from '../types/attendance.ts';

export const attendanceService = {
    async getAttendanceLogs(filter: AttendanceFilter): Promise<AttendanceLog[]> {
        const response = await axios.get<AttendanceLog[]>('/api/attendance', {
            params: {
                start_date: filter.startDate,
                end_date: filter.endDate
            }
        });
        return response.data;
    },

    async getEmployeeAttendance(employeeId: number, filter: AttendanceFilter): Promise<AttendanceLog[]> {
        const response = await axios.get<AttendanceLog[]>(`/api/attendance/employee/${employeeId}`, {
            params: {
                start_date: filter.startDate,
                end_date: filter.endDate
            }
        });
        return response.data;
    }
}; 