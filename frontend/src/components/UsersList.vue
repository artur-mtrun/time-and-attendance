<template>
    <div class="p-4">
        <div class="flex justify-between items-center mb-4">
            <h2 class="text-2xl font-bold">Lista użytkowników</h2>
            <button
                @click="showCreateModal = true"
                class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
            >
                Dodaj użytkownika
            </button>
        </div>

        <div v-if="usersStore.loading" class="text-center py-4">
            Ładowanie...
        </div>

        <div v-else-if="usersStore.error" class="text-red-500 text-center py-4">
            {{ usersStore.error }}
        </div>

        <div v-else class="bg-white shadow-md rounded-lg">
            <table class="min-w-full">
                <thead>
                    <tr class="bg-gray-50">
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            ID
                        </th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Nazwa użytkownika
                        </th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Admin
                        </th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Data utworzenia
                        </th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Akcje
                        </th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="user in usersStore.users" :key="user.id">
                        <td class="px-6 py-4 whitespace-nowrap">{{ user.id }}</td>
                        <td class="px-6 py-4 whitespace-nowrap">{{ user.username }}</td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span :class="user.is_admin ? 'text-green-600' : 'text-red-600'">
                                {{ user.is_admin ? 'Tak' : 'Nie' }}
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            {{ new Date(user.created_at).toLocaleDateString() }}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <button
                                @click="editUser(user)"
                                class="text-blue-600 hover:text-blue-900 mr-2"
                            >
                                Edytuj
                            </button>
                            <button
                                @click="confirmDelete(user)"
                                class="text-red-600 hover:text-red-900"
                            >
                                Usuń
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Modal do tworzenia/edycji użytkownika -->
        <div v-if="showCreateModal || editedUser" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
            <div class="bg-white p-6 rounded-lg w-96">
                <h3 class="text-lg font-bold mb-4">
                    {{ editedUser ? 'Edytuj użytkownika' : 'Dodaj użytkownika' }}
                </h3>
                <form @submit.prevent="handleSubmit">
                    <div class="mb-4">
                        <label class="block text-sm font-medium text-gray-700">Nazwa użytkownika</label>
                        <input
                            v-model="formData.username"
                            type="text"
                            required
                            :disabled="!!editedUser"
                            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                        />
                    </div>
                    <div class="mb-4">
                        <label class="block text-sm font-medium text-gray-700">Hasło</label>
                        <input
                            v-model="formData.password"
                            type="password"
                            :required="!editedUser"
                            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                        />
                    </div>
                    <div class="mb-4">
                        <label class="flex items-center">
                            <input
                                v-model="formData.is_admin"
                                type="checkbox"
                                class="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                            />
                            <span class="ml-2 text-sm text-gray-600">Administrator</span>
                        </label>
                    </div>
                    <div class="flex justify-end space-x-2">
                        <button
                            type="button"
                            @click="closeModal"
                            class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
                        >
                            Anuluj
                        </button>
                        <button
                            type="submit"
                            class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
                        >
                            {{ editedUser ? 'Zapisz' : 'Dodaj' }}
                        </button>
                    </div>
                </form>
            </div>
        </div>

        <!-- Modal potwierdzenia usunięcia -->
        <div v-if="userToDelete" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
            <div class="bg-white p-6 rounded-lg w-96">
                <h3 class="text-lg font-bold mb-4">Potwierdź usunięcie</h3>
                <p class="mb-4">Czy na pewno chcesz usunąć użytkownika "{{ userToDelete.username }}"?</p>
                <div class="flex justify-end space-x-2">
                    <button
                        @click="userToDelete = null"
                        class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
                    >
                        Anuluj
                    </button>
                    <button
                        @click="deleteUser"
                        class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700"
                    >
                        Usuń
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useUsersStore } from '@/stores/users';
import type { User } from '@/types/auth';

const usersStore = useUsersStore();
const showCreateModal = ref(false);
const editedUser = ref<User | null>(null);
const userToDelete = ref<User | null>(null);
const formData = ref({
    username: '',
    password: '',
    is_admin: false
});

onMounted(() => {
    usersStore.fetchUsers();
});

function editUser(user: User) {
    editedUser.value = user;
    formData.value = {
        username: user.username,
        password: '',
        is_admin: user.is_admin
    };
}

function confirmDelete(user: User) {
    userToDelete.value = user;
}

async function deleteUser() {
    if (userToDelete.value) {
        await usersStore.deleteUser(userToDelete.value.id);
        userToDelete.value = null;
    }
}

function closeModal() {
    showCreateModal.value = false;
    editedUser.value = null;
    formData.value = {
        username: '',
        password: '',
        is_admin: false
    };
}

async function handleSubmit() {
    try {
        if (editedUser.value) {
            await usersStore.updateUser(editedUser.value.id, {
                password: formData.value.password || undefined,
                is_admin: formData.value.is_admin
            });
        } else {
            await usersStore.createUser({
                username: formData.value.username,
                password: formData.value.password,
                is_admin: formData.value.is_admin
            });
        }
        closeModal();
    } catch (error) {
        console.error('Failed to save user:', error);
    }
}
</script> 