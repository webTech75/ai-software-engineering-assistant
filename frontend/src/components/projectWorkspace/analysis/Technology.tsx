import { AnalysisCard } from './AnalysisCard'
import { AnalysisValue } from './AnalysisValue'
import { Cpu } from 'lucide-react'

interface TechnologyAnalysisProps {
  technology: any
}

export function TechnologyAnalysis ({ technology }: TechnologyAnalysisProps) {
  return (
    <AnalysisCard icon={<Cpu className='h-4 w-4' />} title='Technology'>
      <AnalysisValue label='Language' value={technology.language} />

      <AnalysisValue label='Framework' value={technology.framework} />

      <AnalysisValue label='Database' value={technology.database} />

      <AnalysisValue label='ORM' value={technology.orm} />

      <AnalysisValue label='Migration' value={technology.migration_tool} />
    </AnalysisCard>
  )
}
