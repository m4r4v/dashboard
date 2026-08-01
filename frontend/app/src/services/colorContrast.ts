/**
 * Utilidades de contraste (WCAG) para que un color de marca elegido
 * libremente por el usuario nunca produzca texto ilegible — ni sobre un
 * relleno sólido de ese color (botones) ni cuando el color se usa como
 * texto sobre una superficie neutra (títulos).
 */

function hexToRgb (hex: string): [number, number, number] {
  const clean = hex.replace('#', '')
  return [
    parseInt(clean.slice(0, 2), 16),
    parseInt(clean.slice(2, 4), 16),
    parseInt(clean.slice(4, 6), 16),
  ]
}

function rgbToHex (r: number, g: number, b: number): string {
  return `#${[r, g, b].map(v => Math.round(Math.min(255, Math.max(0, v))).toString(16).padStart(2, '0')).join('')}`
}

function relativeLuminance (r: number, g: number, b: number): number {
  const [rs, gs, bs] = [r, g, b].map(v => {
    const c = v / 255
    return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4
  })
  return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs
}

function contrastRatio (hexA: string, hexB: string): number {
  const lumA = relativeLuminance(...hexToRgb(hexA))
  const lumB = relativeLuminance(...hexToRgb(hexB))
  const [lighter, darker] = lumA > lumB ? [lumA, lumB] : [lumB, lumA]
  return (lighter + 0.05) / (darker + 0.05)
}

/** Para texto sobre un relleno sólido del color (botones): blanco o negro, el que dé más contraste. */
export function getContrastingColor (bgHex: string): string {
  const white = '#ffffff'
  const black = '#000000'
  return contrastRatio(bgHex, white) >= contrastRatio(bgHex, black) ? white : black
}

function rgbToHsl (r: number, g: number, b: number): [number, number, number] {
  r /= 255; g /= 255; b /= 255
  const max = Math.max(r, g, b)
  const min = Math.min(r, g, b)
  let h = 0
  const l = (max + min) / 2
  const d = max - min
  const s = d === 0 ? 0 : d / (1 - Math.abs(2 * l - 1))
  if (d !== 0) {
    switch (max) {
      case r: h = ((g - b) / d) % 6; break
      case g: h = (b - r) / d + 2; break
      default: h = (r - g) / d + 4
    }
    h *= 60
    if (h < 0) h += 360
  }
  return [h, s, l]
}

function hslToRgb (h: number, s: number, l: number): [number, number, number] {
  const c = (1 - Math.abs(2 * l - 1)) * s
  const x = c * (1 - Math.abs((h / 60) % 2 - 1))
  const m = l - c / 2
  let [r, g, b] = [0, 0, 0]
  if (h < 60) [r, g, b] = [c, x, 0]
  else if (h < 120) [r, g, b] = [x, c, 0]
  else if (h < 180) [r, g, b] = [0, c, x]
  else if (h < 240) [r, g, b] = [0, x, c]
  else if (h < 300) [r, g, b] = [x, 0, c]
  else [r, g, b] = [c, 0, x]
  return [(r + m) * 255, (g + m) * 255, (b + m) * 255]
}

/**
 * Si `hex` usado como texto sobre `bgHex` no llega al contraste mínimo
 * (WCAG AA = 4.5:1), oscurece o aclara `hex` (en HSL, mismo tono) hasta
 * que lo alcance. Nunca cambia el matiz elegido por el usuario, solo su
 * luminosidad — para que siga siendo "su color", pero legible.
 */
export function ensureReadableAsText (hex: string, bgHex: string, minRatio = 4.5): string {
  if (contrastRatio(hex, bgHex) >= minRatio) return hex

  const [h, s, l] = rgbToHsl(...hexToRgb(hex))
  const bgLuminance = relativeLuminance(...hexToRgb(bgHex))
  const shouldDarken = bgLuminance > 0.5 // fondo claro -> el texto necesita oscurecerse, no aclararse

  let lightness = l
  for (let i = 0; i < 20; i++) {
    lightness = shouldDarken ? Math.max(0, lightness - 0.05) : Math.min(1, lightness + 0.05)
    const candidate = rgbToHex(...hslToRgb(h, s, lightness))
    if (contrastRatio(candidate, bgHex) >= minRatio) return candidate
    if (lightness <= 0 || lightness >= 1) break
  }

  return shouldDarken ? '#000000' : '#ffffff'
}
