import { Progress } from "@/components/ui/progress"

interface GenerationProgressProps {
  status:
    | "idle"
    | "submitting"
    | "queued"
    | "processing"
    | "rendering"
    | "completed"
    | "failed"
  progress: number
  currentStage: string | null
}

export function GenerationProgress({
  status,
  progress,
  currentStage,
}: GenerationProgressProps) {
  if (status === "idle") {
    return (
      <div className="rounded-lg border border-white/10 bg-black/40 p-4 text-center text-slate-300">
        Ready when you are 👋
      </div>
    )
  }

  if (status === "completed") {
    return (
      <div className="rounded-lg border border-green-500/30 bg-green-500/10 p-4 text-center text-green-400">
        ✓ Video generation completed!
      </div>
    )
  }

  if (status === "failed") {
    return (
      <div className="rounded-lg border border-red-500/30 bg-red-500/10 p-4 text-center text-red-400">
        Generation failed. Check error message above.
      </div>
    )
  }

  return (
    <div className="space-y-3 rounded-lg border border-white/10 bg-black/40 p-4">
      <div className="flex items-center justify-between text-sm">
        <span className="text-slate-300">
          {status === "submitting"
            ? "Submitting..."
            : status === "queued"
            ? "Queued"
            : currentStage || "Processing..."}
        </span>
        <span className="text-slate-400">{Math.round(progress)}%</span>
      </div>
      <Progress value={progress} className="h-2" />
    </div>
  )
}

