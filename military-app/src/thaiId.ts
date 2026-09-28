export function formatThaiPersonalId(digits: string): string {
	const groups = [
		digits.slice(0, 1),
		digits.slice(1, 5),
		digits.slice(5, 10),
		digits.slice(10, 12),
		digits.slice(12, 13),
	].filter((group) => group.length > 0)

	return groups.join('-')
}

export function isValidThaiPersonalId(digits: string): boolean {
	if (!/^\d{13}$/.test(digits)) return false

	let sum = 0
	for (let i = 0; i < 12; i++) {
		sum += Number(digits[i]) * (13 - i)
	}

	const checkDigit = (11 - (sum % 11)) % 10
	return checkDigit === Number(digits[12])
}
