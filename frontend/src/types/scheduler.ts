export interface Job {
    id: string;
    name: string;
    next_run_time: string | null;
    interval: number;
    enabled: boolean;
} 