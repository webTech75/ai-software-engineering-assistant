import { AnalysisCard } from './AnalysisCard'
import { AnalysisValue } from './AnalysisValue'
import { Package } from 'lucide-react'
interface DependencyAnalysisProps {
  dependencies: any
}

export function DependencyAnalysis ({ dependencies }: DependencyAnalysisProps) {
  return (
    <AnalysisCard icon={<Package className='h-4 w-4' />} title='Dependencies'>
      <AnalysisValue label='Manager' value={dependencies.manager} />

      <AnalysisValue label='File' value={dependencies.file} />

      <AnalysisValue label='Packages' value={dependencies.total} />
    </AnalysisCard>
  )
}
