<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { publicAsset } from '../assetUrl'
import { isAdmin } from '../auth'

const userStore = useUserStore()
const router = useRouter()

const navItems = [
	{ name: 'studentRegistration', label: 'ข้อมูลนักศึกษา (ผู้ขอผ่อนผัน)' },
	{ name: 'attachment', label: 'เอกสาร/หลักฐาน' },
]

const adminMenu = computed(() => {
	if (!isAdmin(userStore.currentUser)) return null

	return {
		label: 'ผู้ดูแลระบบ',
		children: [
			{ name: 'reportStudentByDistrict', label: 'ทะเบียน' },
			{ name: 'migrateFromMis', label: 'ย้ายข้อมูลจาก MIS' },
			{ name: 'queryUser', label: 'จัดการผู้ใช้งาน' },
		]
	}
})

const isMenuOpen = ref(false)
const isAdminMenuOpen = ref(false)

function closeMenus() {
	isMenuOpen.value = false
	isAdminMenuOpen.value = false
}

function handleLogout() {
	closeMenus()
	userStore.logout()
	router.push({ name: 'login' })
}
</script>

<template>
	<div class="layout">
		<header class="topbar">
			<div class="brand">
				<img :src="publicAsset('military_header_icon.png')" alt="" class="badge" />
				<span class="brand-text">ระบบขอผ่อนผันการเกณฑ์ทหาร</span>
			</div>

			<button
				type="button"
				class="menu-toggle"
				:aria-expanded="isMenuOpen"
				aria-label="เปิดเมนู"
				@click="isMenuOpen = !isMenuOpen"
			>
				<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
					<line x1="4" y1="6" x2="20" y2="6" />
					<line x1="4" y1="12" x2="20" y2="12" />
					<line x1="4" y1="18" x2="20" y2="18" />
				</svg>
			</button>

			<nav class="nav" :class="{ open: isMenuOpen }">
				<RouterLink
					v-for="item in navItems"
					:key="item.name"
					:to="{ name: item.name }"
					class="nav-link"
					@click="isMenuOpen = false"
				>
					{{ item.label }}
				</RouterLink>

				<div v-if="adminMenu" class="nav-dropdown" :class="{ open: isAdminMenuOpen }">
					<button
						type="button"
						class="nav-link nav-dropdown-toggle"
						:aria-expanded="isAdminMenuOpen"
						@click="isAdminMenuOpen = !isAdminMenuOpen"
					>
						{{ adminMenu.label }}
						<svg class="chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
							<polyline points="6 9 12 15 18 9" />
						</svg>
					</button>
					<div class="nav-dropdown-menu">
						<RouterLink
							v-for="child in adminMenu.children"
							:key="child.name"
							:to="{ name: child.name }"
							class="nav-dropdown-link"
							@click="closeMenus()"
						>
							{{ child.label }}
						</RouterLink>
					</div>
				</div>
			</nav>

			<div class="account" :class="{ open: isMenuOpen }">
				<span class="account-name">
					{{ userStore.currentUser?.fullname || userStore.currentUser?.username }}
				</span>
				<button type="button" class="logout" @click="handleLogout">ออกจากระบบ</button>
			</div>
		</header>

		<main class="content">
			<RouterView />
		</main>
	</div>
</template>

<style scoped>
.layout {
	min-height: 100svh;
	display: flex;
	flex-direction: column;
}

.topbar {
	display: flex;
	align-items: center;
	gap: 24px;
	flex-wrap: wrap;
	padding: 10px 24px;
	background: var(--bg);
	border-bottom: 3px solid var(--accent);
}

.brand {
	display: flex;
	align-items: center;
	gap: 10px;
	font-weight: 500;
}

.badge {
	width: 42px;
	height: 24px;
	flex-shrink: 0;
	object-fit: cover;
	object-position: center;
}

.brand-text {
	font-size: 16px;
	color: var(--text-h);
}

.menu-toggle {
	display: none;
	align-items: center;
	justify-content: center;
	border: none;
	background: none;
	padding: 6px;
	color: var(--text-h);
	cursor: pointer;
}

.menu-toggle svg {
	width: 24px;
	height: 24px;
}

.nav {
	display: flex;
	gap: 4px;
	flex-wrap: wrap;
	flex: 1;
}

.nav-link {
	padding: 8px 14px;
	border-radius: 4px;
	color: var(--text);
	text-decoration: none;
	font-size: 14px;
}

.nav-link:hover {
	background: var(--accent-bg);
	color: var(--text-h);
}

.nav-link.router-link-active {
	background: var(--accent-bg);
	color: var(--accent);
	font-weight: 500;
}

.nav-button {
	opacity: 0.5;
	cursor: not-allowed;
}

.nav-button:hover {
	background: none;
	color: var(--text);
}

.nav-dropdown {
	position: relative;
}

.nav-dropdown-toggle {
	display: flex;
	align-items: center;
	gap: 6px;
	font: inherit;
	border: none;
	background: none;
	cursor: pointer;
}

.chevron {
	width: 14px;
	height: 14px;
	transition: transform 0.15s ease;
}

.nav-dropdown.open .chevron {
	transform: rotate(180deg);
}

.nav-dropdown-menu {
	display: none;
	flex-direction: column;
	position: absolute;
	top: 100%;
	left: 0;
	min-width: 180px;
	margin-top: 4px;
	padding: 4px;
	background: var(--bg);
	border: 1px solid var(--border);
	border-radius: 4px;
	box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
	z-index: 10;
}

.nav-dropdown.open .nav-dropdown-menu {
	display: flex;
}

.nav-dropdown-link {
	padding: 8px 14px;
	border-radius: 4px;
	color: var(--text);
	text-decoration: none;
	font-size: 14px;
}

.nav-dropdown-link:hover {
	background: var(--accent-bg);
	color: var(--text-h);
}

.nav-dropdown-link.router-link-active {
	background: var(--accent-bg);
	color: var(--accent);
	font-weight: 500;
}

.account {
	display: flex;
	align-items: center;
	gap: 12px;
}

.account-name {
	font-size: 14px;
	color: var(--text-h);
}

.logout {
	font: inherit;
	font-size: 13px;
	padding: 6px 12px;
	border-radius: 4px;
	border: 1px solid var(--border);
	background: var(--code-bg);
	color: var(--text-h);
	cursor: pointer;
}

.logout:hover {
	border-color: var(--accent-border);
}

.content {
	flex: 1;
}

@media (max-width: 720px) {
	.topbar {
		gap: 12px;
	}

	.menu-toggle {
		display: flex;
	}

	.brand {
		flex: 1;
	}

	.nav,
	.account {
		display: none;
		flex-basis: 100%;
	}

	.nav.open,
	.account.open {
		display: flex;
	}

	.nav.open {
		flex-direction: column;
	}

	.nav-dropdown-menu {
		position: static;
		box-shadow: none;
		margin-top: 0;
		margin-left: 12px;
	}

	.account.open {
		justify-content: space-between;
		padding-top: 8px;
		border-top: 1px solid var(--border);
	}

	.account-name {
		display: block;
	}
}
</style>
