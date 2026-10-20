import { AnalysisCard } from './AnalysisCard'
import { AnalysisValue } from './AnalysisValue'
import { Database } from 'lucide-react'
interface DatabaseAnalysisProps {
  database: any
}

export function DatabaseAnalysis ({ database }: DatabaseAnalysisProps) {
  return (
    <AnalysisCard icon={<Database className='h-4 w-4' />} title='Database'>
      <AnalysisValue label='Engine' value={database.engine} />

      <AnalysisValue label='Migration' value={database.migration_tool} />

      <AnalysisValue
        label='Files'
        value={database.database_files?.length ?? 0}
      />
    </AnalysisCard>
  )
}
