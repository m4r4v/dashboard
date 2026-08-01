/**
 * Extrae colores dominantes de una imagen usando Canvas API — sin librería
 * nueva. Pensado para sugerir colores de marca a partir del logo subido en
 * Apariencia > Identidad; el usuario siempre confirma/ajusta, nunca se
 * aplican solos.
 */

const SAMPLE_SIZE = 64 // downscale para performance, no necesitamos resolución real
const QUANTIZE_STEP = 24 // agrupa tonos cercanos para contar frecuencia real

function isNearWhiteOrBlack (r: number, g: number, b: number): boolean {
  // Blanco/negro/gris real = baja saturación (canales parejos), no "un canal alto"
  // — un naranja saturado (#f97316) tiene R=249 pero NO es blanco. Bug real
  // detectado probando con un logo de prueba: el filtro viejo descartaba
  // cualquier color con un canal brillante, no solo blancos/grises reales.
  const max = Math.max(r, g, b)
  const min = Math.min(r, g, b)
  const isGrayish = max - min < 20
  return (max > 235 && isGrayish) || max < 20
}

export async function extractDominantColors (file: File, count = 3): Promise<string[]> {
  const imageUrl = URL.createObjectURL(file)
  try {
    const img = await loadImage(imageUrl)

    const canvas = document.createElement('canvas')
    canvas.width = SAMPLE_SIZE
    canvas.height = SAMPLE_SIZE
    const ctx = canvas.getContext('2d')
    if (!ctx) return []

    ctx.drawImage(img, 0, 0, SAMPLE_SIZE, SAMPLE_SIZE)
    const { data } = ctx.getImageData(0, 0, SAMPLE_SIZE, SAMPLE_SIZE)

    const buckets = new Map<string, { r: number; g: number; b: number; count: number }>()

    for (let i = 0; i < data.length; i += 4) {
      const r = data[i]
      const g = data[i + 1]
      const b = data[i + 2]
      const alpha = data[i + 3]

      if (alpha < 128) continue // transparente
      if (isNearWhiteOrBlack(r, g, b)) continue // fondo blanco/negro típico de logos

      const key = [
        Math.round(r / QUANTIZE_STEP),
        Math.round(g / QUANTIZE_STEP),
        Math.round(b / QUANTIZE_STEP),
      ].join(',')

      const bucket = buckets.get(key)
      if (bucket) {
        bucket.count += 1
      } else {
        buckets.set(key, { r, g, b, count: 1 })
      }
    }

    return [...buckets.values()]
      .sort((a, b) => b.count - a.count)
      .slice(0, count)
      .map(({ r, g, b }) => rgbToHex(r, g, b))
  } finally {
    URL.revokeObjectURL(imageUrl)
  }
}

function loadImage (src: string): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const img = new Image()
    img.crossOrigin = 'anonymous'
    img.onload = () => resolve(img)
    img.onerror = reject
    img.src = src
  })
}

function rgbToHex (r: number, g: number, b: number): string {
  return `#${[r, g, b].map(v => v.toString(16).padStart(2, '0')).join('')}`
}
