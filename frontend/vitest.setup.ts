import '@testing-library/jest-dom'

// JSDOM clipboard polyfill for tests that use navigator.clipboard
Object.assign(navigator, {
  clipboard: {
    writeText: async () => Promise.resolve(),
  },
})

// Canvas 2D context polyfill for JSDOM
// Prevent errors from components that use HTMLCanvasElement.getContext
if (typeof HTMLCanvasElement !== 'undefined') {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  (HTMLCanvasElement.prototype as any).getContext = function (type: string) {
    if (type !== '2d') return null
    // Minimal mock of CanvasRenderingContext2D used by our Vortex component
    return {
      // State
      fillStyle: '',
      strokeStyle: '',
      globalAlpha: 1,
      globalCompositeOperation: 'source-over',
      lineCap: 'butt',
      lineWidth: 1,
      // Methods (no-op)
      clearRect: () => {},
      fillRect: () => {},
      save: () => {},
      restore: () => {},
      beginPath: () => {},
      moveTo: () => {},
      lineTo: () => {},
      stroke: () => {},
      closePath: () => {},
      drawImage: () => {},
    } as unknown as CanvasRenderingContext2D
  }
}

// requestAnimationFrame polyfill for Node/JSDOM environment
if (typeof window !== 'undefined' && typeof window.requestAnimationFrame === 'undefined') {
  window.requestAnimationFrame = (cb: FrameRequestCallback) => setTimeout(() => cb(Date.now()), 16) as unknown as number
}
