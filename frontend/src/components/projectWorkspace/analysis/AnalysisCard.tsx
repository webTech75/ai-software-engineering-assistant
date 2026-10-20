import type { ReactNode } from 'react'

interface AnalysisCardProps {
  title: string
  icon?: ReactNode
  children: ReactNode
}

export function AnalysisCard ({ title, icon, children }: AnalysisCardProps) {
  return (
    <div className='rounded-lg border bg-card p-3'>
      <div className='mb-3 flex items-center justify-center gap-2'>
        {icon && <span className='text-primary'>{icon}</span>}

        <h3 className='text-sm font-semibold'>{title}</h3>
      </div>

      <div className='space-y-1 text-sm'>{children}</div>
    </div>
  )
}
