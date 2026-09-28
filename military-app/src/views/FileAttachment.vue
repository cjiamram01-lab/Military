<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useUserStore } from '../stores/user'
import { api } from '../api'
import ModalMessage from '../components/ModalMessage.vue'
import ConfirmModal from '../components/ConfirmModal.vue'
import type { Option } from '../register'
import {
	deleteAttachment,
	fetchAttachmentsByRegisterId,
	fetchDocumentTypes,
	uploadAttachment,
	type AttachmentRecord,
} from '../attachments'

const userStore = useUserStore()

const registerId = ref<number | null>(null)
const isLoading = ref(true)
const loadError = ref('')

const documentTypes = ref<Option[]>([])
const attachments = ref<AttachmentRecord[]>([])

const selectedDocType = ref('')
const selectedFile = ref<File | null>(null)
const isDragging = ref(false)
const isUploading = ref(false)
const uploadError = ref('')
const uploadSuccess = ref('')

const fileInput = ref<HTMLInputElement | null>(null)

const MAX_FILE_SIZE = 5 * 1024 * 1024
const isModalVisible = ref(false)
const modalMessage = ref('')

function showModal(message: string) {
	modalMessage.value = message
	isModalVisible.value = true
}

function applySelectedFile(file: File | null) {
	if (file && file.size > MAX_FILE_SIZE) {
		showModal('ขนาดไฟล์ต้องมีขนาดไม่เกิน 5 MB')
		if (fileInput.value) fileInput.value.value = ''
		selectedFile.value = null
		return
	}
	selectedFile.value = file
}

function docTypeName(code: string) {
	return documentTypes.value.find((opt) => opt.code === code)?.name ?? code
}

function fileLabel(url: string) {
	try {
		return decodeURIComponent(url.split('/').pop() ?? url)
	} catch {
		return url
	}
}

function fileUrl(item: AttachmentRecord) {
	return `${api.defaults.baseURL}/attachment/get_file/${item.registerId}/${item.docType}`
}

async function loadAttachments() {
	if (!registerId.value) return
	attachments.value = await fetchAttachmentsByRegisterId(registerId.value)
}

const deletingId = ref<number | null>(null)
const isConfirmVisible = ref(false)
const confirmMessage = ref('')
const pendingDeleteItem = ref<AttachmentRecord | null>(null)

function handleDelete(item: AttachmentRecord) {
	pendingDeleteItem.value = item
	confirmMessage.value = `ต้องการลบไฟล์ "${fileLabel(item.fileName)}" หรือไม่?`
	isConfirmVisible.value = true
}

async function confirmDelete() {
	const item = pendingDeleteItem.value
	if (!item) return

	deletingId.value = item.id
	try {
		await deleteAttachment(item.id)
		await loadAttachments()
	} catch (err) {
		showModal(err instanceof Error ? err.message : 'ลบไฟล์ไม่สำเร็จ')
	} finally {
		deletingId.value = null
		pendingDeleteItem.value = null
	}
}

onMounted(async () => {
	try {
		documentTypes.value = await fetchDocumentTypes()

		if (!userStore.currentUser?.registerId) {
			loadError.value = 'กรุณากรอกข้อมูลประวัตินักศึกษาก่อนแนบเอกสาร'
			return
		}

		registerId.value = userStore.currentUser.registerId
		await loadAttachments()
	} catch (err) {
		loadError.value = err instanceof Error ? err.message : 'โหลดข้อมูลไม่สำเร็จ'
	} finally {
		isLoading.value = false
	}
})

function pickFile() {
	fileInput.value?.click()
}

function onFileInputChange(event: Event) {
	const target = event.target as HTMLInputElement
	applySelectedFile(target.files?.[0] ?? null)
}

function onDrop(event: DragEvent) {
	isDragging.value = false
	const file = event.dataTransfer?.files?.[0]
	if (file) applySelectedFile(file)
}

const canUpload = computed(
	() => Boolean(selectedFile.value) && Boolean(selectedDocType.value) && Boolean(registerId.value),
)

async function handleUpload() {
	if (!canUpload.value || !selectedFile.value || !registerId.value) return

	isUploading.value = true
	uploadError.value = ''
	uploadSuccess.value = ''

	try {
		await uploadAttachment(selectedFile.value, selectedDocType.value, registerId.value)
		uploadSuccess.value = 'อัปโหลดไฟล์เรียบร้อยแล้ว'
		selectedFile.value = null
		selectedDocType.value = ''
		if (fileInput.value) fileInput.value.value = ''
		await loadAttachments()
	} catch (err) {
		uploadError.value = err instanceof Error ? err.message : 'อัปโหลดไฟล์ไม่สำเร็จ'
	} finally {
		isUploading.value = false
	}
}
</script>

<template>
	<div class="page">
		<header class="page-header">
			<h1>เอกสาร/หลักฐาน</h1>
		</header>

		<p v-if="isLoading">กำลังโหลดข้อมูล...</p>
		<p v-else-if="loadError" class="error">{{ loadError }}</p>

		<template v-else>
			<section class="card">
				<h2>เอกสารที่แนบแล้ว</h2>
				<table v-if="attachments.length" class="attachment-table">
					<thead>
						<tr>
							<th>ประเภทเอกสาร</th>
							<th>ไฟล์</th>
							<th></th>
						</tr>
					</thead>
					<tbody>
						<tr v-for="item in attachments" :key="item.id">
							<td>{{ docTypeName(item.docType) }}</td>
							<td>{{ fileLabel(item.fileName) }}</td>
							<td>
								<a
									:href="fileUrl(item)"
									target="_blank"
									rel="noopener"
									class="view-icon"
									title="ดูไฟล์"
									aria-label="ดูไฟล์"
								>
									<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
										<path
											d="M1.5 12S5 5 12 5s10.5 7 10.5 7-3.5 7-10.5 7S1.5 12 1.5 12Z"
											stroke-linecap="round"
											stroke-linejoin="round"
										/>
										<circle cx="12" cy="12" r="3" />
									</svg>
								</a>
								<button
									type="button"
									class="delete-icon"
									title="ลบไฟล์"
									aria-label="ลบไฟล์"
									:disabled="deletingId === item.id"
									@click="handleDelete(item)"
								>
									<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
										<path
											d="M4 7h16M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2m-8 0 1 13a2 2 0 0 0 2 2h4a2 2 0 0 0 2-2l1-13"
											stroke-linecap="round"
											stroke-linejoin="round"
										/>
									</svg>
								</button>
							</td>
						</tr>
					</tbody>
				</table>
				<p v-else class="empty">ยังไม่มีเอกสารที่แนบ</p>
			</section>

			<section class="card">
				<h2>อัปโหลดเอกสาร</h2>

				<div class="field">
					<label for="docType">ประเภทเอกสาร</label>
					<select id="docType" v-model="selectedDocType">
						<option value="">***เลือกประเภทเอกสาร***</option>
						<option v-for="opt in documentTypes" :key="opt.code" :value="opt.code">
							{{ opt.name }}
						</option>
					</select>
				</div>

				<div
					class="dropzone"
					:class="{ dragging: isDragging }"
					@click="pickFile"
					@dragover.prevent="isDragging = true"
					@dragleave.prevent="isDragging = false"
					@drop.prevent="onDrop"
				>
					<input
						ref="fileInput"
						type="file"
						class="hidden-input"
						@change="onFileInputChange"
					/>
					<p v-if="selectedFile">{{ selectedFile.name }}</p>
					<p v-else>ลากไฟล์มาวาง หรือคลิกเพื่อเลือกไฟล์</p>
				</div>

				<p v-if="uploadError" class="error">{{ uploadError }}</p>
				<p v-if="uploadSuccess" class="success">{{ uploadSuccess }}</p>

				<button type="button" :disabled="!canUpload || isUploading" @click="handleUpload">
					{{ isUploading ? 'กำลังอัปโหลด...' : 'อัปโหลด' }}
				</button>
			</section>
		</template>

		<ModalMessage v-model:visible="isModalVisible" :message="modalMessage" />
		<ConfirmModal
			v-model:visible="isConfirmVisible"
			:message="confirmMessage"
			confirm-text="ลบ"
			@confirm="confirmDelete"
		/>
	</div>
</template>

<style scoped>
.page {
	max-width: 900px;
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

.card h2 {
	font-size: 17px;
	color: var(--accent);
	margin: 0 0 16px;
}

.attachment-table {
	width: 100%;
	border-collapse: collapse;
}

.attachment-table th,
.attachment-table td {
	text-align: left;
	padding: 8px 10px;
	border-bottom: 1px solid var(--border);
	font-size: 14px;
}

.attachment-table a {
	color: var(--accent);
}

.view-icon {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	width: 28px;
	height: 28px;
	border-radius: 4px;
	color: var(--accent);
}

.view-icon:hover {
	background: var(--accent-bg);
}

.view-icon svg {
	width: 18px;
	height: 18px;
}

.delete-icon {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	width: 28px;
	height: 28px;
	padding: 0;
	border-radius: 4px;
	border: none;
	background: none;
	color: #b3261e;
	font-weight: normal;
	cursor: pointer;
	margin-left: 4px;
}

.delete-icon:hover {
	background: rgba(179, 38, 30, 0.1);
}

.delete-icon:disabled {
	opacity: 0.5;
	cursor: not-allowed;
}

.delete-icon svg {
	width: 18px;
	height: 18px;
}

.empty {
	color: var(--text);
	font-size: 14px;
}

.field {
	display: flex;
	flex-direction: column;
	gap: 4px;
	margin-bottom: 16px;
}

label {
	font-size: 14px;
	color: var(--text-h);
}

select {
	font: inherit;
	padding: 8px 10px;
	border-radius: 4px;
	border: 1px solid var(--border);
	background: var(--bg);
	color: var(--text-h);
	box-sizing: border-box;
}

.dropzone {
	border: 2px dashed var(--border);
	border-radius: 6px;
	padding: 32px;
	text-align: center;
	cursor: pointer;
	color: var(--text);
	margin-bottom: 16px;
}

.dropzone.dragging {
	border-color: var(--accent);
	background: var(--accent-bg);
	color: var(--text-h);
}

.hidden-input {
	display: none;
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

button:disabled {
	opacity: 0.6;
	cursor: not-allowed;
}

.error {
	color: #b3261e;
}

.success {
	color: var(--accent);
}
</style>
