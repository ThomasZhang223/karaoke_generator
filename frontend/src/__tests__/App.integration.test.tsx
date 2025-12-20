import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from '../App'

// Mock API client module
vi.mock('../lib/apiClient', async () => {
  return {
    startGeneration: vi.fn(async () => ({ jobId: 'job-123' })),
    getJobStatus: vi.fn(async () => ({
      jobId: 'job-123',
      status: 'completed',
      progress: 100,
      stage: 'Rendering video',
      videoUrl: '/api/v1/karaoke/download/job-123',
      errorMessage: null,
    })),
  }
})

describe('App integration', () => {
  it('submits url and shows completed state with video', async () => {
    const user = userEvent.setup()
    render(<App />)

    const input = screen.getByLabelText(/YouTube URL/i)
    await user.type(input, 'https://youtu.be/dQw4w9WgXcQ')
    await user.click(screen.getByRole('button', { name: /generate karaoke/i }))

    // After mocked polling, should show completed status
    expect(await screen.findByText(/video generation completed/i)).toBeInTheDocument()
    // Placeholder should not be present when completed
    expect(screen.queryByText(/your generated karaoke video will appear here/i)).not.toBeInTheDocument()
  })
})
