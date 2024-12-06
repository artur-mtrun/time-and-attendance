export interface AttendanceLog {
    id: number;
    employee_id: number;
    terminal_id: number;
    event_timestamp: string;
    in_out_mode: number;
    verify_mode: number;
    work_code: number;
    employee_name: string;
    terminal_name: string;
    created_at: string;
    updated_at: string;
}

export interface AttendanceFilter {
    startDate: string;
    endDate: string;
}

// Mapowanie typów zdarzeń
export const InOutModes = {
    1: 'Wejście',
    2: 'Wyjście',
    3: 'Przerwa',
    4: 'Powrót z przerwy'
} as const;

export const VerifyModes = {
    1: 'Odcisk palca',
    2: 'Karta',
    3: 'PIN',
    4: 'Twarz'
} as const; 