// Public-folder assets need the configured base path (e.g. "/military/")
// prefixed at runtime, since Vite only rewrites root-absolute src/href
// attributes automatically inside index.html, not inside component templates.
export function publicAsset(path: string): string {
	return `${import.meta.env.BASE_URL}${path}`
}
