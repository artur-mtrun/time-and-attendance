import axios from 'axios';

const axiosInstance = axios.create({
    baseURL: 'http://localhost:8000',
    timeout: 10000,  // dodajemy timeout 10 sekund
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
});

// ... reszta kodu ... 