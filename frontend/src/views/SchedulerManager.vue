<template>
  <div class="p-4">
    <h2 class="text-2xl font-bold mb-4">Zarządzanie zadaniami</h2>
    
    <div v-if="loading" class="text-center">
      <span class="loading loading-spinner loading-lg"></span>
    </div>
    
    <div v-else class="overflow-x-auto">
      <table class="table w-full">
        <thead>
          <tr>
            <th>Nazwa</th>
            <th>Następne uruchomienie</th>
            <th>Interwał (min)</th>
            <th>Status</th>
            <th>Akcje</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="job in jobs" :key="job.id">
            <td>{{ job.name }}</td>
            <td>{{ job.next_run_time || 'Wstrzymane' }}</td>
            <td>
              <input 
                type="number" 
                v-model="job.interval"
                class="input input-bordered w-24"
                :disabled="!job.enabled"
              />
            </td>
            <td>
              <label class="swap">
                <input 
                  type="checkbox" 
                  v-model="job.enabled"
                  @change="updateJob(job)"
                />
                <div class="swap-on">Aktywne</div>
                <div class="swap-off">Nieaktywne</div>
              </label>
            </td>
            <td>
              <button 
                class="btn btn-primary btn-sm"
                @click="runJobNow(job.id)"
              >
                Uruchom teraz
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { schedulerService } from '@/services/scheduler';

const jobs = ref([]);
const loading = ref(true);

const loadJobs = async () => {
  try {
    loading.value = true;
    jobs.value = await schedulerService.getJobs();
  } catch (error) {
    console.error('Błąd podczas ładowania zadań:', error);
  } finally {
    loading.value = false;
  }
};

const updateJob = async (job) => {
  try {
    await updateJob(job.id, {
      interval: job.interval,
      enabled: job.enabled
    });
    await loadJobs();
  } catch (error) {
    console.error('Błąd podczas aktualizacji zadania:', error);
  }
};

const runJobNow = async (jobId) => {
  try {
    await runJob(jobId);
    await loadJobs();
  } catch (error) {
    console.error('Błąd podczas uruchamiania zadania:', error);
  }
};

onMounted(loadJobs);
</script> 