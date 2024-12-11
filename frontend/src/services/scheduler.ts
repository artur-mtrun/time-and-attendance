import axios from '../plugins/axios.js';

class SchedulerService {
    async getJobs() {
        const response = await axios.get('/api/jobs');
        return response.data;
    }

    async updateJob(data: { id: string; interval: number; enabled: boolean }) {
        const response = await axios.put(`/api/jobs/${data.id}`, {
            interval: data.interval,
            enabled: data.enabled
        });
        return response.data;
    }

    async runJob(jobId: string) {
        const response = await axios.post(`/api/jobs/${jobId}/run`);
        return response.data;
    }
}

export const schedulerService = new SchedulerService();