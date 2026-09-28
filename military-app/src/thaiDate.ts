export const THAI_MONTHS = [
	'มกราคม',
	'กุมภาพันธ์',
	'มีนาคม',
	'เมษายน',
	'พฤษภาคม',
	'มิถุนายน',
	'กรกฎาคม',
	'สิงหาคม',
	'กันยายน',
	'ตุลาคม',
	'พฤศจิกายน',
	'ธันวาคม',
]

export function formatThaiFullDate(isoDate: string): string {
	const date = new Date(isoDate)
	if (Number.isNaN(date.getTime())) return ''

	const day = String(date.getDate()).padStart(2, '0')
	const month = THAI_MONTHS[date.getMonth()]
	const buddhistYear = date.getFullYear() + 543

	return `${day}-${month}-${buddhistYear}`
}
