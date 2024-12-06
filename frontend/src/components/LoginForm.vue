<template>
    <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div class="max-w-md w-full space-y-8">
            <div>
                <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
                    Zaloguj się do systemu
                </h2>
            </div>
            <form class="mt-8 space-y-6" @submit.prevent="handleSubmit">
                <div v-if="error" class="text-red-500 text-center">
                    {{ error }}
                </div>
                <div class="rounded-md shadow-sm -space-y-px">
                    <div>
                        <label for="username" class="sr-only">Nazwa użytkownika</label>
                        <input
                            id="username"
                            v-model="username"
                            name="username"
                            type="text"
                            required
                            class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                            placeholder="Nazwa użytkownika"
                        />
                    </div>
                    <div>
                        <label for="password" class="sr-only">Hasło</label>
                        <input
                            id="password"
                            v-model="password"
                            name="password"
                            type="password"
                            required
                            class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                            placeholder="Hasło"
                        />
                    </div>
                </div>

                <div>
                    <button
                        type="submit"
                        :disabled="loading"
                        class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                    >
                        {{ loading ? 'Logowanie...' : 'Zaloguj się' }}
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const username = ref('');
const password = ref('');
const error = ref('');
const loading = ref(false);

async function handleSubmit() {
    loading.value = true;
    error.value = '';
    
    try {
        const success = await authStore.login(username.value, password.value);
        if (success) {
            router.push('/dashboard');
        } else {
            error.value = 'Logowanie nie powiodło się';
        }
    } catch (e) {
        error.value = 'Nieprawidłowa nazwa użytkownika lub hasło';
    } finally {
        loading.value = false;
    }
}
</script> 