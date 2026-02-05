import { Vortex } from "@/components/ui/vortex"

export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="relative min-h-screen text-slate-50">
      {/* Vortex background */}
      <div 
        style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          width: '100vw',
          height: '100vh',
          margin: 0,
          padding: 0,
          zIndex: -10,
          backgroundColor: 'black',
          overflow: 'hidden'
        }}
      >
        <Vortex
          backgroundColor="black"
          rangeY={300}
          particleCount={450}
          baseHue={45}
          baseRadius={2}
          rangeRadius={3}
          className="w-full h-full"
        />
      </div>

      {/* Overlay to improve contrast */}
      <div className="pointer-events-none fixed inset-0 -z-0 bg-gradient-to-b from-black/40 via-black/30 to-black/50" />

      {/* Foreground content */}
      <header className="relative z-10 px-4 pt-16 pb-6">
        <div className="mx-auto max-w-5xl">
          <h1 
            className="text-4xl font-bold tracking-tight md:text-5xl"
            style={{
              color: 'rgb(255, 206, 26)',
              textShadow: `
                0 0 5px rgba(255, 206, 26, 0.5),
                0 0 10px rgba(255, 206, 26, 0.3),
                1px 1px 2px rgba(0, 0, 0, 0.8),
                -1px -1px 2px rgba(0, 0, 0, 0.8)
              `
            }}
          >
            Karaoke Video Generator
          </h1>
          <p 
            className="mt-2 text-lg"
            style={{
              color: 'rgb(255, 206, 26)',
              textShadow: `
                0 0 3px rgba(255, 206, 26, 0.4),
                0.5px 0.5px 1px rgba(0, 0, 0, 0.8)
              `
            }}
          >
            Turn any YouTube song into a synced karaoke video with one click.
          </p>
        </div>
      </header>
      <main className="relative z-10 px-4 pb-10">
        <div className="mx-auto max-w-5xl">{children}</div>
      </main>
    </div>
  )
}

