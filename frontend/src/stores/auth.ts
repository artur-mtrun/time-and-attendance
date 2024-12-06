import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { User } from '../types/auth.js';
import { authService } from '../services/auth.js';

export const useAuthStore = defineStore('auth', () => {
    const user = ref<User | null>(null);
    const loading = ref(true);

    async function login(username: string, password: string) {
        try {
            await authService.login({ username, password });
            await loadUser();
            return true;
        } catch (error) {
            console.error('Login failed:', error);
            return false;
        }
    }

    async function loadUser() {
        try {
            if (authService.getToken()) {
                const userData = await authService.getCurrentUser();
                user.value = userData;
            }
        } catch (error) {
            console.error('Failed to load user:', error);
            user.value = null;
        } finally {
            loading.value = false;
        }
    }

    function logout() {
        authService.logout();
        user.value = null;
    }

    return {
        user,
        loading,
        login,
        logout,
        loadUser
    };
}); 