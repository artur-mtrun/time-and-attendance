<template>
  <nav class="bg-gray-800">
    <div class="max-w-7xl mx-auto px-4">
      <div class="flex items-center justify-between h-16">
        <div class="flex items-center">
          <router-link 
            to="/dashboard" 
            class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium"
          >
            Dashboard
          </router-link>
          <router-link 
            to="/users" 
            class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium"
          >
            Użytkownicy
          </router-link>
        </div>
        <div class="flex items-center">
          <button 
            @click="logout" 
            class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium"
          >
            Wyloguj
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const authStore = useAuthStore();

async function logout() {
  authStore.logout();
  router.push('/login');
}
</script> 