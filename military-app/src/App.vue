<script setup lang="ts">
import ThemeToggle from './components/ThemeToggle.vue'
</script>

<template>
	<RouterView />
	<ThemeToggle class="global-theme-toggle" />
</template>

<style scoped>
.global-theme-toggle {
	position: fixed;
	right: 16px;
	bottom: 16px;
	z-index: 40;
}
</style>
