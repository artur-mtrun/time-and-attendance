export interface Terminal {
    id: number;
    number: number;
    name: string;
    ip_address: string;
    port: number;
    is_active: boolean;
    is_main: boolean;
    last_sync_at: string | null;
    created_at: string;
    updated_at: string;
}

export interface CreateTerminalData {
    number: number;
    name: string;
    ip_address: string;
    port: number;
    is_active: boolean;
    is_main: boolean;
}

export interface UpdateTerminalData {
    name?: string;
    ip_address?: string;
    port?: number;
    is_active?: boolean;
    is_main?: boolean;
}

export interface TerminalFormData {
    number: number;
    name: string;
    ip_address: string;
    port: number;
    is_active: boolean;
    is_main: boolean;
} 