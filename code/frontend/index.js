import { createRouter, createWebHistory, createWebHashHistory, RouterLink } from "vue-router"
import Library from '../pages/Library.vue'
import Search from '../pages/Search.vue'
// import Account from '../pages/Account.vue'
import Home from '../pages/Home.vue'
import  Settings from '../pages/Settings.vue'
import Login from '../pages/Login.vue'
import Register from '../pages/Register.vue'
import  Paper from '../pages/PaperView.vue'
const router = createRouter({
    base: import.meta.env.BASE_URL,
    history: createWebHashHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            component: Home
        },
        {
            path: '/library',
            component: Library
        },
        // {
        //     path: '/account',
        //     component: Account
        // },
        {
            path: '/login',
            component: Login
        },
        {
            path: '/register',
            component: Register
        },
        {
            path: '/home',
            component: Home
        },
        {
            path: '/search',
            component: Search
        },
        {
            path: '/settings',
            component: Settings
        },
        {
            path: '/paperview',
            component: Paper
        }
    ]
})

export default router
