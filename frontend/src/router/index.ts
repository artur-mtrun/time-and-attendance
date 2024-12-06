import { createRouter, createWebHistory } from 'vue-router';
import { authService } from '@/services/auth';
import LoginForm from '@/components/LoginForm.vue';
import MainHeader from '@/layouts/MainHeader.vue';

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            redirect: '/dashboard'
        },
        {
            path: '/login',
            name: 'login',
            component: LoginForm,
            meta: { requiresAuth: false }
        },
        {
            path: '/',
            component: MainHeader,
            meta: { requiresAuth: true },
            children: [
                {
                    path: 'dashboard',
                    name: 'dashboard',
                    component: () => import('@/views/Dashboard.vue')
                },
                {
                    path: 'users',
                    name: 'users',
                    component: () => import('@/components/UsersList.vue')
                },
                {
                    path: 'terminals',
                    name: 'terminals',
                    component: () => import('@/components/TerminalsList.vue')
                },
                {
                    path: 'employees',
                    name: 'employees',
                    component: () => import('@/components/EmployeesList.vue')
                },
                {
                    path: 'attendance',
                    name: 'attendance',
                    component: () => import('@/components/AttendanceList.vue')
                }
            ]
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