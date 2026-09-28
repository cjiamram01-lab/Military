<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { formatThaiPersonalId } from '../thaiId'
import AttachmentModal from '../components/AttachmentModal.vue'
import {
	fetchDistricts,
	fetchProvinces,
	fetchStudentsByDistrict,
	type DistrictStudentRow,
	type Option,
} from '../register'

const currentBuddhistYear = new Date().getFullYear() + 543

const provinces = ref<Option[]>([])
const districts = ref<Option[]>([])
const provinceCode = ref('')
const districtCode = ref('')
const birthYear = ref('')

const rows = ref<DistrictStudentRow[]>([])
const hasSearched = ref(false)
const isLoading = ref(false)
const errorMessage = ref('')

const PAGE_SIZE_OPTIONS = [10, 25, 50, 100]
const pageSize = ref(25)
const currentPage = ref(1)

const totalPages = computed(() => Math.max(1, Math.ceil(rows.value.length / pageSize.value)))
const pageStart = computed(() => (currentPage.value - 1) * pageSize.value)
const pagedRows = computed(() => rows.value.slice(pageStart.value, pageStart.value + pageSize.value))
const pageEnd = computed(() => Math.min(pageStart.value + pageSize.value, rows.value.length))

// Window of page numbers around the current page, with 0 standing for an ellipsis.
const pageNumbers = computed(() => {
	const total = totalPages.value
	const current = currentPage.value
	const pages = new Set([1, total, current - 1, current, current + 1])
	const sorted = [...pages].filter((p) => p >= 1 && p <= total).sort((a, b) => a - b)
	const result: number[] = []
	sorted.forEach((p, i) => {
		if (i > 0 && p - sorted[i - 1] > 1) result.push(0)
		result.push(p)
	})
	return result
})

const attachmentRow = ref<DistrictStudentRow | null>(null)
const isAttachmentOpen = ref(false)

function openAttachments(row: DistrictStudentRow) {
	attachmentRow.value = row
	isAttachmentOpen.value = true
}

function goToPage(page: number) {
	currentPage.value = Math.min(Math.max(1, page), totalPages.value)
}

watch([rows, pageSize], () => {
	currentPage.value = 1
})

onMounted(async () => {
	provinces.value = await fetchProvinces()
	provinceCode.value = '19'
	await handleProvinceChange()
})

async function handleProvinceChange() {
	districtCode.value = ''
	districts.value = provinceCode.value ? await fetchDistricts(provinceCode.value) : []
}

function personalIdLabel(value: string) {
	return value ? formatThaiPersonalId(value) : ''
}

function ageFromBirthYear(year: string) {
	const y = Number(year)
	return y ? currentBuddhistYear - y : ''
}

const canSearch = () => Boolean(provinceCode.value  && birthYear.value)

async function handleSearch() {
	if (!canSearch()) return

	isLoading.value = true
	errorMessage.value = ''
	hasSearched.value = true

	try {
		rows.value = await fetchStudentsByDistrict(
			provinceCode.value,
			districtCode.value,
			birthYear.value,
		)
	} catch (err) {
		errorMessage.value = err instanceof Error ? err.message : 'โหลดข้อมูลไม่สำเร็จ'
		rows.value = []
	} finally {
		isLoading.value = false
	}
}

async function handleExport() {
	if (!rows.value.length) return

	const XLSX = await import('xlsx')

	const header = [
		'No.',
		'ชื่อ-สกุล',
		'เลขประจำตัวประชาชน',
		'เกิด พ.ศ.',
		'อายุ',
		'ถนน',
		'เลขที่',
		'หมู่ที่',
		'ตำบล',
		'อำเภอ',
		'จังหวัด',
		'บิดา',
		'มารดา',
		'หมายเหตุ',
	]

	const data = rows.value.map((row, index) => [
		index + 1,
		row.studentName,
		personalIdLabel(row.personalId),
		row.birthYear,
		ageFromBirthYear(row.birthYear),
		row.street ?? '',
		row.homeNo ?? '',
		row.mooNo ?? '',
		row.subDistrict ?? '',
		row.districtName ?? '',
		row.provinceName ?? '',
		row.fatherName ?? '',
		row.motherName ?? '',
		'',
	])

	const worksheet = XLSX.utils.aoa_to_sheet([header, ...data])
	const workbook = XLSX.utils.book_new()
	XLSX.utils.book_append_sheet(workbook, worksheet, 'รายชื่อ')
	XLSX.writeFile(workbook, `รายชื่อผู้เกณฑ์ทหาร_${birthYear.value}.xlsx`)
}
</script>

<template>
	<div class="page">
		<header class="page-header">
			<h1>รายงานผู้ขึ้นทะเบียนทหารตามภูมิลำเนา</h1>
		</header>

		<section class="card filters">
			<div class="field">
				<label for="province">จังหวัด</label>
				<select id="province" v-model="provinceCode" @change="handleProvinceChange">
					<option value="">***จังหวัด***</option>
					<option v-for="opt in provinces" :key="opt.code" :value="opt.code">
						{{ opt.name }}
					</option>
				</select>
			</div>
			<div class="field">
				<label for="district">อำเภอ</label>
				<select id="district" v-model="districtCode" :disabled="!provinceCode">
					<option value="">***อำเภอ***</option>
					<option v-for="opt in districts" :key="opt.code" :value="opt.code">
						{{ opt.name }}
					</option>
				</select>
			</div>
			<div class="field">
				<label for="birthYear">ปีเกิด (พ.ศ.)</label>
				<input id="birthYear" v-model="birthYear" type="text" inputmode="numeric" placeholder="เช่น 2545" />
			</div>
			<div class="actions">
				<button type="button" :disabled="!canSearch() || isLoading" @click="handleSearch">
					{{ isLoading ? 'กำลังค้นหา...' : 'ค้นหา' }}
				</button>
				<button type="button" class="secondary" :disabled="!rows.length" @click="handleExport">
					ส่งออก Excel
				</button>
			</div>
		</section>

		<p v-if="errorMessage" class="error">{{ errorMessage }}</p>

		<section class="card table-card">
			<div class="table-scroll">
				<table class="report-table">
					<thead>
						<tr>
							<th rowspan="2">No.</th>
							<th rowspan="2">ชื่อ-สกุล</th>
							<th rowspan="2">เลขประจำตัวประชาชน</th>
							<th rowspan="2">เกิด พ.ศ.</th>
							<th rowspan="2">อายุ</th>
							<th colspan="6">ภูมิลำเนาทหาร</th>
							<th colspan="2">ชื่อ</th>
							<th rowspan="2">หมายเหตุ</th>
							<th rowspan="2">เอกสาร</th>
						</tr>
						<tr>
							<th>ถนน</th>
							<th>เลขที่</th>
							<th>หมู่ที่</th>
							<th>ตำบล</th>
							<th>อำเภอ</th>
							<th>จังหวัด</th>
							<th>บิดา</th>
							<th>มารดา</th>
						</tr>
					</thead>
					<tbody>
						<tr v-if="!rows.length">
							<td colspan="15" class="empty">
								{{ hasSearched ? 'ไม่พบข้อมูล' : 'กรุณาเลือกจังหวัด อำเภอ และปีเกิด แล้วกดค้นหา' }}
							</td>
						</tr>
						<tr v-for="(row, index) in pagedRows" :key="`${row.studentCode}-${pageStart + index}`">
							<td>{{ pageStart + index + 1 }}</td>
							<td>{{ row.studentName }}</td>
							<td>{{ personalIdLabel(row.personalId) }}</td>
							<td>{{ row.birthYear }}</td>
							<td>{{ ageFromBirthYear(row.birthYear) }}</td>
							<td>{{ row.street }}</td>
							<td>{{ row.homeNo }}</td>
							<td>{{ row.mooNo }}</td>
							<td>{{ row.subDistrict }}</td>
							<td>{{ row.districtName }}</td>
							<td>{{ row.provinceName }}</td>
							<td>{{ row.fatherName }}</td>
							<td>{{ row.motherName }}</td>
							<td></td>
							<td>
								<button type="button" class="secondary doc-btn" @click="openAttachments(row)">
									เอกสาร ({{ row.attachments?.length ?? 0 }})
								</button>
							</td>
						</tr>
					</tbody>
				</table>
			</div>

			<div v-if="rows.length" class="pager">
				<div class="pager-info">
					แสดง {{ pageStart + 1 }}–{{ pageEnd }} จาก {{ rows.length }} รายการ
				</div>
				<div class="pager-controls">
					<label class="page-size">
						แถวต่อหน้า
						<select v-model.number="pageSize">
							<option v-for="size in PAGE_SIZE_OPTIONS" :key="size" :value="size">{{ size }}</option>
						</select>
					</label>
					<button type="button" class="secondary page-btn" :disabled="currentPage === 1" @click="goToPage(currentPage - 1)">
						ก่อนหน้า
					</button>
					<template v-for="(page, i) in pageNumbers" :key="`${page}-${i}`">
						<span v-if="page === 0" class="ellipsis">…</span>
						<button
							v-else
							type="button"
							class="secondary page-btn"
							:class="{ active: page === currentPage }"
							:aria-current="page === currentPage ? 'page' : undefined"
							@click="goToPage(page)"
						>
							{{ page }}
						</button>
					</template>
					<button type="button" class="secondary page-btn" :disabled="currentPage === totalPages" @click="goToPage(currentPage + 1)">
						ถัดไป
					</button>
				</div>
			</div>
		</section>

		<AttachmentModal
			v-model:visible="isAttachmentOpen"
			:title="attachmentRow ? `เอกสาร/หลักฐาน — ${attachmentRow.studentName}` : undefined"
			:attachments="attachmentRow?.attachments ?? []"
		/>
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

select,
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

button.secondary {
	color: var(--text-h);
	background: var(--code-bg);
	border: 1px solid var(--border);
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
}

.report-table td {
	white-space: normal;
}

.pager {
	display: flex;
	flex-wrap: wrap;
	align-items: center;
	justify-content: space-between;
	gap: 12px;
	padding: 12px 16px;
	font-size: 13px;
	color: var(--text);
}

.pager-controls {
	display: flex;
	flex-wrap: wrap;
	align-items: center;
	gap: 6px;
}

.page-size {
	display: flex;
	align-items: center;
	gap: 6px;
	margin-right: 8px;
	font-size: 13px;
}

.page-size select {
	padding: 4px 6px;
}

.page-btn {
	min-width: 34px;
	padding: 5px 10px;
	font-size: 13px;
}

button.page-btn.active {
	color: var(--accent-contrast);
	background: var(--accent);
	border-color: var(--accent);
}

.ellipsis {
	padding: 0 4px;
}

.doc-btn {
	padding: 4px 10px;
	font-size: 12px;
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
