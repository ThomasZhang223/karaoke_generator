import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

interface UrlFormProps {
  isSubmitting: boolean
  onSubmit: (data: {
    youtubeUrl: string
    style?: "classic" | "neon" | "minimal"
    quality?: "standard" | "high"
  }) => void
}

export function UrlForm({ isSubmitting, onSubmit }: UrlFormProps) {
  const [youtubeUrl, setYoutubeUrl] = useState("")
  const [style, setStyle] = useState<"classic" | "neon" | "minimal">("classic")
  const [quality, setQuality] = useState<"standard" | "high">("standard")
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)

    if (!youtubeUrl.trim()) {
      setError("Please enter a YouTube URL")
      return
    }

    if (
      !youtubeUrl.includes("youtube.com") &&
      !youtubeUrl.includes("youtu.be")
    ) {
      setError("Please enter a valid YouTube URL")
      return
    }

    onSubmit({ youtubeUrl: youtubeUrl.trim(), style, quality })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="youtube-url">YouTube URL</Label>
        <Input
          id="youtube-url"
          type="url"
          placeholder="https://www.youtube.com/watch?v=..."
          value={youtubeUrl}
          onChange={(e) => {
            setYoutubeUrl(e.target.value)
            setError(null)
          }}
          disabled={isSubmitting}
          className="bg-black/40 border-white/20 text-white placeholder:text-slate-400"
        />
        {error && (
          <p className="text-sm text-red-400">{error}</p>
        )}
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="style">Style</Label>
          <Select
            value={style}
            onValueChange={(value) =>
              setStyle(value as "classic" | "neon" | "minimal")
            }
            disabled={isSubmitting}
          >
            <SelectTrigger
              id="style"
              className="bg-black/40 border-white/20 text-white"
            >
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="classic">Classic</SelectItem>
              <SelectItem value="neon">Neon</SelectItem>
              <SelectItem value="minimal">Minimal</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="quality">Quality</Label>
          <Select
            value={quality}
            onValueChange={(value) =>
              setQuality(value as "standard" | "high")
            }
            disabled={isSubmitting}
          >
            <SelectTrigger
              id="quality"
              className="bg-black/40 border-white/20 text-white"
            >
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="standard">Standard</SelectItem>
              <SelectItem value="high">High</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      <Button
        type="submit"
        disabled={isSubmitting}
        className="w-full bg-white/10 hover:bg-white/20 text-white border border-white/20"
      >
        {isSubmitting ? "Generating..." : "Generate Karaoke Video"}
      </Button>

      <p className="text-xs text-slate-400 text-center">
        Longer songs may take a few minutes to process.
      </p>
    </form>
  )
}

