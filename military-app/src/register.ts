import axios from 'axios'
import { api } from './api'

export interface Option {
	code: string
	name: string
}

export interface RegistrationRecord {
	id: number
	studentCode: string
	studentName: string
	personalId: string
	birthYear: number | string
	age: number
	street?: string
	homeNo?: string
	mooNo?: string
	subDistrict?: string
	district?: string
	province?: string
	postalCode?: string
	fatherName?: string
	motherName?: string
	description?: string
	fatherTel?: string
	motherTel?: string
	birthDate: string
	departmentCode?: string
	telNo?: string
	eduLevel?: string
	eduProgram?: string
	registYear?: string
	eduType?: string
	everRequest?: number | boolean
	everSchool?: number | boolean | string
	isAprove?: number | boolean
}

export interface RegistrationPayload {
	id: number
	studentCode: string
	studentName: string
	personalId: string
	birthYear: number
	age: number
	street?: string
	homeNo?: string
	mooNo?: string
	subDistrict?: string
	district?: string
	province?: string
	postalCode?: string
	fatherName?: string
	motherName?: string
	description?: string
	fatherTel?: string
	motherTel?: string
	birthDate: string
	departmentCode?: string
	telNo?: string
	eduLevel?: string
	eduProgram?: string
	registYear?: string
	eduType?: string
	everRequest?: boolean
	everSchool?: boolean
	isAprove?: boolean
}

async function fetchOptions(path: string): Promise<Option[]> {
	const response = await api.get(path)
	console.log(path, response.data)
	return response.data?.data ?? []
}

export const fetchProvinces = () => fetchOptions('/register/get_province')
export const fetchDepartments = () => fetchOptions('/register/get_department')
export const fetchEduLevels = () => fetchOptions('/register/get_edulevel')
export const fetchStudentTypes = () => fetchOptions('/register/get_studenttype')
export const fetchDistricts = (provinceCode: string) =>
	fetchOptions(`/register/get_district/${provinceCode}`)

export async function submitRegistration(payload: RegistrationPayload) {
	const response = await api.post('/register/add', payload)
	console.log('/register/add', response.data)
	if (response.data?.status !== 'success') {
		throw new Error(response.data?.message || 'บันทึกข้อมูลไม่สำเร็จ')
	}
	return response.data.data
}

export async function updateRegistration(id: number, payload: RegistrationPayload) {
	console.log(JSON.stringify(payload));
	const response = await api.put(`/register/update/${id}`, payload)
	console.log(`/register/update/${id}`, response.data)
	if (response.data?.status !== 'success') {
		throw new Error(response.data?.message || 'บันทึกข้อมูลไม่สำเร็จ')
	}
	return response.data.data
}

export async function fetchStudentByCode(
	studentCode: string,
): Promise<RegistrationRecord | null> {
	try {
		const response = await api.get(
			`/register/get_data_by_student_code/${encodeURIComponent(studentCode)}`,
		)
		console.log('/register/get_data_by_student_code', response.data)
		return response.data?.status === 'success' ? response.data.data : null
	} catch (err) {
		if (axios.isAxiosError(err) && err.response?.status === 404) {
			return null
		}
		throw err
	}
}

export async function fetchRegisterId(studentCode: string): Promise<number | null> {
	try {
		const response = await api.get(
			`/register/get_ref_id_by_student_code/${encodeURIComponent(studentCode)}`,
		)
		console.log('/register/get_ref_id_by_student_code', response.data)
		return response.data?.status === 'success' ? response.data.data : null
	} catch (err) {
		if (axios.isAxiosError(err) && err.response?.status === 404) {
			return null
		}
		throw err
	}
}

export interface ReportRecord {
	id: number
	studentCode: string
	studentName: string
	personalId: string
	birthDate: string
	age: number
	street?: string
	homeNo?: string
	mooNo?: string
	subDistrict?: string
	district?: string
	province?: string
	postalCode?: string
	fatherName?: string
	motherName?: string
	fatherTel?: string
	motherTel?: string
	eduLevel?: string
	eduProgram?: string
	registYear?: string
	eduType?: string
	departmentCode?: string
	everRequest?: number | boolean
	everSchool?: number | boolean | string
	telNo?: string
}

export async function fetchRegisterById(id: number): Promise<ReportRecord | null> {
	try {
		const response = await api.get(`/register/get_register_by_id/${id}`)
		console.log(`/register/get_register_by_id/${id}`, response.data)
		return response.data?.status === 'success' ? response.data.data : null
	} catch (err) {
		if (axios.isAxiosError(err) && err.response?.status === 404) {
			return null
		}
		throw err
	}
}

export interface DistrictAttachment {
	file_name: string
	document_type: string
}

export interface DistrictStudentRow {
	registerId: number
	attachments: DistrictAttachment[]
	studentCode: string
	personalId: string
	studentName: string
	birthYear: string
	street?: string
	homeNo?: string
	mooNo?: string
	subDistrict?: string
	postalCode?: string
	fatherName?: string
	motherName?: string
	districtName?: string
	districtCode?: string
	provinceName?: string
	provinceCode?: string
}

export async function fetchStudentsByDistrict(
	provinceCode: string,
	districtCode: string,
	birthYear: string,
): Promise<DistrictStudentRow[]> {
	// An empty district means "all districts": the API route without a district segment.
	const path = districtCode
		? `${provinceCode}/${districtCode}/${birthYear}`
		: `${provinceCode}/${birthYear}`
	const response = await api.get(`/register/get_student_by_district/${path}`)
	return response.data?.status === 'success' ? response.data.data : []
}

export interface MigrateHistoryItem {
	studentCode: string
	activeYear: number
	action: 'create' | 'update'
	result: {
		Flag: boolean
		Id?: number
		err?: string
	}
}

export interface MigrateResult {
	history: MigrateHistoryItem[]
	message: boolean
}

export async function migrateStudentSoldierFromNrru(
	orgYear: number,
	activeYear: number,
): Promise<MigrateResult> {
	const response = await api.get(
		`/register/migrate_student_soldier_from_nrru/${orgYear}/${activeYear}`,
		{ timeout: 5 * 60 * 1000 },
	)
	if (response.data?.status !== 'success') {
		throw new Error(response.data?.message || 'ย้ายข้อมูลไม่สำเร็จ')
	}
	return response.data.data as MigrateResult
}
