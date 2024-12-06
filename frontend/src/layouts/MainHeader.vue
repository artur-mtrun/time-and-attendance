<template>
  <div class="min-h-screen bg-gray-100">
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <h1 class="text-xl font-bold">ZK Teco Reader Manager</h1>
            </div>
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <router-link 
                to="/dashboard" 
                class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="{ 'border-indigo-500 text-gray-900': $route.path === '/dashboard' }"
              >
                Dashboard
              </router-link>

              <!-- Dropdown menu dla Pracowników -->
              <div class="relative group">
                <router-link 
                  to="/employees" 
                  class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                  :class="{ 'border-indigo-500 text-gray-900': $route.path.startsWith('/employees') }"
                >
                  Pracownicy
                </router-link>
                <div class="absolute left-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 hidden group-hover:block z-50">
                  <div class="py-1">
                    <router-link 
                      to="/employees" 
                      class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      :class="{ 'bg-gray-100': $route.path === '/employees' }"
                    >
                      Lista pracowników
                    </router-link>
                    <router-link 
                      to="/employees/sync" 
                      class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      :class="{ 'bg-gray-100': $route.path === '/employees/sync' }"
                    >
                      Synchronizacja
                    </router-link>
                  </div>
                </div>
              </div>

              <router-link 
                to="/terminals" 
                class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="{ 'border-indigo-500 text-gray-900': $route.path === '/terminals' }"
              >
                Czytniki
              </router-link>
              <router-link 
                to="/users" 
                class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="{ 'border-indigo-500 text-gray-900': $route.path === '/users' }"
              >
                Użytkownicy
              </router-link>
              <router-link 
                to="/attendance" 
                class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="{ 'border-indigo-500 text-gray-900': $route.path === '/attendance' }"
              >
              Obecności
              </router-link>
              <router-link 
                to="/employees/sync" 
                class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="{ 'border-indigo-500 text-gray-900': $route.path === '/employees/sync' }"
              >
              Pracownicy - synchro
              </router-link>
            </div>
          </div>
          <div class="flex items-center">
            <span class="text-gray-500 mr-4">{{ authStore.user?.username }}</span>
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

    <main class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
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

<style scoped>
.group:hover .hidden {
    display: block;
}
</style> 