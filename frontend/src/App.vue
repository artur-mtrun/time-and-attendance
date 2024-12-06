<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Górny pasek nawigacji -->
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <h1 class="text-xl font-bold">Dashboard</h1>
            </div>
            <!-- Menu nawigacyjne -->
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8" v-if="authStore.user">
              <router-link 
                to="/dashboard" 
                class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
              >
                Dashboard
              </router-link>
              <router-link 
                to="/users" 
                class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
              >
                Użytkownicy
              </router-link>
            </div>
          </div>
          <!-- Prawy panel z nazwą użytkownika i przyciskiem wylogowania -->
          <div class="flex items-center" v-if="authStore.user">
            <span class="text-gray-500 mr-4">{{ authStore.user.username }}</span>
            <button 
              @click="handleLogout" 
              class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
            >
              Wyloguj
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Główna zawartość -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <router-view></router-view>
    </main>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const handleLogout = () => {
  authStore.logout();
  router.push('/login');
};
</script>
