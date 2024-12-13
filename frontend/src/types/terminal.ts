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

export interface SyncResult {
  status: string;
  message: string;
  stats: {
    terminal_id: number;
    terminal_name: string;
    total_employees: number;
    synced_employees: number;
    sync_details: {
      status: string;
      message: string;
      updated_count: number;
    };
    changes: SyncChange[];
  };
}

export interface SyncChange {
  type: 'add' | 'update';
  employee: string;
  enroll_number: string;
  message?: string;
  changes?: string[];
} 