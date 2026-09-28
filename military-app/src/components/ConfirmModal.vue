<script setup lang="ts">
withDefaults(
	defineProps<{
		message: string
		confirmText?: string
		cancelText?: string
	}>(),
	{
		confirmText: 'ยืนยัน',
		cancelText: 'ยกเลิก',
	},
)

const visible = defineModel<boolean>('visible', { default: false })

const emit = defineEmits<{ confirm: [] }>()

function cancel() {
	visible.value = false
}

function confirm() {
	visible.value = false
	emit('confirm')
}
</script>

<template>
	<Teleport to="body">
		<div v-if="visible" class="overlay" @click.self="cancel">
			<div class="dialog" role="alertdialog" aria-modal="true">
				<p class="message">{{ message }}</p>
				<div class="actions">
					<button type="button" class="cancel-button" @click="cancel">{{ cancelText }}</button>
					<button type="button" class="confirm-button" @click="confirm">{{ confirmText }}</button>
				</div>
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
	max-width: 320px;
	width: 100%;
	text-align: center;
	box-sizing: border-box;
}

.message {
	color: var(--text-h);
	margin: 0 0 20px;
}

.actions {
	display: flex;
	justify-content: center;
	gap: 12px;
}

.cancel-button,
.confirm-button {
	font: inherit;
	font-weight: 500;
	padding: 8px 24px;
	border-radius: 4px;
	border: none;
	cursor: pointer;
}

.cancel-button {
	color: var(--text-h);
	background: var(--code-bg);
	border: 1px solid var(--border);
}

.cancel-button:hover {
	border-color: var(--accent-border);
}

.confirm-button {
	color: var(--accent-contrast);
	background: #b3261e;
}
</style>
