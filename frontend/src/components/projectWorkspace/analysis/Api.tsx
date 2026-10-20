import { AnalysisCard } from './AnalysisCard'
import { AnalysisValue } from './AnalysisValue'
import { Route } from 'lucide-react'
interface ApiAnalysisProps {
  api: any
}

export function ApiAnalysis ({ api }: ApiAnalysisProps) {
  return (
    <AnalysisCard icon={<Route className='h-4 w-4' />} title='API'>
      <AnalysisValue label='Total routes' value={api.total_routes} />
    </AnalysisCard>
  )
}
