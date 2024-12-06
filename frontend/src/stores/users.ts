import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { User } from '../types/auth.js';
import { userService, type CreateUserData, type UpdateUserData } from '../services/users.js';

export const useUsersStore = defineStore('users', () => {
    const users = ref<User[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    async function fetchUsers() {
        loading.value = true;
        error.value = null;
        try {
            users.value = await userService.getUsers();
        } catch (e) {
            error.value = 'Nie udało się pobrać listy użytkowników';
            console.error(e);
        } finally {
            loading.value = false;
        }
    }

    async function createUser(userData: CreateUserData) {
        try {
            const newUser = await userService.createUser(userData);
            users.value.push(newUser);
            return true;
        } catch (e) {
            error.value = 'Nie udało się utworzyć użytkownika';
            console.error(e);
            return false;
        }
    }

    async function updateUser(userId: number, userData: UpdateUserData) {
        try {
            const updatedUser = await userService.updateUser(userId, userData);
            const index = users.value.findIndex(u => u.id === userId);
            if (index !== -1) {
                users.value[index] = updatedUser;
            }
            return true;
        } catch (e) {
            error.value = 'Nie udało się zaktualizować użytkownika';
            console.error(e);
            return false;
        }
    }

    async function deleteUser(userId: number) {
        try {
            await userService.deleteUser(userId);
            users.value = users.value.filter(u => u.id !== userId);
            return true;
        } catch (e) {
            error.value = 'Nie udało się usunąć użytkownika';
            console.error(e);
            return false;
        }
    }

    return {
        users,
        loading,
        error,
        fetchUsers,
        createUser,
        updateUser,
        deleteUser
    };
}); 