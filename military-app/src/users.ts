import { api } from './api'

export interface UserRecord {
	id: number
	username: string
	fullname: string
	picture?: string
	description?: string
	position: string
}

export async function queryUsers(keyword: string): Promise<UserRecord[]> {
	const response = await api.get('/user/query_user', { params: { keyword } })
	return response.data?.status === 'success' ? response.data.data : []
}

export async function setUserPosition(userId: number, position: string) {
	const response = await api.put('/user/set_user_position', null, {
		params: { user_id: userId, position },
	})
	if (response.data?.status !== 'success') {
		throw new Error(response.data?.message || 'อัปเดตตำแหน่งไม่สำเร็จ')
	}
	return response.data.data
}
