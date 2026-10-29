import { AnalysisCard } from './AnalysisCard'
import { AnalysisValue } from './AnalysisValue'
import { Database } from 'lucide-react'

interface DatabaseAnalysisProps {
  database: any
}

export function DatabaseAnalysis({ database }: DatabaseAnalysisProps) {
  return (
    <AnalysisCard
      icon={<Database className="h-4 w-4" />}
      title="Database"
    >
      <AnalysisValue
        label="Engine"
        value={database.database}
      />

      <AnalysisValue
        label="ORM"
        value={database.orms?.join(', ')}
      />

      <AnalysisValue
        label="Migration"
        value={database.migration_tools?.join(', ')}
      />
    </AnalysisCard>
  )
}