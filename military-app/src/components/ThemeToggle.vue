<script setup lang="ts">
import { isDarkTheme, toggleTheme } from '../theme'
</script>

<template>
	<button
		type="button"
		class="theme-toggle"
		:aria-label="isDarkTheme ? 'สลับเป็นโหมดสว่าง' : 'สลับเป็นโหมดมืด'"
		@click="toggleTheme"
	>
		<svg v-if="isDarkTheme" viewBox="0 0 24 24" fill="currentColor">
			<path
				d="M12 4.5a1 1 0 0 1 1-1V2a1 1 0 1 1-2 0v1.5a1 1 0 0 1 1 1Zm0 15a1 1 0 0 1 1 1V22a1 1 0 1 1-2 0v-1.5a1 1 0 0 1 1-1ZM4.5 12a1 1 0 0 1-1 1H2a1 1 0 1 1 0-2h1.5a1 1 0 0 1 1 1Zm15 0a1 1 0 0 1 1-1H22a1 1 0 1 1 0 2h-1.5a1 1 0 0 1-1-1ZM6.34 6.34a1 1 0 0 1-1.41 0L3.87 5.28a1 1 0 0 1 1.41-1.41l1.06 1.05a1 1 0 0 1 0 1.42Zm12.73 12.73a1 1 0 0 1-1.41 0l-1.06-1.06a1 1 0 0 1 1.41-1.41l1.06 1.06a1 1 0 0 1 0 1.41ZM6.34 17.66a1 1 0 0 1 0 1.41l-1.06 1.06a1 1 0 1 1-1.41-1.41l1.06-1.06a1 1 0 0 1 1.41 0Zm12.73-12.73a1 1 0 0 1 0 1.41l-1.06 1.06a1 1 0 1 1-1.41-1.41l1.06-1.06a1 1 0 0 1 1.41 0ZM12 7a5 5 0 1 1 0 10 5 5 0 0 1 0-10Z"
			/>
		</svg>
		<svg v-else viewBox="0 0 24 24" fill="currentColor">
			<path
				d="M20.7 14.9a8.5 8.5 0 0 1-10.6-10.6 1 1 0 0 0-1.3-1.2A10.5 10.5 0 1 0 21.9 16.2a1 1 0 0 0-1.2-1.3Z"
			/>
		</svg>
	</button>
</template>

<style scoped>
.theme-toggle {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	width: 34px;
	height: 34px;
	border-radius: 50%;
	border: 1px solid var(--border);
	background: var(--bg);
	color: var(--text-h);
	cursor: pointer;
}

.theme-toggle:hover {
	border-color: var(--accent-border);
	color: var(--accent);
}

.theme-toggle svg {
	width: 18px;
	height: 18px;
}

@media print {
	.theme-toggle {
		display: none;
	}
}
</style>
