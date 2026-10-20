import { AnalysisCard } from './AnalysisCard'
import { AnalysisValue } from './AnalysisValue'
import { BarChart3 } from 'lucide-react'
interface StatisticsAnalysisProps {
  statistics: any
}

export function StatisticsAnalysis ({ statistics }: StatisticsAnalysisProps) {
  return (
    <AnalysisCard icon={<BarChart3 className='h-4 w-4' />} title='Statistics'>
      <AnalysisValue label='Files' value={statistics.total_files} />

      <AnalysisValue label='Directories' value={statistics.total_directories} />

      <AnalysisValue label='Size' value={`${statistics.total_size} bytes`} />

      <AnalysisValue
        label='Average size'
        value={statistics.average_file_size}
      />

      <AnalysisValue label='Largest file' value={statistics.largest_file} />
    </AnalysisCard>
  )
}
