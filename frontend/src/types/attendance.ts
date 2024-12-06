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
    2: "Wejście",
    3: "Wyjście",
    4: "Przerwa",
    5: "Powrót z przerwy"
} as const;

export type InOutMode = keyof typeof InOutModes;

export const VerifyModes = {
    1: "Odcisk palca",
    2: "Karta",
    3: "PIN",
    4: "Twarz"
} as const;

export type VerifyMode = keyof typeof VerifyModes; 