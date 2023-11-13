import { createRouter, createWebHistory } from 'vue-router';


const routes = [
    {
        path: '/',
        name: 'home',
        component: _ => import('../pages/Flowchart.vue'),
    },
    {
        path: '/child',
        name: 'child',
        component: _ => import('../pages/Child.vue'),
    },
    {
        path: '/script',
        name: 'script',
        component: _ => import('../pages/Script.vue'),
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;