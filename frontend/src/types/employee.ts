export interface Employee {
    id: number;
    enroll_number: string;
    name: string;
    password?: string;
    card_number?: string;
    privileges: number;
    is_active: boolean;
    created_at: string;
    updated_at: string;
}

export interface CreateEmployeeData {
    enroll_number: string;
    name: string;
    password?: string;
    card_number?: string;
    privileges: number;
    is_active: boolean;
}

export interface UpdateEmployeeData {
    name?: string;
    password?: string;
    card_number?: string;
    privileges?: number;
    is_active?: boolean;
} 