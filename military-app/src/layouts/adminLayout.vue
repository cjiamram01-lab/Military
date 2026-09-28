<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { publicAsset } from '../assetUrl'

const userStore = useUserStore()
const router = useRouter()

const menuItems = [
	{ name: 'reportStudentByDistrict', label: 'ทะเบียน' },
	{ name: 'migrateFromMis', label: 'ย้ายข้อมูลจาก MIS' },
	{ name: 'queryUser', label: 'จัดการผู้ใช้งาน' },
]

const isMenuOpen = ref(false)

function handleLogout() {
	isMenuOpen.value = false
	userStore.logout()
	router.push({ name: 'login' })
}
</script>

<template>
	<div class="layout">
		<header class="topbar">
			<div class="brand">
				<img :src="publicAsset('military_header_icon.png')" alt="" class="badge" />
				<span class="brand-text">ผู้ดูแลระบบ</span>
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
		</header>

		<div class="body">
			<aside class="sidebar" :class="{ open: isMenuOpen }">
				<div class="sidebar-brand">
					<img :src="publicAsset('military_header_icon.png')" alt="" class="badge" />
					<span class="brand-text">ผู้ดูแลระบบ</span>
				</div>

				<nav class="side-nav">
					<RouterLink
						v-for="item in menuItems"
						:key="item.name"
						:to="{ name: item.name }"
						class="side-link"
						@click="isMenuOpen = false"
					>
						{{ item.label }}
					</RouterLink>
				</nav>

				<div class="sidebar-footer">
					<span class="account-name">
						{{ userStore.currentUser?.fullname || userStore.currentUser?.username }}
					</span>
					<button type="button" class="side-link logout" @click="handleLogout">
						ออกจากระบบ
					</button>
				</div>
			</aside>

			<main class="content">
				<RouterView />
			</main>
		</div>
	</div>
</template>

<style scoped>
.layout {
	min-height: 100svh;
	display: flex;
	flex-direction: column;
}

.body {
	flex: 1;
	display: flex;
	min-height: 0;
}

.topbar {
	display: none;
	align-items: center;
	gap: 12px;
	padding: 10px 16px;
	background: var(--bg);
	border-bottom: 3px solid var(--accent);
}

.brand,
.sidebar-brand {
	display: flex;
	align-items: center;
	gap: 10px;
	font-weight: 500;
}

.brand {
	flex: 1;
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
	display: flex;
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

.sidebar {
	width: 240px;
	flex-shrink: 0;
	display: flex;
	flex-direction: column;
	gap: 16px;
	padding: 16px 12px;
	background: var(--bg);
	border-right: 1px solid var(--border);
	border-top: 3px solid var(--accent);
}

.sidebar-brand {
	padding: 4px 8px 12px;
	border-bottom: 1px solid var(--border);
}

.side-nav {
	display: flex;
	flex-direction: column;
	gap: 4px;
	flex: 1;
}

.side-link {
	display: block;
	width: 100%;
	box-sizing: border-box;
	padding: 10px 14px;
	border: none;
	border-radius: 4px;
	background: none;
	font: inherit;
	font-size: 14px;
	text-align: left;
	color: var(--text);
	text-decoration: none;
	cursor: pointer;
}

.side-link:hover {
	background: var(--accent-bg);
	color: var(--text-h);
}

.side-link.router-link-active {
	background: var(--accent-bg);
	color: var(--accent);
	font-weight: 500;
}

.sidebar-footer {
	display: flex;
	flex-direction: column;
	gap: 8px;
	padding-top: 12px;
	border-top: 1px solid var(--border);
}

.account-name {
	padding: 0 14px;
	font-size: 13px;
	color: var(--text-h);
}

.logout {
	border: 1px solid var(--border);
	background: var(--code-bg);
	color: var(--text-h);
}

.logout:hover {
	border-color: var(--accent-border);
}

.content {
	flex: 1;
	min-width: 0;
}

@media (max-width: 720px) {
	.topbar {
		display: flex;
	}

	.body {
		flex-direction: column;
	}

	.sidebar {
		display: none;
		width: auto;
		border-right: none;
		border-top: none;
		border-bottom: 1px solid var(--border);
	}

	.sidebar.open {
		display: flex;
	}

	.sidebar-brand {
		display: none;
	}
}
</style>
