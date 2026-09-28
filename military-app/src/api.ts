import axios from 'axios'
import { loadConfig } from './config'

export const api = axios.create()

let configured: Promise<void> | null = null

export function ensureApiConfigured(): Promise<void> {
	if (!configured) {
		configured = loadConfig().then((config) => {
			api.defaults.baseURL = config.apiBaseUrl
		})
	}
	return configured
}
