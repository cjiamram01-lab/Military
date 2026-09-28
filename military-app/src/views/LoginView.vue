<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { publicAsset } from '../assetUrl'
import { homeRouteName } from '../auth'

const userStore = useUserStore()
const router = useRouter()

const username = ref('')
const password = ref('')
const isSubmitting = ref(false)
const errorMessage = ref('')

async function handleSubmit() {
	if (!username.value || !password.value) return

	isSubmitting.value = true
	errorMessage.value = ''

	try {
		const user = await userStore.login(username.value, password.value)
		router.push({ name: homeRouteName(user) })
	} catch (err) {
		errorMessage.value = err instanceof Error ? err.message : 'Sign in failed'
	} finally {
		isSubmitting.value = false
	}
}
</script>

<template>
	<div class="login-page">
		<div class="login-panel">
			<img :src="publicAsset('thai_military_icon.png')" alt="" class="badge" />
			<h1>ระบบขอผ่อนผันการเกณฑ์ทหาร</h1>
			<p class="subtitle">เข้าสู่ระบบเพื่อยื่นคำขอผ่อนผันการเกณฑ์ทหาร</p>

			<form class="login-form" @submit.prevent="handleSubmit">
				<label for="username">ชื่อผู้ใช้งาน</label>
				<input
					id="username"
					v-model="username"
					type="text"
					autocomplete="username"
					required
				/>

				<label for="password">รหัสผ่าน</label>
				<input
					id="password"
					v-model="password"
					type="password"
					autocomplete="current-password"
					required
				/>

				<p v-if="errorMessage" class="error">{{ errorMessage }}</p>

				<button type="submit" :disabled="isSubmitting">
					{{ isSubmitting ? 'กำลังเข้าสู่ระบบ...' : 'เข้าสู่ระบบ' }}
				</button>
			</form>
		</div>
	</div>
</template>

<style scoped>
.login-page {
	min-height: 100svh;
	display: flex;
	align-items: center;
	justify-content: center;
	padding: 24px;
	box-sizing: border-box;
	background:
		linear-gradient(var(--bg), var(--bg)),
		repeating-linear-gradient(
			135deg,
			var(--accent-bg) 0 18px,
			transparent 18px 36px
		);
}

.login-panel {
	width: 100%;
	max-width: 380px;
	display: flex;
	flex-direction: column;
	align-items: center;
	text-align: center;
	background: var(--bg);
	border: 1px solid var(--border);
	border-top: 4px solid var(--accent);
	border-radius: 8px;
	box-shadow: var(--shadow);
	padding: 40px 32px 32px;
	box-sizing: border-box;
}

.badge {
	width: 88px;
	height: 88px;
	object-fit: contain;
	margin-bottom: 16px;
}

h1 {
	font-size: 26px;
	margin: 0 0 8px;
	text-transform: uppercase;
	letter-spacing: 0.5px;
}

.subtitle {
	margin-bottom: 32px;
}

.login-form {
	width: 100%;
	display: flex;
	flex-direction: column;
	gap: 6px;
	text-align: left;
}

label {
	font-size: 14px;
	color: var(--text-h);
	margin-top: 12px;
}

input {
	font: inherit;
	padding: 10px 12px;
	border-radius: 4px;
	border: 1px solid var(--border);
	background: var(--bg);
	color: var(--text-h);
}

input:focus-visible {
	outline: 2px solid var(--accent);
	outline-offset: 1px;
}

button {
	margin-top: 24px;
	font: inherit;
	font-weight: 500;
	letter-spacing: 0.5px;
	text-transform: uppercase;
	padding: 10px 12px;
	border-radius: 4px;
	border: none;
	color: var(--accent-contrast);
	background: var(--accent);
	cursor: pointer;
}

button:disabled {
	opacity: 0.6;
	cursor: not-allowed;
}

.error {
	color: #b3261e;
	font-size: 14px;
	margin-top: 8px;
}
</style>
