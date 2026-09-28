<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { formatThaiPersonalId, isValidThaiPersonalId } from '../thaiId'
import ThaiDateInput from '../components/ThaiDateInput.vue'
import {
	fetchDepartments,
	fetchDistricts,
	fetchEduLevels,
	fetchProvinces,
	fetchRegisterId,
	fetchStudentByCode,
	fetchStudentTypes,
	submitRegistration,
	updateRegistration,
	type Option,
} from '../register'

const userStore = useUserStore()
const router = useRouter()

const currentBuddhistYear = new Date().getFullYear() + 543

const registrationId = ref<number | null>(userStore.currentUser?.registerId ?? null)
const existingEverSchool = ref(false)
const existingIsAprove = ref(false)

const studentCode = ref(userStore.currentUser?.username ?? '')
const studentName = ref(userStore.currentUser?.fullname ?? '')
const personalIdDigits = ref('')
const birthDate = ref('')
const telNo = ref('')

const eduType = ref('')
const eduLevel = ref('')
const departmentCode = ref('')
const eduProgram = ref('')

const street = ref('')
const homeNo = ref('')
const mooNo = ref('')
const subDistrict = ref('')
const provinceCode = ref('')
const districtCode = ref('')
const postalCode = ref('')
const fatherName = ref('')
const fatherTel = ref('')
const motherName = ref('')
const motherTel = ref('')

const everRequest = ref(false)
const everRequestDetail = ref('')
const description = ref('')

const provinces = ref<Option[]>([])
const districts = ref<Option[]>([])
const departments = ref<Option[]>([])
const eduLevels = ref<Option[]>([])
const studentTypes = ref<Option[]>([])

const isLoading = ref(true)
const isSubmitting = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const personalId = computed({
	get: () => formatThaiPersonalId(personalIdDigits.value),
	set: (value: string) => {
		personalIdDigits.value = value.replace(/\D/g, '').slice(0, 13)
	},
})

const personalIdError = computed(() => {
	if (!personalIdDigits.value) return ''
	if (personalIdDigits.value.length < 13) return 'กรุณากรอกเลขบัตรประชาชนให้ครบ 13 หลัก'
	return isValidThaiPersonalId(personalIdDigits.value) ? '' : 'เลขบัตรประชาชนไม่ถูกต้อง'
})

const age = computed(() => {
	if (!birthDate.value) return null
	const birth = new Date(birthDate.value)
	if (Number.isNaN(birth.getTime())) return null
	const today = new Date()
	let years = today.getFullYear() - birth.getFullYear()
	const hasHadBirthdayThisYear =
		today.getMonth() > birth.getMonth() ||
		(today.getMonth() === birth.getMonth() && today.getDate() >= birth.getDate())
	if (!hasHadBirthdayThisYear) years -= 1
	return years
})

async function selectProvince(code: string, presetDistrict = '') {
	provinceCode.value = code
	districts.value = code ? await fetchDistricts(code) : []
	districtCode.value = presetDistrict
}

async function handleProvinceChange() {
	await selectProvince(provinceCode.value)
}

async function loadExistingRegistration() {
	if (!studentCode.value || !userStore.currentUser?.registerId) return

	const existing = await fetchStudentByCode(studentCode.value)
	if (!existing) return

	registrationId.value = existing.id
	studentName.value = existing.studentName ?? studentName.value
	personalIdDigits.value = existing.personalId ?? ''
	birthDate.value = existing.birthDate ? existing.birthDate.slice(0, 10) : ''
	telNo.value = existing.telNo ?? ''
	eduType.value = existing.eduType ?? ''
	eduLevel.value = existing.eduLevel ?? ''
	departmentCode.value = existing.departmentCode ?? ''
	eduProgram.value = existing.eduProgram ?? ''
	street.value = existing.street ?? ''
	homeNo.value = existing.homeNo ?? ''
	mooNo.value = existing.mooNo ?? ''
	subDistrict.value = existing.subDistrict ?? ''
	postalCode.value = existing.postalCode ?? ''
	fatherName.value = existing.fatherName ?? ''
	fatherTel.value = existing.fatherTel ?? ''
	motherName.value = existing.motherName ?? ''
	motherTel.value = existing.motherTel ?? ''
	description.value = existing.description ?? ''
	everRequest.value = Boolean(existing.everRequest)
	existingEverSchool.value = Boolean(existing.everSchool)
	existingIsAprove.value = Boolean(existing.isAprove)

	await selectProvince(existing.province ?? '', existing.district ?? '')
}

onMounted(async () => {
	const [provinceOptions, departmentOptions, eduLevelOptions, studentTypeOptions] =
		await Promise.all([
			fetchProvinces(),
			fetchDepartments(),
			fetchEduLevels(),
			fetchStudentTypes(),
		])
	provinces.value = provinceOptions
	departments.value = departmentOptions
	eduLevels.value = eduLevelOptions
	studentTypes.value = studentTypeOptions

	try {
		await loadExistingRegistration()
	} finally {
		isLoading.value = false
	}
})

function handlePrint() {
	if (!registrationId.value) return
	//alert(`registrationId: ${registrationId.value}`)
	const url = router.resolve({ name: 'print', params: { id: registrationId.value } }).href
	window.open(url, '_blank')
}

async function handleSubmit() {
	if (!isValidThaiPersonalId(personalIdDigits.value) || !birthDate.value || age.value === null)
		return

	isSubmitting.value = true
	errorMessage.value = ''
	successMessage.value = ''

	let fullDescription = description.value
	if (everRequest.value && everRequestDetail.value) {
		fullDescription = `เคยผ่อนผันมาแล้ว: ${everRequestDetail.value}\n${fullDescription}`.trim()
	}

	const payload = {
		id: registrationId.value ?? 0,
		studentCode: studentCode.value,
		studentName: studentName.value,
		personalId: personalIdDigits.value,
		birthYear: new Date(birthDate.value).getFullYear() + 543,
		age: age.value,
		street: street.value,
		homeNo: homeNo.value,
		mooNo: mooNo.value,
		subDistrict: subDistrict.value,
		district: districtCode.value,
		province: provinceCode.value,
		postalCode: postalCode.value,
		fatherName: fatherName.value,
		motherName: motherName.value,
		description: fullDescription,
		fatherTel: fatherTel.value,
		motherTel: motherTel.value,
		birthDate: new Date(birthDate.value).toISOString(),
		departmentCode: departmentCode.value,
		telNo: telNo.value,
		eduLevel: eduLevel.value,
		eduProgram: eduProgram.value,
		registYear: String(currentBuddhistYear),
		eduType: eduType.value,
		everRequest: everRequest.value,
		everSchool: existingEverSchool.value,
		isAprove: existingIsAprove.value,
	}

	try {
		if (registrationId.value) {
			await updateRegistration(registrationId.value, payload)
		} else {
			await submitRegistration(payload)
		}
		registrationId.value = await fetchRegisterId(studentCode.value)
		successMessage.value = 'บันทึกคำขอผ่อนผันเรียบร้อยแล้ว'
	} catch (err) {
		errorMessage.value = err instanceof Error ? err.message : 'บันทึกข้อมูลไม่สำเร็จ'
	} finally {
		isSubmitting.value = false
	}
}
</script>

<template>
	<div class="page">
		<header class="page-header">
			<h1>ข้อมูลนักศึกษา (ผู้ขอผ่อนผัน)</h1>
		</header>

		<p v-if="isLoading">กำลังโหลดข้อมูล...</p>
		<form v-else class="form-card" @submit.prevent="handleSubmit">
			<section>
				<h2>
					ข้อมูลนักศึกษา
					<span class="year-badge">ปีที่ผ่อนผัน {{ currentBuddhistYear }}</span>
				</h2>
				<div class="grid grid-3">
					<div class="field">
						<label for="studentCode">รหัสนักศึกษา</label>
						<input id="studentCode" v-model="studentCode" type="text" readonly />
					</div>
					<div class="field">
						<label for="studentName">ชื่อนักศึกษา</label>
						<input id="studentName" v-model="studentName" type="text" readonly />
					</div>
					<div class="field">
						<label for="personalId">เลขบัตรประชาชน</label>
						<input
							id="personalId"
							v-model="personalId"
							type="text"
							inputmode="numeric"
							placeholder="X-XXXX-XXXXX-XX-X"
							maxlength="17"
							required
						/>
						<p v-if="personalIdError" class="field-error">{{ personalIdError }}</p>
					</div>
					<div class="field">
						<label>วัน/เดือน/ปี (เกิด)</label>
						<ThaiDateInput v-model="birthDate" />
					</div>
					<div class="field">
						<label for="age">อายุ</label>
						<input id="age" :value="age ?? ''" type="text" readonly />
					</div>
					<div class="field">
						<label for="telNo">หมายเลขโทรศัพท์</label>
						<input id="telNo" v-model="telNo" type="tel" placeholder="Tel" />
					</div>
				</div>
			</section>

			<section>
				<h2>ข้อมูลการศึกษา</h2>
				<div class="grid grid-3">
					<div class="field">
						<label for="eduType">ภาค</label>
						<select id="eduType" v-model="eduType">
							<option value="">***นักศึกษาภาค***</option>
							<option v-for="opt in studentTypes" :key="opt.code" :value="opt.code">
								{{ opt.name }}
							</option>
						</select>
					</div>
					<div class="field">
						<label for="eduLevel">ระดับการศึกษา</label>
						<select id="eduLevel" v-model="eduLevel">
							<option value="">***ระดับการศึกษา***</option>
							<option v-for="opt in eduLevels" :key="opt.code" :value="opt.code">
								{{ opt.name }}
							</option>
						</select>
					</div>
					<div class="field">
						<label for="departmentCode">คณะ</label>
						<select id="departmentCode" v-model="departmentCode">
							<option value="">***คณะ***</option>
							<option v-for="opt in departments" :key="opt.code" :value="opt.code">
								{{ opt.name }}
							</option>
						</select>
					</div>
					<div class="field">
						<label for="eduProgram">โปรแกรมวิชา</label>
						<input id="eduProgram" v-model="eduProgram" type="text" />
					</div>
				</div>
			</section>

			<section>
				<h2>ภูมิลำเนาทหาร (ตาม สด.9)</h2>
				<div class="grid grid-3">
					<div class="field">
						<label for="street">ถนน</label>
						<input id="street" v-model="street" type="text" placeholder="ถนน" />
					</div>
					<div class="field">
						<label for="homeNo">บ้านเลขที่</label>
						<input id="homeNo" v-model="homeNo" type="text" placeholder="บ้านเลขที่" />
					</div>
					<div class="field">
						<label for="mooNo">หมู่ที่</label>
						<input id="mooNo" v-model="mooNo" type="text" placeholder="หมู่ที่" />
					</div>
					<div class="field">
						<label for="subDistrict">ตำบล</label>
						<input id="subDistrict" v-model="subDistrict" type="text" placeholder="ตำบล" />
					</div>
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
						<label for="postalCode">รหัสไปรษณีย์</label>
						<input id="postalCode" v-model="postalCode" type="text" placeholder="รหัสไปรษณีย์" />
					</div>
					<div class="field">
						<label for="fatherName">บิดา</label>
						<input id="fatherName" v-model="fatherName" type="text" placeholder="บิดา" />
					</div>
					<div class="field">
						<label for="fatherTel">โทรศัพท์(บิดา)</label>
						<input id="fatherTel" v-model="fatherTel" type="tel" placeholder="โทรศัพท์(บิดา)" />
					</div>
					<div class="field">
						<label for="motherName">มารดา</label>
						<input id="motherName" v-model="motherName" type="text" placeholder="มารดา" />
					</div>
					<div class="field">
						<label for="motherTel">โทรศัพท์(มารดา)</label>
						<input id="motherTel" v-model="motherTel" type="tel" placeholder="โทรศัพท์(มารดา)" />
					</div>
				</div>
			</section>

			<section class="ever-request">
				<label class="checkbox-row">
					<input v-model="everRequest" type="checkbox" />
					เคยผ่อนผันมาแล้ว:
				</label>
				<input v-model="everRequestDetail" type="text" :disabled="!everRequest" />
			</section>

			<section>
				<label for="description">รายละเอียด</label>
				<textarea id="description" v-model="description" rows="4"></textarea>
			</section>

			<p v-if="errorMessage" class="error">{{ errorMessage }}</p>
			<p v-if="successMessage" class="success">{{ successMessage }}</p>

			<div class="actions">
				<button type="submit" :disabled="isSubmitting">
					{{ isSubmitting ? 'กำลังบันทึก...' : 'บันทึก' }}
				</button>
				<button
					type="button"
					class="secondary"
					:disabled="!registrationId"
					:title="!registrationId ? 'กรุณาบันทึกข้อมูลก่อนพิมพ์เอกสาร' : ''"
					@click="handlePrint"
				>
					พิมพ์เอกสาร
				</button>
			</div>
		</form>
	</div>
</template>

<style scoped>
.page {
	max-width: 1100px;
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

.form-card {
	background: var(--bg);
	border: 1px solid var(--border);
	border-radius: 8px;
	padding: 24px;
	display: flex;
	flex-direction: column;
	gap: 24px;
}

section h2 {
	font-size: 17px;
	color: var(--accent);
	margin: 0 0 14px;
	display: flex;
	align-items: baseline;
	gap: 10px;
	flex-wrap: wrap;
}

.year-badge {
	color: #b3261e;
	font-size: 14px;
}

.grid {
	display: grid;
	gap: 16px 24px;
}

.grid-3 {
	grid-template-columns: repeat(3, 1fr);
}

@media (max-width: 720px) {
	.grid-3 {
		grid-template-columns: 1fr;
	}
}

.field {
	display: flex;
	flex-direction: column;
	gap: 4px;
	text-align: left;
}

label {
	font-size: 14px;
	color: var(--text-h);
}

input,
select,
textarea {
	font: inherit;
	padding: 8px 10px;
	border-radius: 4px;
	border: 1px solid var(--border);
	background: var(--bg);
	color: var(--text-h);
	box-sizing: border-box;
	width: 100%;
}

input:read-only {
	background: var(--code-bg);
}

input:focus-visible,
select:focus-visible,
textarea:focus-visible {
	outline: 2px solid var(--accent);
	outline-offset: 1px;
}

.ever-request {
	display: flex;
	align-items: center;
	gap: 16px;
	flex-wrap: wrap;
}

.checkbox-row {
	display: flex;
	align-items: center;
	gap: 8px;
	white-space: nowrap;
}

.ever-request input[type='text'] {
	flex: 1;
	min-width: 200px;
}

textarea {
	resize: vertical;
}

.actions {
	display: flex;
	gap: 12px;
}

button {
	font: inherit;
	font-weight: 500;
	padding: 10px 20px;
	border-radius: 4px;
	border: none;
	color: var(--accent-contrast);
	background: var(--accent);
	cursor: pointer;
}

button.secondary {
	color: var(--text-h);
	background: var(--code-bg);
	border: 1px solid var(--border);
}

button:disabled {
	opacity: 0.6;
	cursor: not-allowed;
}

.field-error {
	color: #b3261e;
	font-size: 13px;
	margin: 0;
}

.error {
	color: #b3261e;
}

.success {
	color: var(--accent);
}
</style>
