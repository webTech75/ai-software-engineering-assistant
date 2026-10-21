import { AnalysisCard } from './AnalysisCard'
import { AnalysisValue } from './AnalysisValue'
import { Cpu } from 'lucide-react'

interface TechnologyAnalysisProps {
  technology: any
}

function formatList (value: string[] | null | undefined) {
  if (!value || value.length === 0) {
    return 'N/A'
  }

  return value.join(', ')
}

export function TechnologyAnalysis ({ technology }: TechnologyAnalysisProps) {
  return (
    <AnalysisCard icon={<Cpu className='h-4 w-4' />} title='Technology'>
      <AnalysisValue
        label='Languages'
        value={formatList(technology.languages)}
      />

      <AnalysisValue
        label='Frameworks'
        value={formatList(technology.frameworks)}
      />

      <AnalysisValue label='Database' value={technology.database ?? 'N/A'} />

      <AnalysisValue label='ORMs' value={formatList(technology.orms)} />

      <AnalysisValue
        label='Migration'
        value={formatList(technology.migration_tools)}
      />

      <AnalysisValue
        label='Package Manager'
        value={technology.package_manager ?? 'N/A'}
      />

      <AnalysisValue
        label='Build Tools'
        value={formatList(technology.build_tools)}
      />

      <AnalysisValue
        label='Styling'
        value={formatList(technology.styling_tools)}
      />

      <AnalysisValue
        label='Testing'
        value={formatList(technology.testing_tools)}
      />
    </AnalysisCard>
  )
}
