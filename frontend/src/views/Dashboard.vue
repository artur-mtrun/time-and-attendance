<template>
  <div class="min-h-screen bg-gray-100">
    <nav class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <h1 class="text-xl font-semibold">Dashboard</h1>
          </div>
          <div class="flex items-center">
            <span class="mr-4">{{ user?.username }}</span>
            <button
              @click="handleLogout"
              class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
            >
              Wyloguj
            </button>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <h2 class="text-2xl font-bold mb-4">Witaj, {{ user?.username }}!</h2>
        <!-- Tutaj dodaj zawartość dashboardu -->
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'

const router = useRouter()
const authStore = useAuthStore()
const { user } = storeToRefs(authStore)

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script> 