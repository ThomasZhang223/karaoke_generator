import { Download, Copy, Video } from "lucide-react"
import { Button } from "@/components/ui/button"

interface VideoResultProps {
  videoUrl: string | null
  status:
    | "idle"
    | "submitting"
    | "queued"
    | "processing"
    | "rendering"
    | "completed"
    | "failed"
}

export function VideoResult({ videoUrl, status }: VideoResultProps) {
  const handleDownload = () => {
    if (!videoUrl) return
    const link = document.createElement("a")
    link.href = videoUrl
    link.download = "karaoke-video.mp4"
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  const handleCopyLink = async () => {
    if (!videoUrl) return
    try {
      await navigator.clipboard.writeText(videoUrl)
      // You could add a toast notification here
    } catch (err) {
      console.error("Failed to copy link:", err)
    }
  }

  if (!videoUrl || status !== "completed") {
    return (
      <div className="flex h-full min-h-[400px] flex-col items-center justify-center rounded-lg border border-white/10 bg-black/40 p-8 text-center">
        <Video className="mb-4 h-16 w-16 text-slate-500" />
        <p className="text-slate-400">
          Your generated karaoke video will appear here.
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="rounded-lg border border-white/10 bg-black/40 p-2">
        <video
          src={videoUrl}
          controls
          className="w-full rounded-md"
          preload="metadata"
        >
          Your browser does not support the video tag.
        </video>
      </div>
      <div className="flex gap-2">
        <Button
          onClick={handleDownload}
          className="flex-1 bg-white/10 hover:bg-white/20 text-white border border-white/20"
        >
          <Download className="mr-2 h-4 w-4" />
          Download
        </Button>
        <Button
          onClick={handleCopyLink}
          variant="outline"
          className="flex-1 border-white/20 text-white hover:bg-white/10"
        >
          <Copy className="mr-2 h-4 w-4" />
          Copy Link
        </Button>
      </div>
    </div>
  )
}

