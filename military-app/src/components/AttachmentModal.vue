<script setup lang="ts">
import { ref, watch } from 'vue'
import type { DistrictAttachment } from '../register'

defineProps<{ title?: string; attachments: DistrictAttachment[] }>()
const visible = defineModel<boolean>('visible', { default: false })

// The document currently shown in the inline viewer (null = show the list).
const selected = ref<DistrictAttachment | null>(null)

watch(visible, (isVisible) => {
	if (!isVisible) selected.value = null
})

function close() {
	visible.value = false
}

// document_type can carry stray <br> markup from the source data; show it as plain text.
function typeLabel(value: string) {
	return (value ?? '').replace(/<br\s*\/?>/gi, ' ').trim()
}

function isSafeUrl(url: string) {
	return /^https?:\/\//i.test(url)
}
</script>

<template>
	<Teleport to="body">
		<div v-if="visible" class="overlay" @click.self="close">
			<div
				class="dialog"
				:class="{ wide: selected }"
				role="dialog"
				aria-modal="true"
				aria-labelledby="attachment-title"
			>
				<h2 id="attachment-title" class="title">
					{{ selected ? typeLabel(selected.document_type) : title || 'เอกสาร/หลักฐาน' }}
				</h2>

				<template v-if="selected">
					<iframe :src="selected.file_name" class="viewer" :title="typeLabel(selected.document_type)" />
					<div class="actions">
						<button type="button" class="secondary" @click="selected = null">กลับ</button>
						<a :href="selected.file_name" target="_blank" rel="noopener noreferrer" class="open-link">
							เปิดในแท็บใหม่
						</a>
						<button type="button" @click="close">ปิด</button>
					</div>
				</template>

				<template v-else>
					<p v-if="!attachments.length" class="empty">ไม่มีเอกสารแนบ</p>
					<ol v-else class="list">
						<li v-for="(file, index) in attachments" :key="`${file.file_name}-${index}`">
							<a
								v-if="isSafeUrl(file.file_name)"
								:href="file.file_name"
								target="_blank"
								rel="noopener noreferrer"
								@click.prevent="selected = file"
							>
								{{ typeLabel(file.document_type) }}
							</a>
							<span v-else>{{ typeLabel(file.document_type) }}</span>
						</li>
					</ol>

					<div class="actions">
						<button type="button" @click="close">ปิด</button>
					</div>
				</template>
			</div>
		</div>
	</Teleport>
</template>

<style scoped>
.overlay {
	position: fixed;
	inset: 0;
	background: rgba(0, 0, 0, 0.5);
	display: flex;
	align-items: center;
	justify-content: center;
	padding: 16px;
	box-sizing: border-box;
	z-index: 100;
}

.dialog {
	background: var(--bg);
	border: 1px solid var(--border);
	border-top: 4px solid var(--accent);
	border-radius: 8px;
	box-shadow: var(--shadow);
	padding: 24px;
	max-width: 520px;
	width: 100%;
	max-height: 90vh;
	overflow-y: auto;
	box-sizing: border-box;
}

.dialog.wide {
	max-width: 960px;
}

.title {
	font-size: 17px;
	margin: 0 0 16px;
	color: var(--text-h);
}

.list {
	margin: 0 0 20px;
	padding-left: 22px;
	display: flex;
	flex-direction: column;
	gap: 10px;
	font-size: 14px;
	color: var(--text-h);
}

.list a {
	color: var(--accent);
}

.empty {
	margin: 0 0 20px;
	color: var(--text);
}

.viewer {
	display: block;
	width: 100%;
	height: 70vh;
	border: 1px solid var(--border);
	border-radius: 4px;
	background: #fff;
	margin-bottom: 16px;
}

.actions {
	display: flex;
	align-items: center;
	justify-content: flex-end;
	gap: 12px;
}

.actions button {
	font: inherit;
	font-weight: 500;
	padding: 8px 24px;
	border-radius: 4px;
	border: none;
	color: var(--accent-contrast);
	background: var(--accent);
	cursor: pointer;
}

.actions button.secondary {
	color: var(--text-h);
	background: var(--code-bg);
	border: 1px solid var(--border);
}

.open-link {
	margin-right: auto;
	font-size: 14px;
	color: var(--accent);
}
</style>
