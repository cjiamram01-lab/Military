import { api } from './api'
import type { Option } from './register'

export interface AttachmentRecord {
	id: number
	fileName: string
	docType: string
	registerId: number
}

export const fetchDocumentTypes = async (): Promise<Option[]> => {
	const response = await api.get('/attachment/get_document_types')
	return response.data?.data ?? []
}

export const fetchAttachmentsByRegisterId = async (
	registerId: number,
): Promise<AttachmentRecord[]> => {
	const response = await api.get(`/attachment/get_attachments_by_register_id/${registerId}`)
	return response.data?.data ?? []
}

export async function uploadAttachment(file: File, docType: string, registerId: number) {
	const form = new FormData()
	form.append('file', file)
	form.append('doc_type', docType)
	form.append('register_id', String(registerId))

	const response = await api.post('/attachment/upload', form)
	if (response.data?.status !== 'success') {
		throw new Error(response.data?.message || 'อัปโหลดไฟล์ไม่สำเร็จ')
	}
	return response.data
}

export async function deleteAttachment(id: number) {
	const response = await api.delete(`/attachment/delete_by_id/${id}`)
	if (response.data?.status !== 'success') {
		throw new Error(response.data?.message || 'ลบไฟล์ไม่สำเร็จ')
	}
	return response.data
}
