export interface AttendanceRecord {
    id: number;
    enroll_number: string;
    employee_name: string | null;
    terminal_id: number;
    event_timestamp: string;
    in_out_mode: number;
    verify_mode: number;
    work_code: number;
    is_sync: boolean;
} 