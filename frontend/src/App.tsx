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
  const [videoUrl, setVideoUrl] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [jobId, setJobId] = useState<string | null>(null)

  // Poll for job status
  useEffect(() => {
    if (!jobId) return

    const interval = setInterval(async () => {
      try {
        const res = await getJobStatus(jobId)
        setProgress(res.progress ?? 0)
        setCurrentStage(res.stage ?? null)
        setStatus(mapBackendStatusToFrontend(res.status))

        if (res.status === "completed") {
          setVideoUrl(res.videoUrl ?? null)
          clearInterval(interval)
        } else if (res.status === "failed") {
          setError(res.errorMessage ?? "Unknown error while generating video.")
          clearInterval(interval)
        }
      } catch (e) {
        setStatus("failed")
        setError(
          e instanceof Error
            ? e.message
            : "Lost connection to the server. Please try again."
        )
        clearInterval(interval)
      }
    }, 2500)

    return () => clearInterval(interval)
  }, [jobId])

  const handleSubmit = async (data: StartGenerationRequest) => {
    setError(null)
    setStatus("submitting")
    setProgress(0)
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
                progress={progress}
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
