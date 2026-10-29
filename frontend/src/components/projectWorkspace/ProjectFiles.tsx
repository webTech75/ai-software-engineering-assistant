import { useProjectScan } from '@/hooks/useProjectScan'
import { buildFileTree } from '@/utils/buildFileTree'
import FileTree from './FileTree'
import ProjectUpload from './ProjectUpload'
import { Folder, Loader2 } from 'lucide-react'
import { useQueryClient } from '@tanstack/react-query'
import type { UploadResponse } from '@/types/chat'

interface ProjectFilesProps {
  projectId: number
  onUploadSuccess: (response: UploadResponse) => void
}

export function ProjectFiles({
  projectId,
  onUploadSuccess,
}: ProjectFilesProps) {
  
  const { data: scan, isLoading, isFetching } = useProjectScan(projectId)
  const queryClient = useQueryClient()

  const files = scan?.structure?.files ?? []
console.log("FILES", files)
console.log("COMPLEXITY", scan?.complexity?.highest_complexity)
  return (
    <>
      <h2 className="mb-4 font-semibold">
        Project Files
      </h2>

      {/* Upload should always be visible */}
      <div className="border-b p-3">
        <ProjectUpload
          projectId={projectId}
          onSuccess={(response) => {
            queryClient.invalidateQueries({
              queryKey: ['project-scan', projectId],
            })

            onUploadSuccess(response)
          }}
        />
      </div>

      <div className="relative min-h-0 flex-1 overflow-visible">
        <div className="h-full overflow-y-auto">

          {isLoading || isFetching ? (
            <div className="flex items-center justify-center gap-2 rounded-lg border border-blue-500/30 bg-blue-500/10 px-3 py-2 text-sm text-blue-400 animate-pulse">
              <Loader2 className="h-4 w-4 animate-spin" />
              <span>
                Neura is processing project files...
              </span>
            </div>

          ) : files.length > 0 ? (
            <FileTree
              nodes={buildFileTree(
                files,
                scan?.complexity?.highest_complexity ?? []
              )}
            />

          ) : (
            <div className="flex flex-col items-center justify-center py-8 text-center">
              <Folder className="mb-3 h-8 w-8 text-muted-foreground" />

              <p className="text-sm font-medium">
                No files available yet
              </p>

              <p className="mt-1 text-xs text-muted-foreground">
                Upload a project ZIP file to explore source files.
              </p>
            </div>
          )}

        </div>
      </div>
    </>
  )
}