export interface AppConfig {
	apiBaseUrl: string
}

let cachedConfig: AppConfig | null = null

export async function loadConfig(): Promise<AppConfig> {
	if (cachedConfig) return cachedConfig

	const response = await fetch(`${import.meta.env.BASE_URL}config.json`)
	if (!response.ok) {
		throw new Error(`Failed to load config.json: ${response.status}`)
	}

	cachedConfig = (await response.json()) as AppConfig
	return cachedConfig
}
