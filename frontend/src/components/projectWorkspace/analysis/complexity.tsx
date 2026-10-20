import { AnalysisCard } from './AnalysisCard'
import { AnalysisValue } from './AnalysisValue'
import { Gauge } from 'lucide-react'
interface ComplexityAnalysisProps {
  complexity: any
}

export function ComplexityAnalysis ({ complexity }: ComplexityAnalysisProps) {
  return (
    <AnalysisCard icon={<Gauge className='h-4 w-4' />} title='Complexity'>
      <AnalysisValue label='Files analyzed' value={complexity.files_analyzed} />

      <AnalysisValue label='Functions' value={complexity.total_functions} />

      <AnalysisValue label='Complexity' value={complexity.total_complexity} />
    </AnalysisCard>
  )
}
