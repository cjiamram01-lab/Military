import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import Register from '../views/Register.vue'
import FileAttachment from '../views/FileAttachment.vue'
import PrintReport from '../views/PrintReport.vue'
import ReportStudentReg from '../views/ReportStudentReg.vue'
import MigrateFromMIS from '../views/MigrateFromMIS.vue'
import QueryUser from '../views/QueryUser.vue'
import StudentLayout from '../layouts/studentLayout.vue'
import AdminLayout from '../layouts/adminLayout.vue'
import { useUserStore } from '../stores/user'
import { homeRouteName, isAdmin } from '../auth'

const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: [
		{ path: '/', redirect: '/login' },
		{ path: '/login', name: 'login', component: LoginView },
		{
			path: '/print/:id',
			name: 'print',
			component: PrintReport,
			meta: { requiresAuth: true },
		},
		{
			path: '/',
			component: StudentLayout,
			meta: { requiresAuth: true },
			children: [
				{ path: 'student/registration', name: 'studentRegistration', component: Register },
				{ path: 'attachment', name: 'attachment', component: FileAttachment },
			],
		},
		{
			path: '/',
			component: AdminLayout,
			meta: { requiresAuth: true, requiresAdmin: true },
			children: [
				{
					path: 'admin/migrate-from-mis',
					name: 'migrateFromMis',
					component: MigrateFromMIS,
				},
				{
					path: 'report/student-by-district',
					name: 'reportStudentByDistrict',
					component: ReportStudentReg,
				},
				
				{
					path: 'admin/users',
					name: 'queryUser',
					component: QueryUser,
				},
			],
		},
	],
})

router.beforeEach((to) => {
	const userStore = useUserStore()

	if (to.meta.requiresAuth && !userStore.currentUser) {
		return { name: 'login' }
	}

	if (to.meta.requiresAdmin && !isAdmin(userStore.currentUser)) {
		return { name: 'studentRegistration' }
	}

	if (to.name === 'login' && userStore.currentUser) {
		return { name: homeRouteName(userStore.currentUser) }
	}
})

export default router
