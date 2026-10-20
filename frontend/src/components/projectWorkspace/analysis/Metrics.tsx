import { AnalysisCard } from './AnalysisCard'
import { AnalysisValue } from './AnalysisValue'
import { Activity } from 'lucide-react'
interface MetricsAnalysisProps {
  metrics: any
}

export function MetricsAnalysis ({ metrics }: MetricsAnalysisProps) {
  return (
    <AnalysisCard icon={<Activity className='h-4 w-4' />} title='Metrics'>
      <AnalysisValue label='Files analyzed' value={metrics.files_analyzed} />

      <AnalysisValue label='Total lines' value={metrics.total_lines} />

      <AnalysisValue label='Code lines' value={metrics.code_lines} />
    </AnalysisCard>
  )
}
