import { useState, useEffect } from "react"
import { AppShell } from "@/components/layout/AppShell"
import { Card, CardContent } from "@/components/ui/card"
import { UrlForm } from "@/components/karaoke/UrlForm"
import { GenerationProgress } from "@/components/karaoke/GenerationProgress"
import { VideoResult } from "@/components/karaoke/VideoResult"
import { ErrorBanner } from "@/components/karaoke/ErrorBanner"
import { startGeneration, getJobStatus } from "@/lib/apiClient"
import type {
  GenerationStatus,
  StartGenerationRequest,
} from "@/lib/types"

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000"

type FrontendStatus =
  | "idle"
  | "submitting"
  | "queued"
  | "processing"
  | "rendering"
  | "completed"
  | "failed"

function mapBackendStatusToFrontend(
  backendStatus: GenerationStatus
): FrontendStatus {
  switch (backendStatus) {
    case "queued":
      return "queued"
    case "processing":
      return "processing"
    case "rendering":
      return "rendering"
    case "completed":
      return "completed"
    case "failed":
      return "failed"
    default:
      return "processing"
  }
}

function App() {
  const [status, setStatus] = useState<FrontendStatus>("idle")
  const [currentStage, setCurrentStage] = useState<string | null>(null)
  const [progress, setProgress] = useState<number>(0)
  const [animatedProgress, setAnimatedProgress] = useState<number>(0)
  const [videoUrl, setVideoUrl] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [jobId, setJobId] = useState<string | null>(null)

  // Animate progress smoothly
  useEffect(() => {
    if (progress === animatedProgress) return

    // Determine animation duration based on progress change
    const diff = Math.abs(progress - animatedProgress)
    let duration = 300 // Default 300ms for small changes
    
    // Special handling for start: animate from 0% to 10% over 1 second
    if (animatedProgress === 0 && progress >= 10) {
      duration = 1000
    }
    // Special handling for end: animate from 80% to 100% over 1.5 seconds
    else if (animatedProgress >= 80 && progress === 100) {
      duration = 1500
    }
    // For larger jumps, use longer duration
    else if (diff > 20) {
      duration = 600
    } else if (diff > 10) {
      duration = 400
    }

    const startProgress = animatedProgress
    const endProgress = progress
    const startTime = Date.now()

    const animate = () => {
      const elapsed = Date.now() - startTime
      const progressRatio = Math.min(elapsed / duration, 1)
      
      // Use easing function for smoother animation (ease-out)
      const eased = 1 - Math.pow(1 - progressRatio, 3)
      const currentProgress = startProgress + (endProgress - startProgress) * eased
      
      setAnimatedProgress(currentProgress)

      if (progressRatio < 1) {
        requestAnimationFrame(animate)
      } else {
        setAnimatedProgress(endProgress)
      }
    }

    requestAnimationFrame(animate)
  }, [progress, animatedProgress])

  // Poll for job status
  useEffect(() => {
    console.log("[Frontend] useEffect triggered, jobId:", jobId)
    if (!jobId) {
      console.log("[Frontend] No jobId, skipping polling")
      return
    }

    let interval: NodeJS.Timeout | null = null

    // Poll immediately, then every 1 second for faster updates
    const pollStatus = async () => {
      console.log("[Frontend] Polling for job status...")
      try {
        console.log("[Frontend] About to call getJobStatus with jobId:", jobId)
        const res = await getJobStatus(jobId)
        console.log("[Frontend] getJobStatus returned:", res)
        // Debug: Log what we received
        console.log("[Frontend] Poll result:", {
          status: res.status,
          progress: res.progress,
          stage: res.stage,
          jobId: res.jobId
        })
        
        // Update state - force updates even if values are the same
        const newProgress = res.progress ?? 0
        const newStage = res.stage ?? null
        const newStatus = mapBackendStatusToFrontend(res.status)
        
        console.log("[Frontend] Updating state:", {
          progress: newProgress,
          stage: newStage,
          status: newStatus
        })
        
        setProgress(newProgress)
        setCurrentStage(newStage)
        setStatus(newStatus)

        if (res.status === "completed") {
          // Prepend API base URL if videoUrl is a relative path
          const videoUrl = res.videoUrl
          const fullVideoUrl = videoUrl?.startsWith("http")
            ? videoUrl
            : videoUrl
            ? `${API_BASE_URL}${videoUrl}`
            : null
          setVideoUrl(fullVideoUrl)
          if (interval) clearInterval(interval)
        } else if (res.status === "failed") {
          setError(res.errorMessage ?? "Unknown error while generating video.")
          if (interval) clearInterval(interval)
        }
      } catch (e) {
        console.error("[Frontend] Poll error:", e)
        setStatus("failed")
        setError(
          e instanceof Error
            ? e.message
            : "Lost connection to the server. Please try again."
        )
        if (interval) clearInterval(interval)
      }
    }
    
    // Poll immediately
    pollStatus()
    
    // Then poll every 1 second for faster updates
    interval = setInterval(pollStatus, 1000)

    return () => {
      if (interval) clearInterval(interval)
    }
  }, [jobId])

  const handleSubmit = async (data: StartGenerationRequest) => {
    setError(null)
    setStatus("submitting")
    setProgress(0)
    setAnimatedProgress(0)
    setCurrentStage(null)
    setVideoUrl(null)

    try {
      const response = await startGeneration(data)
      setJobId(response.jobId)
      setStatus("queued")
    } catch (e) {
      setStatus("failed")
      setError(
        e instanceof Error
          ? e.message
          : "Failed to start generation. Please try again."
      )
    }
  }

  const handleCloseError = () => {
    setError(null)
  }

  return (
    <AppShell>
      <Card className="bg-black/60 border-white/10 backdrop-blur-xl">
        <CardContent className="p-6 md:p-8">
          <div className="grid gap-8 md:grid-cols-[minmax(0,1.4fr)_minmax(0,1fr)] items-start">
            {/* Left: form + status */}
            <div className="space-y-6">
              <div>
                <h2 className="text-2xl font-semibold mb-2">
                  Generate a Karaoke Video
                </h2>
              </div>

              <UrlForm
                isSubmitting={status === "submitting"}
                onSubmit={handleSubmit}
              />

              <ErrorBanner message={error} onClose={handleCloseError} />

              <GenerationProgress
                status={status}
                progress={animatedProgress}
                currentStage={currentStage}
              />
            </div>

            {/* Right: preview */}
            <div>
              <VideoResult videoUrl={videoUrl} status={status} />
            </div>
          </div>
        </CardContent>
      </Card>
    </AppShell>
  )
}

export default App
