import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { ErrorBanner } from '../ErrorBanner'

describe('ErrorBanner', () => {
  it('does not render when message is null', () => {
    const { container } = render(<ErrorBanner message={null} />)
    expect(container.firstChild).toBeNull()
  })

  it('does not render when message is empty string', () => {
    const { container } = render(<ErrorBanner message="" />)
    expect(container.firstChild).toBeNull()
  })

  it('displays error message', () => {
    render(<ErrorBanner message="Something went wrong" />)
    expect(screen.getByText('Something went wrong')).toBeInTheDocument()
  })

  it('displays error title', () => {
    render(<ErrorBanner message="An error occurred" />)
    expect(screen.getByText('Error')).toBeInTheDocument()
  })

  it('displays close button when onClose is provided', () => {
    const mockOnClose = vi.fn()
    render(<ErrorBanner message="Error message" onClose={mockOnClose} />)
    
    const closeButton = screen.getByRole('button')
    expect(closeButton).toBeInTheDocument()
  })

  it('does not display close button when onClose is not provided', () => {
    render(<ErrorBanner message="Error message" />)
    
    const closeButton = screen.queryByRole('button')
    expect(closeButton).not.toBeInTheDocument()
  })

  it('calls onClose when close button is clicked', async () => {
    const user = userEvent.setup()
    const mockOnClose = vi.fn()
    render(<ErrorBanner message="Error message" onClose={mockOnClose} />)
    
    const closeButton = screen.getByRole('button')
    await user.click(closeButton)
    
    expect(mockOnClose).toHaveBeenCalledOnce()
  })

  it('displays long error messages', () => {
    const longMessage = 'This is a very long error message that should still be displayed correctly in the error banner component'
    render(<ErrorBanner message={longMessage} />)
    expect(screen.getByText(longMessage)).toBeInTheDocument()
  })
})
