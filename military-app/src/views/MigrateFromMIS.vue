<script setup lang="ts">
import { computed, ref } from 'vue'
import { migrateStudentSoldierFromNrru, type MigrateResult } from '../register'

const currentBuddhistYear = new Date().getFullYear() + 543

const orgYear = ref(currentBuddhistYear)
const activeYear = ref(currentBuddhistYear + 1)

const isLoading = ref(false)
const errorMessage = ref('')
const result = ref<MigrateResult | null>(null)

const canSubmit = computed(() => Boolean(orgYear.value && activeYear.value) && !isLoading.value)

const createdCount = computed(
	() => result.value?.history.filter((item) => item.action === 'create').length ?? 0,
)
const updatedCount = computed(
	() => result.value?.history.filter((item) => item.action === 'update').length ?? 0,
)
const failedCount = computed(
	() => result.value?.history.filter((item) => !item.result?.Flag).length ?? 0,
)

async function handleSubmit() {
	if (!canSubmit.value) return

	isLoading.value = true
	errorMessage.value = ''
	result.value = null

	try {
		result.value = await migrateStudentSoldierFromNrru(orgYear.value, activeYear.value)
	} catch (err) {
		errorMessage.value = err instanceof Error ? err.message : 'ย้ายข้อมูลไม่สำเร็จ'
	} finally {
		isLoading.value = false
	}
}
</script>

<template>
	<div class="page">
		<header class="page-header">
			<h1>ย้ายข้อมูลผู้ขอผ่อนผันจากระบบ MIS</h1>
		</header>

		<section class="card filters">
			<div class="field">
				<label for="orgYear">ปีเกิด (พ.ศ.)</label>
				<input
					id="orgYear"
					v-model.number="orgYear"
					type="number"
					inputmode="numeric"
					placeholder="เช่น 2549"
				/>
			</div>
			<div class="field">
				<label for="activeYear">ปีที่ขึ้นทะเบียน (พ.ศ.)</label>
				<input
					id="activeYear"
					v-model.number="activeYear"
					type="number"
					inputmode="numeric"
					placeholder="เช่น 2569"
				/>
			</div>
			<div class="actions">
				<button type="button" :disabled="!canSubmit" @click="handleSubmit">
					{{ isLoading ? 'กำลังย้ายข้อมูล...' : 'เริ่มย้ายข้อมูล' }}
				</button>
			</div>
		</section>

		<p v-if="errorMessage" class="error">{{ errorMessage }}</p>

		<section v-if="result" class="card summary">
			<div class="summary-item">
				<span class="summary-value">{{ result.history.length }}</span>
				<span class="summary-label">ทั้งหมด</span>
			</div>
			<div class="summary-item">
				<span class="summary-value">{{ createdCount }}</span>
				<span class="summary-label">เพิ่มใหม่</span>
			</div>
			<div class="summary-item">
				<span class="summary-value">{{ updatedCount }}</span>
				<span class="summary-label">อัปเดต</span>
			</div>
			<div class="summary-item" :class="{ 'summary-item--error': failedCount > 0 }">
				<span class="summary-value">{{ failedCount }}</span>
				<span class="summary-label">ล้มเหลว</span>
			</div>
		</section>

		<section v-if="result" class="card table-card">
			<div class="table-scroll">
				<table class="report-table">
					<thead>
						<tr>
							<th>No.</th>
							<th>รหัสนักศึกษา</th>
							<th>ปีที่ขึ้นทะเบียน</th>
							<th>การดำเนินการ</th>
							<th>สถานะ</th>
							<th>Id</th>
						</tr>
					</thead>
					<tbody>
						<tr v-if="!result.history.length">
							<td colspan="6" class="empty">ไม่พบข้อมูลสำหรับช่วงปีที่ระบุ</td>
						</tr>
						<tr v-for="(item, index) in result.history" :key="`${item.studentCode}-${index}`">
							<td>{{ index + 1 }}</td>
							<td>{{ item.studentCode }}</td>
							<td>{{ item.activeYear }}</td>
							<td>{{ item.action === 'create' ? 'เพิ่มใหม่' : 'อัปเดต' }}</td>
							<td :class="item.result?.Flag ? 'status-ok' : 'status-error'">
								{{ item.result?.Flag ? 'สำเร็จ' : item.result?.err || 'ล้มเหลว' }}
							</td>
							<td>{{ item.result?.Id ?? '-' }}</td>
						</tr>
					</tbody>
				</table>
			</div>
		</section>
	</div>
</template>

<style scoped>
.page {
	max-width: 1200px;
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
	min-width: 180px;
}

label {
	font-size: 14px;
	color: var(--text-h);
}

input {
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

.summary {
	display: flex;
	flex-wrap: wrap;
	gap: 24px;
}

.summary-item {
	display: flex;
	flex-direction: column;
	gap: 4px;
	min-width: 100px;
}

.summary-value {
	font-size: 24px;
	font-weight: 600;
	color: var(--text-h);
}

.summary-item--error .summary-value {
	color: #b3261e;
}

.summary-label {
	font-size: 13px;
	color: var(--text);
}

.table-card {
	padding: 0;
	overflow: hidden;
}

.table-scroll {
	overflow-x: auto;
	max-height: 60vh;
	overflow-y: auto;
}

.report-table {
	width: 100%;
	border-collapse: collapse;
	font-size: 13px;
	white-space: nowrap;
}

.report-table th,
.report-table td {
	border: 1px solid var(--border);
	padding: 6px 8px;
	text-align: center;
}

.report-table thead th {
	background: var(--accent-bg);
	color: var(--text-h);
	position: sticky;
	top: 0;
}

.status-ok {
	color: #1e7e34;
}

.status-error {
	color: #b3261e;
}

.empty {
	color: var(--text);
	padding: 24px 8px;
}

.error {
	color: #b3261e;
	margin-bottom: 16px;
}
</style>
