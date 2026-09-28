<script setup lang="ts">
import { computed } from 'vue'
import { THAI_MONTHS } from '../thaiDate'

const modelValue = defineModel<string>({ default: '' })

const days = Array.from({ length: 31 }, (_, i) => i + 1)
const months = THAI_MONTHS.map((name, i) => ({ value: i + 1, name }))

const currentBuddhistYear = new Date().getFullYear() + 543
const years = Array.from({ length: 100 }, (_, i) => currentBuddhistYear - i)

const parsed = computed(() => {
	if (!modelValue.value) return { day: null, month: null, buddhistYear: null }
	const [y, m, d] = modelValue.value.split('-').map(Number)
	if (!y || !m || !d) return { day: null, month: null, buddhistYear: null }
	return { day: d, month: m, buddhistYear: y + 543 }
})

const day = computed({
	get: () => parsed.value.day,
	set: (value) => updatePart('day', value),
})
const month = computed({
	get: () => parsed.value.month,
	set: (value) => updatePart('month', value),
})
const buddhistYear = computed({
	get: () => parsed.value.buddhistYear,
	set: (value) => updatePart('buddhistYear', value),
})

function updatePart(part: 'day' | 'month' | 'buddhistYear', value: number | null) {
	const next = { ...parsed.value, [part]: value }
	if (!next.day || !next.month || !next.buddhistYear) {
		modelValue.value = ''
		return
	}
	const gregorianYear = next.buddhistYear - 543
	const iso = `${String(gregorianYear).padStart(4, '0')}-${String(next.month).padStart(2, '0')}-${String(next.day).padStart(2, '0')}`
	modelValue.value = iso
}
</script>

<template>
	<div class="thai-date-input">
		<select v-model="day" aria-label="วัน">
			<option :value="null">วัน</option>
			<option v-for="d in days" :key="d" :value="d">{{ d }}</option>
		</select>
		<select v-model="month" aria-label="เดือน">
			<option :value="null">เดือน</option>
			<option v-for="m in months" :key="m.value" :value="m.value">{{ m.name }}</option>
		</select>
		<select v-model="buddhistYear" aria-label="ปี พ.ศ.">
			<option :value="null">ปี (พ.ศ.)</option>
			<option v-for="y in years" :key="y" :value="y">{{ y }}</option>
		</select>
	</div>
</template>

<style scoped>
.thai-date-input {
	display: grid;
	grid-template-columns: 0.8fr 1.4fr 1.2fr;
	gap: 6px;
}

select {
	font: inherit;
	padding: 8px 10px;
	border-radius: 4px;
	border: 1px solid var(--border);
	background: var(--bg);
	color: var(--text-h);
	box-sizing: border-box;
	width: 100%;
}

select:focus-visible {
	outline: 2px solid var(--accent);
	outline-offset: 1px;
}
</style>
