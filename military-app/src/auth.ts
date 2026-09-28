import { api } from './api'

export interface LoggedInUser {
	id?: number
	username?: string
	fullname?: string
	picture?: string
	description?: string
	registerId?: number
	position?:string
	role?: string
	[key: string]: unknown
}

export function isAdmin(user: LoggedInUser | null | undefined): boolean {
	return user?.role?.toLowerCase() === 'admin'
}

export function homeRouteName(user: LoggedInUser | null | undefined): string {
	return isAdmin(user) ? 'reportStudentByDistrict' : 'studentRegistration'
}

export async function login(username: string, password: string): Promise<LoggedInUser> {
	const response = await api.post(
		'/user/login',
		null,
		{ params: { user_name: username, password } },
	)

	const body = response.data
	const raw = body?.data
	// login_system returns a plain object when it falls back to login_mis,
	// but an array of rows when it matches a user directly in t_user.
	const data = Array.isArray(raw) ? raw[0] : raw

	if (body?.status !== 'success' || !data || data.status === 'error') {
		throw new Error(data?.message || 'ชื่อผู้ใช้งานหรือรหัสผ่านไม่ถูกต้อง')
	}

	return data as LoggedInUser
}
