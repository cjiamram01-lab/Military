import { defineStore } from 'pinia'
import { login as loginRequest, type LoggedInUser } from '../auth'
import { fetchRegisterId } from '../register'

const STORAGE_KEY = 'military-app.currentUser'

// sessionStorage is copied into any tab opened via window.open()/target="_blank"
// from the same origin (e.g. the print report), so this keeps that tab logged in
// even though Pinia's own state is in-memory only and starts fresh there.
function loadStoredUser(): LoggedInUser | null {
	try {
		const raw = sessionStorage.getItem(STORAGE_KEY)
		return raw ? (JSON.parse(raw) as LoggedInUser) : null
	} catch {
		return null
	}
}

export const useUserStore = defineStore('user', {
	state: () => ({
		currentUser: loadStoredUser(),
	}),
	actions: {
		async login(username: string, password: string) {
			const user = await loginRequest(username, password)

			let registerId: number | undefined
			try {
				registerId = (await fetchRegisterId(user.username ?? username)) ?? undefined
			} catch {
				registerId = undefined
			}

			this.currentUser = { ...user, registerId }
			try {
				sessionStorage.setItem(STORAGE_KEY, JSON.stringify(this.currentUser))
			} catch {
				// storage unavailable (e.g. private browsing) - session just won't survive a new tab
			}

			return this.currentUser
		},
		logout() {
			this.currentUser = null
			try {
				sessionStorage.removeItem(STORAGE_KEY)
			} catch {
				// ignore
			}
		},
	},
})
