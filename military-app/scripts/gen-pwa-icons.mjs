import sharp from 'sharp'
import { mkdirSync } from 'node:fs'

const source = 'public/thai_military_icon.png'
const outDir = 'public/icons'
const accent = '#1d4ed8'

mkdirSync(outDir, { recursive: true })

async function main() {
	await sharp(source).resize(192, 192).png().toFile(`${outDir}/icon-192.png`)
	await sharp(source).resize(512, 512).png().toFile(`${outDir}/icon-512.png`)

	const maskableSize = 512
	const glyphSize = Math.round(maskableSize * 0.7)
	const glyph = await sharp(source).resize(glyphSize, glyphSize).png().toBuffer()

	await sharp({
		create: {
			width: maskableSize,
			height: maskableSize,
			channels: 4,
			background: accent,
		},
	})
		.composite([{ input: glyph, gravity: 'center' }])
		.png()
		.toFile(`${outDir}/icon-maskable-512.png`)

	console.log('PWA icons generated in', outDir)
}

main().catch((err) => {
	console.error(err)
	process.exit(1)
})
