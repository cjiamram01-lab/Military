<script setup lang="ts">
defineProps<{ message: string }>()
const visible = defineModel<boolean>('visible', { default: false })

function close() {
	visible.value = false
}
</script>

<template>
	<Teleport to="body">
		<div v-if="visible" class="overlay" @click.self="close">
			<div class="dialog" role="alertdialog" aria-modal="true">
				<p class="message">{{ message }}</p>
				<button type="button" class="ok-button" @click="close">ตกลง</button>
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

.ok-button {
	font: inherit;
	font-weight: 500;
	padding: 8px 24px;
	border-radius: 4px;
	border: none;
	color: var(--accent-contrast);
	background: var(--accent);
	cursor: pointer;
}
</style>
