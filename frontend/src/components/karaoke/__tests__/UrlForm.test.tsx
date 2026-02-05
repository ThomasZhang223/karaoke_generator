import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { UrlForm } from '../UrlForm'

describe('UrlForm', () => {
  it('shows validation error for empty URL', async () => {
    const user = userEvent.setup()
    const onSubmit = vi.fn()
    render(<UrlForm isSubmitting={false} onSubmit={onSubmit} />)
    await user.click(screen.getByRole('button', { name: /generate karaoke/i }))
    expect(screen.getByText(/please enter a youtube url/i)).toBeInTheDocument()
    expect(onSubmit).not.toHaveBeenCalled()
  })

  it('submits valid URL with defaults', async () => {
    const user = userEvent.setup()
    const onSubmit = vi.fn()
    render(<UrlForm isSubmitting={false} onSubmit={onSubmit} />)
    const input = screen.getByLabelText(/YouTube URL/i)
    await user.type(input, 'https://youtu.be/dQw4w9WgXcQ')
    await user.click(screen.getByRole('button', { name: /generate karaoke/i }))
    expect(onSubmit).toHaveBeenCalledWith({ youtubeUrl: 'https://youtu.be/dQw4w9WgXcQ', style: 'classic', quality: 'standard' })
  })
})
