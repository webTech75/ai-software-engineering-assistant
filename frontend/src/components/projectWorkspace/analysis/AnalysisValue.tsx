interface AnalysisValueProps {
  label: string
  value: React.ReactNode
  variant?: 'default' | 'success' | 'warning' | 'danger'
}

export function AnalysisValue ({
  label,
  value,
  variant = 'default'
}: AnalysisValueProps) {
  const displayValue =
    value === null || value === undefined || value === '' ? 'N/A' : value

  const variants = {
    default: 'bg-primary/10 text-primary',
    success: 'bg-green-500/10 text-green-500',
    warning: 'bg-yellow-500/10 text-yellow-500',
    danger: 'bg-red-500/10 text-red-500'
  }

  return (
    <div className='flex items-center justify-between gap-4'>
      <span className='text-muted-foreground'>{label}</span>

      <span
        className={`
          rounded-md
          px-2
          py-0.5
          text-xs
          font-medium
          ${variants[variant]}
        `}
      >
        {displayValue}
      </span>
    </div>
  )
}
