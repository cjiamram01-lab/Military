import { computed, ref, watchEffect } from 'vue'

type Theme = 'light' | 'dark'

const STORAGE_KEY = 'military-app.theme'

function getStoredTheme(): Theme | null {
	try {
		const stored = localStorage.getItem(STORAGE_KEY)
		return stored === 'light' || stored === 'dark' ? stored : null
	} catch {
		return null
	}
}

const darkMediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
const systemPrefersDark = ref(darkMediaQuery.matches)
darkMediaQuery.addEventListener('change', (event) => {
	systemPrefersDark.value = event.matches
})

// null means "follow the system setting"; becomes explicit once the user toggles
export const theme = ref<Theme | null>(getStoredTheme())

export const isDarkTheme = computed(() =>
	theme.value ? theme.value === 'dark' : systemPrefersDark.value,
)

export function toggleTheme() {
	theme.value = isDarkTheme.value ? 'light' : 'dark'
}

watchEffect(() => {
	if (theme.value) {
		document.documentElement.setAttribute('data-theme', theme.value)
		try {
			localStorage.setItem(STORAGE_KEY, theme.value)
		} catch {
			// ignore
		}
	} else {
		document.documentElement.removeAttribute('data-theme')
	}
})
