import axios from 'axios';
import router from '../router/index.js';

const instance = axios.create({
    baseURL: 'http://localhost:8000',
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    },
    withCredentials: true
});

// Interceptor do dodawania tokenu
instance.interceptors.request.use(config => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    console.log('Request:', {
        method: config.method,
        url: config.url,
        baseURL: config.baseURL,
        headers: config.headers
    });
    return config;
});

// Dodajemy interceptor do logowania odpowiedzi i obsługi błędów autoryzacji
instance.interceptors.response.use(
    response => {
        console.log('Response:', {
            status: response.status,
            data: response.data,
            headers: response.headers
        });
        return response;
    },
    error => {
        console.error('Response Error:', {
            status: error.response?.status,
            data: error.response?.data,
            config: error.config
        });

        // Obsługa błędu 401 Unauthorized
        if (error.response && error.response.status === 401) {
            console.log('Unauthorized - clearing token and redirecting to login');
            localStorage.removeItem('token');
            router.push('/login');
        }

        return Promise.reject(error);
    }
);

export default instance; 