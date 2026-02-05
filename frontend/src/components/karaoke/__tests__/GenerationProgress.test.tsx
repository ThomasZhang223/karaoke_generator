import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { GenerationProgress } from '../GenerationProgress'

describe('GenerationProgress', () => {
  it('renders idle state', () => {
    render(<GenerationProgress status="idle" progress={0} currentStage={null} />)
    expect(screen.getByText(/ready when you are/i)).toBeInTheDocument()
  })

  it('renders completed state', () => {
    render(<GenerationProgress status="completed" progress={100} currentStage={null} />)
    expect(screen.getByText(/video generation completed/i)).toBeInTheDocument()
  })

  it('renders progress with stage', () => {
    render(<GenerationProgress status="processing" progress={42} currentStage={'Fetching lyrics'} />)
    expect(screen.getByText(/fetching lyrics/i)).toBeInTheDocument()
    expect(screen.getByText(/42%/)).toBeInTheDocument()
  })
})
