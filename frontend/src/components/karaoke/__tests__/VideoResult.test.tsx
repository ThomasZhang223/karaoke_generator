import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { VideoResult } from '../VideoResult'

describe('VideoResult', () => {
  it('shows placeholder when not completed or no url', () => {
    render(<VideoResult videoUrl={null} status="processing" />)
    expect(screen.getByText(/your generated karaoke video will appear here/i)).toBeInTheDocument()
  })

  it('renders video when completed', () => {
    render(<VideoResult videoUrl={'http://example.com/video.mp4'} status="completed" />)
    expect(screen.getByTestId('video')).toBeInTheDocument()
  })

  it('copies link to clipboard', async () => {
    const user = userEvent.setup()
    const spy = vi.spyOn(navigator.clipboard, 'writeText')
    render(<VideoResult videoUrl={'http://example.com/video.mp4'} status="completed" />)
    await user.click(screen.getByRole('button', { name: /copy link/i }))
    expect(spy).toHaveBeenCalledWith('http://example.com/video.mp4')
  })
})
