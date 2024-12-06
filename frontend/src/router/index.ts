import { createRouter, createWebHistory } from 'vue-router';
import { authService } from '@/services/auth';

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            redirect: '/login'
        },
        {
            path: '/login',
            name: 'login',
            component: () => import('../components/LoginForm.vue'),
            meta: { requiresAuth: false }
        },
        {
            path: '/dashboard',
            name: 'dashboard',
            component: () => import('../views/Dashboard.vue'),
            meta: { requiresAuth: true }
        }
    ]
});

router.beforeEach((to, from, next) => {
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
    const token = authService.getToken();

    if (requiresAuth && !token) {
        next('/login');
    } else if (to.path === '/login' && token) {
        next('/dashboard');
    } else {
        next();
    }
});

export default router; 