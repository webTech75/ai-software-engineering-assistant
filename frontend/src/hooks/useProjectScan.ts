import { useQuery } from '@tanstack/react-query'

import { scanProjectRequest } from '@/api/requests'

export function useProjectScan (projectId: number) {
  return useQuery({
    queryKey: ['project-scan', projectId],
    queryFn: () => scanProjectRequest(projectId)
  })
}
