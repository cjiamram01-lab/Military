<script setup lang="ts">
import '@fontsource/sarabun/400.css'
import '@fontsource/sarabun/700.css'
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import {
	fetchDepartments,
	fetchEduLevels,
	fetchRegisterById,
	fetchStudentTypes,
	type Option,
	type ReportRecord,
} from '../register'
import { fetchAttachmentsByRegisterId, fetchDocumentTypes } from '../attachments'
import { formatThaiFullDate } from '../thaiDate'
import { formatThaiPersonalId } from '../thaiId'
import { publicAsset } from '../assetUrl'

const INSTITUTION_NAME = 'มหาวิทยาลัยราชภัฏนครราชสีมา'

const route = useRoute()
const registerId = Number(route.params.id)

const record = ref<ReportRecord | null>(null)
const eduLevels = ref<Option[]>([])
const studentTypes = ref<Option[]>([])
const departments = ref<Option[]>([])
const uploadedDocTypes = ref<Set<string>>(new Set())
const requiredDocuments = ref<Option[]>([])

const isLoading = ref(true)
const loadError = ref('')

function optionName(options: Option[], code?: string) {
	return options.find((opt) => opt.code === code)?.name ?? ''
}

const departmentName = computed(() => optionName(departments.value, record.value?.departmentCode))
const eduLevelName = computed(() => optionName(eduLevels.value, record.value?.eduLevel))
const studentTypeName = computed(() => optionName(studentTypes.value, record.value?.eduType))
const formattedBirthDate = computed(() =>
	record.value?.birthDate ? formatThaiFullDate(record.value.birthDate) : '',
)
const formattedPersonalId = computed(() =>
	record.value?.personalId ? formatThaiPersonalId(record.value.personalId) : '',
)
const hasEverRequested = computed(() => Boolean(record.value?.everRequest))

onMounted(async () => {
	if (!registerId) {
		loadError.value = 'ไม่พบรหัสคำขอผ่อนผัน'
		isLoading.value = false
		return
	}

	try {
		const [reportData, eduLevelOptions, studentTypeOptions, departmentOptions, docTypes, attachments] =
			await Promise.all([
				fetchRegisterById(registerId),
				fetchEduLevels(),
				fetchStudentTypes(),
				fetchDepartments(),
				fetchDocumentTypes(),
				fetchAttachmentsByRegisterId(registerId),
			])

		if (!reportData) {
			loadError.value = 'ไม่พบข้อมูลคำขอผ่อนผัน'
			return
		}

		record.value = reportData
		eduLevels.value = eduLevelOptions
		studentTypes.value = studentTypeOptions
		departments.value = departmentOptions
		requiredDocuments.value = docTypes.slice(0, 5)
		uploadedDocTypes.value = new Set(attachments.map((item) => item.docType))
	} catch (err) {
		loadError.value = err instanceof Error ? err.message : 'โหลดข้อมูลไม่สำเร็จ'
	} finally {
		isLoading.value = false
	}
})

function handlePrint() {
	window.print()
}
</script>

<template>
	<div class="print-page">
		<p v-if="isLoading">กำลังโหลดข้อมูล...</p>
		<p v-else-if="loadError" class="error">{{ loadError }}</p>

		<template v-else-if="record">
			<button type="button" class="print-button no-print" @click="handlePrint">พิมพ์เอกสาร</button>

			<div class="sheet">
				<div class="letterhead">
					<img :src="publicAsset('Royal.jpg')" alt="ตราครุฑ" class="emblem" />
					<h1>บันทึกข้อความ</h1>
				</div>

				<table class="memo-head">
					<tr>
						<th>ส่วนราชการ</th>
						<td>กองพัฒนานักศึกษา {{ INSTITUTION_NAME }}</td>
					</tr>
					<tr>
						<th>เรียน</th>
						<td>อธิการบดี{{ INSTITUTION_NAME }}</td>
					</tr>
					<tr>
						<th>เรื่อง</th>
						<td>ขอผ่อนผันตรวจเลือกเข้ารับราชการทหาร</td>
					</tr>
				</table>

				<div class="line two-col">
					<span>ข้าพเจ้า {{ record.studentName }}</span>
					<span>เลขบัตรประจำตัวประชาชน {{ formattedPersonalId }}</span>
				</div>

				<div class="line two-col">
					<span>วัน/เดือน/ปี เกิด {{ formattedBirthDate }}</span>
					<span>อายุ {{ record.age }} ปี</span>
				</div>

				<div class="line student-line">
					<span class="line-label">นักศึกษา</span>
					<span class="checkbox-item">
						<span class="box" :class="{ checked: record.eduType === '01' }"></span>
						ภาคปกติ ชั้นปีที่ ______
					</span>
					<span class="checkbox-item">
						<span class="box" :class="{ checked: record.eduType === '02' }"></span>
						ภาค กศ.ปช.
					</span>
					<span class="checkbox-item">
						<span class="box" :class="{ checked: record.eduType === '03' }"></span>
						ปริญญาโท รุ่นที่ ______
					</span>
					<span v-if="studentTypeName" class="edu-level-name">({{ studentTypeName }})</span>
				</div>

				<div class="line two-col">
					<span>สาขาวิชา {{ record.eduProgram }} ({{ departmentName }})</span>
					<span>รหัสประจำตัวนักศึกษา {{ record.studentCode }}</span>
				</div>

				<div class="line two-col">
					<span>&nbsp;</span>
					<span>หมายเลขโทรศัพท์ {{ record.telNo }}</span>
				</div>

				<div class="line student-line">
					<span class="line-label">ระดับ</span>
					<span class="checkbox-item">
						<span class="box" :class="{ checked: record.eduLevel === '01' }"></span>
						ปริญญาตรี 4 ปี
					</span>
					<span class="checkbox-item">
						<span class="box" :class="{ checked: record.eduLevel === '02' }"></span>
						ปริญญาตรี 5 ปี
					</span>
					<span class="checkbox-item">
						<span class="box" :class="{ checked: record.eduLevel === '03' }"></span>
						ปริญญาตรี 2 ปี (ต่อเนื่อง/เทียบโอน)
					</span>
					<span v-if="eduLevelName" class="edu-level-name">({{ eduLevelName }})</span>
				</div>

				<p class="paragraph">
					มีความประสงค์ขอให้มหาวิทยาลัย ฯ ทำการขอผ่อนผันการตรวจเลือกทหารกองเกินเข้ารับราชการทหาร
					กองประจำการ ในคราวที่มีคนพอ ตามมาตรา 29 (3) แห่งพระราชบัญญัติรับราชการทหาร พ.ศ.2497
					เนื่องจากข้าพเจ้า มีกำหนดที่ต้องเข้ารับการตรวจเลือกเข้ารับราชการทหาร ตามกำหนดในหมายเรียกฯ
					ของนายอำเภอภูมิลำเนาทหาร ประจำปี พ.ศ. {{ record.registYear }}
				</p>

				<div class="line">
					<span class="checkbox-item">
						<span class="box" :class="{ checked: !hasEverRequested }"></span>
						ข้าพเจ้าไม่เคยขอผ่อนผันมาก่อน
					</span>
				</div>
				<div class="line">
					<span class="checkbox-item">
						<span class="box" :class="{ checked: hasEverRequested }"></span>
						ข้าพเจ้าเคยขอผ่อนผันมาแล้ว {{ record.registYear }} ณ สถานศึกษา {{ INSTITUTION_NAME }}
					</span>
				</div>

				<p class="section-title">
					ภูมิลำเนาทหาร (ตาม สด.9) ของข้าพเจ้า บ้านเลขที่ {{ record.homeNo }} หมู่ที่
					{{ record.mooNo }} ถนน/ตรอก {{ record.street }}
				</p>
				<p class="paragraph">
					ตำบล/แขวง {{ record.subDistrict }} อำเภอ/เขต {{ record.district }} จังหวัด
					{{ record.province }} รหัสไปรษณีย์ {{ record.postalCode }}
				</p>

				<div class="line two-col">
					<span>ชื่อ-สกุล (บิดา) {{ record.fatherName }}</span>
					<span>หมายเลขโทรศัพท์ {{ record.fatherTel }}</span>
				</div>
				<div class="line two-col">
					<span>ชื่อ-สกุล (มารดา) {{ record.motherName }}</span>
					<span>หมายเลขโทรศัพท์ {{ record.motherTel }}</span>
				</div>

				<p class="section-title bold">หลักฐานที่ส่งประกอบขอผ่อนผันเข้ารับราชการทหาร</p>
				<ol class="doc-list">
					<li v-for="doc in requiredDocuments" :key="doc.code">
						<span class="box" :class="{ checked: uploadedDocTypes.has(doc.code) }"></span>
						{{ doc.name }}
					</li>
				</ol>

				<p class="closing">จึงเรียนมาเพื่อโปรดพิจารณา</p>
				<p class="closing">ขอแสดงความนับถือ</p>

				<div class="signature">
					<p>ลงชื่อ................................................ผู้ขอผ่อนผัน</p>
					<p>(................................................)</p>
				</div>
			</div>
		</template>
	</div>
</template>

<style scoped>
.print-page {
	min-height: 100svh;
	background: #e5e4e7;
	padding: 24px;
	box-sizing: border-box;
}

.print-button {
	display: block;
	margin: 0 auto 16px;
	font: inherit;
	font-weight: 500;
	padding: 10px 20px;
	border-radius: 4px;
	border: none;
	color: var(--accent-contrast);
	background: var(--accent);
	cursor: pointer;
}

.sheet {
	width: 210mm;
	min-height: 297mm;
	margin: 0 auto;
	padding: 5mm 18mm 20mm;
	box-sizing: border-box;
	background: #fff;
	color: #000;
	font-family: 'Sarabun', sans-serif;
	font-size: 15px;
	line-height: 1.7;
}

.letterhead {
	position: relative;
	text-align: center;
	margin-bottom: 12px;
}

.emblem {
	position: absolute;
	left: 0;
	top: 0;
	width: 50px;
	height: auto;
}

.letterhead h1 {
	font-size: 22px;
	font-weight: 700;
	margin: 0;
	color: #000;
}

.memo-head {
	width: 100%;
	border-collapse: collapse;
	margin-bottom: 12px;
}

.memo-head th {
	width: 110px;
	text-align: left;
	font-weight: 700;
	vertical-align: top;
	padding: 2px 8px 2px 0;
}

.memo-head td {
	padding: 2px 0;
}

.line {
	margin-bottom: 6px;
	display: flex;
	flex-wrap: wrap;
	gap: 8px 24px;
}

.two-col {
	justify-content: space-between;
}

.two-col span:first-child {
	flex: 1.4;
}

.two-col span:last-child {
	flex: 1;
}

.student-line {
	align-items: center;
}

.line-label {
	font-weight: 700;
	margin-right: 4px;
}

.checkbox-item {
	display: inline-flex;
	align-items: center;
	gap: 4px;
	white-space: nowrap;
}

.edu-level-name {
	color: #444;
}

.box {
	display: inline-block;
	width: 13px;
	height: 13px;
	border: 1px solid #000;
	flex-shrink: 0;
	text-align: center;
	line-height: 12px;
	font-size: 11px;
}

.box.checked::after {
	content: '\2713';
}

.paragraph {
	text-align: justify;
	margin: 10px 0;
}

.section-title {
	margin: 12px 0 4px;
}

.section-title.bold {
	font-weight: 700;
}

.doc-list {
	margin: 0 0 12px;
	padding-left: 24px;
}

.doc-list li {
	display: flex;
	align-items: center;
	gap: 6px;
	margin-bottom: 4px;
}

.closing {
	margin: 4px 0;
}

.signature {
	margin-top: 60px;
	text-align: center;
}

.error {
	color: #b3261e;
	text-align: center;
}

@page {
	size: A4;
	margin: 0;
}

@media print {
	.print-page {
		background: #fff;
		padding: 0;
	}

	.no-print {
		display: none;
	}

	.sheet {
		width: auto;
		min-height: 0;
		margin: 0;
		padding: 5mm 18mm 20mm;
	}
}
</style>
