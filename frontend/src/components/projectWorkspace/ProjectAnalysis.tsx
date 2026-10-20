import { useProjectScan } from '@/hooks/useProjectScan'
import { TechnologyAnalysis } from './analysis/Technology'
import { StatisticsAnalysis } from './analysis/Statistics'
import { DependencyAnalysis } from './analysis/Dependency'
import { ApiAnalysis } from './analysis/Api'
import { MetricsAnalysis } from './analysis/Metrics'
import { ComplexityAnalysis } from './analysis/complexity'
import { DatabaseAnalysis } from './analysis/Database'
import ReviewSummary from './ReviewSummary'
import { Sparkles } from 'lucide-react'

interface ProjectAnalysisProps {
  projectId: number
}

export function ProjectAnalysis ({ projectId }: ProjectAnalysisProps) {
  const { data: scan, isLoading } = useProjectScan(projectId)

  function hasAnalysisData (scan: any) {
    return scan && scan.statistics && scan.statistics.total_files > 0
  }

  if (isLoading) {
    return (
      <p className='text-sm text-center text-muted-foreground'>
        Loading analysis...
      </p>
    )
  }

  if (!hasAnalysisData(scan)) {
    return (
      <section className='rounded-lg border bg-card p-6 text-center'>
        <h2 className='font-semibold'>Project Analysis</h2>

        <p className='mt-2 text-sm text-muted-foreground'>
          Upload a project to generate analysis.
        </p>
      </section>
    )
  }

  if (!scan) {
    return null
  }

  return (
    <section className='space-y-4'>
      <div className='flex items-center justify-center gap-3'>
        <Sparkles className='h-5 w-5 text-primary' />

        <h2 className='text-xl font-semibold'>Project Analysis</h2>

        <Sparkles className='h-5 w-5 text-primary' />
      </div>
      <ReviewSummary scan={scan} />
      <div className='grid gap-3 sm:grid-cols-2 lg:grid-cols-3'>
        <TechnologyAnalysis technology={scan.technology} />

        <StatisticsAnalysis statistics={scan.statistics} />

        <DependencyAnalysis dependencies={scan.dependencies} />

        <ApiAnalysis api={scan.api} />

        <MetricsAnalysis metrics={scan.metrics} />

        <ComplexityAnalysis complexity={scan.complexity} />

        <DatabaseAnalysis database={scan.database} />
      </div>
    </section>
  )
}
