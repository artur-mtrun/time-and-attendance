export interface LoginRequest {
    username: string;
    password: string;
}

export interface LoginResponse {
    access_token: string;
    token_type: string;
}

export interface User {
    id: number;
    username: string;
    is_admin: boolean;
    created_at: string;
    updated_at: string;
} 