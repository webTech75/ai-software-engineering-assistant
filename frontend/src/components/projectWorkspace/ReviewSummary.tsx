import { Bug, ShieldAlert, Brain, FlaskConical } from 'lucide-react'

interface ReviewSummaryProps {
  scan: any
}

interface FileIssue {
  type: string
  severity: string
  message: string
  line?: number
}

function getColor (score: number) {
  if (score >= 90) return 'bg-green-500'
  if (score >= 70) return 'bg-yellow-500'
  if (score >= 50) return 'bg-orange-500'

  return 'bg-red-500'
}

function getTextColor (score: number) {
  if (score >= 90) return 'text-green-500'
  if (score >= 70) return 'text-yellow-500'
  if (score >= 50) return 'text-orange-500'

  return 'text-red-500'
}

export default function ReviewSummary ({ scan }: ReviewSummaryProps) {
  const fileIssues = scan?.review?.file_issues ?? {}

  const allIssues = Object.values(fileIssues).flat() as FileIssue[]

  const bugCount = allIssues.filter(issue => issue.type === 'bug').length

  const securityCount = allIssues.filter(
    issue => issue.type === 'security'
  ).length

  const complexityCount = allIssues.filter(
    issue => issue.type === 'complexity'
  ).length

  const metrics = [
    {
      title: 'Bugs',
      count: bugCount,
      label: bugCount === 1 ? 'issue' : 'issues',
      score: Math.round(100 / (1 + bugCount * 0.1)),
      icon: <Bug className='h-4 w-4 text-red-500' />
    },
    {
      title: 'Security',
      count: securityCount,
      label: securityCount === 1 ? 'finding' : 'findings',
      score: Math.round(100 / (1 + securityCount * 0.25)),
      icon: <ShieldAlert className='h-4 w-4 text-red-500' />
    },
    {
      title: 'Complexity',
      count: complexityCount,
      label: complexityCount === 1 ? 'function' : 'functions',
      score: Math.round(100 / (1 + complexityCount * 0.1)),
      icon: <Brain className='h-4 w-4 text-orange-500' />
    },
    {
      title: 'Tests',
      count: scan?.tests?.total_test_files ?? 0,
      label: scan?.tests?.total_test_files === 1 ? 'test' : 'tests',
      score: scan?.tests?.total_test_files ? 100 : 0,
      icon: <FlaskConical className='h-4 w-4 text-yellow-500' />
    }
  ]
  return (
    <div className='mb-6 space-y-6'>
      {/* Overall Health */}
      {/* Overall Health */}
      <div className='rounded-lg border bg-card p-4'>
        <div className='flex items-center gap-2 mb-2'>
          <span className='text-sm font-semibold'>Overall Health</span>
        </div>

        <div className='flex items-center gap-2'>
          <div className='h-2 flex-1 overflow-hidden rounded-full bg-muted'>
            <div
              className={`h-2 rounded-full ${getColor(
                scan?.review?.health_score ?? 0
              )}`}
              style={{
                width: `${scan?.review?.health_score ?? 0}%`
              }}
            />
          </div>

          <span
            className={`text-xs font-semibold ${getTextColor(
              scan?.review?.health_score ?? 0
            )}`}
          >
            {scan?.review?.health_score ?? 0}%
          </span>
        </div>
      </div>

      {/* Category Gauges  */}
      <div className='grid grid-cols-4 gap-6'>
        {metrics.map(metric => (
          <div key={metric.title} className='space-y-2'>
            <div className='flex items-center gap-2'>
              {metric.icon}

              <span className='text-sm font-semibold'>{metric.title}</span>
            </div>

            <div className='flex items-center gap-2'>
              <div className='h-2 flex-1 overflow-hidden rounded-full bg-muted'>
                <div
                  className={`h-2 rounded-full ${getColor(metric.score)}`}
                  style={{
                    width: `${metric.score}%`
                  }}
                />
              </div>

              <span
                className={`text-xs font-semibold ${getTextColor(
                  metric.score
                )}`}
              >
                {metric.score}%
              </span>
            </div>

            <p className='text-xs text-muted-foreground'>
              {metric.count} {metric.label}
            </p>
          </div>
        ))}
      </div>

      {/* Summary */}
      {scan?.review?.summary && (
        <div className='rounded-lg border bg-card p-4'>
          <h3 className='mb-2 text-sm font-semibold'>Summary</h3>

          <p className='text-sm text-muted-foreground'>{scan.review.summary}</p>
        </div>
      )}

      {/* Strengths */}
      {scan?.review?.strengths?.length > 0 && (
        <div className='rounded-lg border bg-card p-4'>
          <h3 className='mb-3 text-sm font-semibold'>Strengths</h3>

          <ul className='space-y-2'>
            {scan.review.strengths.map((strength: string, index: number) => (
              <li
                key={index}
                className='flex items-center gap-2 text-sm text-muted-foreground'
              >
                <span className='text-green-500'>✓</span>

                {strength}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Recommendations */}
      {scan?.review?.recommendations?.length > 0 && (
        <div className='rounded-lg border bg-card p-4'>
          <h3 className='mb-3 text-sm font-semibold'>Recommendations</h3>

          <ul className='space-y-2'>
            {scan.review.recommendations.map(
              (recommendation: string, index: number) => (
                <li
                  key={index}
                  className='flex items-start gap-2 text-sm text-muted-foreground'
                >
                  <span className='mt-0.5 text-yellow-500'>⚠</span>

                  {recommendation}
                </li>
              )
            )}
          </ul>
        </div>
      )}
    </div>
  )
}
