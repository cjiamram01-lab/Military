<script setup lang="ts">
import { ref } from 'vue'
import { queryUsers, setUserPosition, type UserRecord } from '../users'

const POSITION_OPTIONS = [
	{ code: 'Admin', name: 'ผู้ดูแลระบบ' },
	{ code: 'user', name: 'ผู้ใช้งานทั่วไป' },
]

const keyword = ref('')
const users = ref<UserRecord[]>([])
const isLoading = ref(false)
const hasSearched = ref(false)
const errorMessage = ref('')

const savingUserId = ref<number | null>(null)
const saveError = ref('')

async function handleSearch() {
	if (!keyword.value.trim()) return

	isLoading.value = true
	errorMessage.value = ''
	saveError.value = ''
	hasSearched.value = true

	try {
		users.value = await queryUsers(keyword.value.trim())
	} catch (err) {
		errorMessage.value = err instanceof Error ? err.message : 'ค้นหาไม่สำเร็จ'
		users.value = []
	} finally {
		isLoading.value = false
	}
}

async function handlePositionChange(user: UserRecord, event: Event) {
	const newPosition = (event.target as HTMLSelectElement).value
	const previousPosition = user.position

	user.position = newPosition
	savingUserId.value = user.id
	saveError.value = ''

	try {
		await setUserPosition(user.id, newPosition)
	} catch (err) {
		user.position = previousPosition
		saveError.value = err instanceof Error ? err.message : 'อัปเดตตำแหน่งไม่สำเร็จ'
	} finally {
		savingUserId.value = null
	}
}
</script>

<template>
	<div class="page">
		<header class="page-header">
			<h1>ค้นหาผู้ใช้งาน</h1>
		</header>

		<section class="card filters">
			<div class="field">
				<label for="keyword">คำค้นหา</label>
				<input
					id="keyword"
					v-model="keyword"
					type="text"
					placeholder="ชื่อผู้ใช้ หรือ ชื่อ-สกุล"
					@keyup.enter="handleSearch"
				/>
			</div>
			<div class="actions">
				<button type="button" :disabled="!keyword.trim() || isLoading" @click="handleSearch">
					{{ isLoading ? 'กำลังค้นหา...' : 'ค้นหา' }}
				</button>
			</div>
		</section>

		<p v-if="errorMessage" class="error">{{ errorMessage }}</p>
		<p v-if="saveError" class="error">{{ saveError }}</p>

		<section class="card table-card">
			<div class="table-scroll">
				<table class="user-table">
					<thead>
						<tr>
							<th></th>
							<th>ชื่อผู้ใช้</th>
							<th>ชื่อ-สกุล</th>
							<th>รายละเอียด</th>
							<th>ตำแหน่ง</th>
						</tr>
					</thead>
					<tbody>
						<tr v-if="!users.length">
							<td colspan="5" class="empty">
								{{ hasSearched ? 'ไม่พบผู้ใช้งาน' : 'กรุณากรอกคำค้นหาแล้วกดค้นหา' }}
							</td>
						</tr>
						<tr v-for="user in users" :key="user.id">
							<td>
								<span class="avatar" role="img" :aria-label="user.fullname">
									<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
										<circle cx="12" cy="8" r="4" />
										<path d="M4 20c0-4 4-6 8-6s8 2 8 6" stroke-linecap="round" stroke-linejoin="round" />
									</svg>
								</span>
							</td>
							<td>{{ user.username }}</td>
							<td>{{ user.fullname }}</td>
							<td>{{ user.description }}</td>
							<td>
								<select
									:value="user.position"
									:disabled="savingUserId === user.id"
									@change="handlePositionChange(user, $event)"
								>
									<option v-for="opt in POSITION_OPTIONS" :key="opt.code" :value="opt.code">
										{{ opt.name }}
									</option>
								</select>
							</td>
						</tr>
					</tbody>
				</table>
			</div>
		</section>
	</div>
</template>

<style scoped>
.page {
	max-width: 1000px;
	margin: 0 auto;
	padding: 24px 16px 48px;
	box-sizing: border-box;
}

.page-header {
	margin-bottom: 20px;
}

.page-header h1 {
	font-size: 20px;
	margin: 0;
}

.card {
	background: var(--bg);
	border: 1px solid var(--border);
	border-radius: 8px;
	padding: 24px;
	margin-bottom: 24px;
}

.filters {
	display: flex;
	flex-wrap: wrap;
	align-items: flex-end;
	gap: 16px;
}

.field {
	display: flex;
	flex-direction: column;
	gap: 4px;
	min-width: 240px;
	flex: 1;
}

label {
	font-size: 14px;
	color: var(--text-h);
}

input,
select {
	font: inherit;
	padding: 8px 10px;
	border-radius: 4px;
	border: 1px solid var(--border);
	background: var(--bg);
	color: var(--text-h);
	box-sizing: border-box;
}

.actions {
	display: flex;
	gap: 12px;
}

button {
	font: inherit;
	font-weight: 500;
	padding: 9px 20px;
	border-radius: 4px;
	border: none;
	color: var(--accent-contrast);
	background: var(--accent);
	cursor: pointer;
	white-space: nowrap;
}

button:disabled {
	opacity: 0.5;
	cursor: not-allowed;
}

.table-card {
	padding: 0;
	overflow: hidden;
}

.table-scroll {
	overflow-x: auto;
}

.user-table {
	width: 100%;
	border-collapse: collapse;
	font-size: 14px;
}

.user-table th,
.user-table td {
	border: 1px solid var(--border);
	padding: 8px 10px;
	text-align: left;
}

.user-table thead th {
	background: var(--accent-bg);
	color: var(--text-h);
}

.avatar {
	width: 36px;
	height: 36px;
	border-radius: 50%;
	background: var(--accent-bg);
	color: var(--text);
	display: flex;
	align-items: center;
	justify-content: center;
}

.avatar svg {
	width: 20px;
	height: 20px;
}

.empty {
	color: var(--text);
	padding: 24px 8px;
	text-align: center;
}

.error {
	color: #b3261e;
	margin-bottom: 16px;
}
</style>
