import { useProjectScan } from '@/hooks/useProjectScan'
import { buildFileTree } from '@/utils/buildFileTree'
import FileTree from './FileTree'
import ProjectUpload from './ProjectUpload'
import { Folder, Loader2 } from 'lucide-react'
import { useQueryClient } from '@tanstack/react-query'

interface ProjectFilesProps {
  projectId: number
}

export function ProjectFiles ({ projectId }: ProjectFilesProps) {
  // const [scan, setScan] = useState<ProjectScan | null>(null)
  // const [loading, setLoading] = useState(false)

  // useEffect(() => {
  //   loadFiles()
  // }, [projectId])

  // async function loadFiles () {
  //   try {
  //     setLoading(true)
  //     const data = await scanProjectRequest(projectId)

  //     setScan(data)
  //   } catch (error) {
  //     console.error(error)
  //   } finally {
  //     setLoading(false)
  //   }
  // }

  const { data: scan, isLoading, isFetching } = useProjectScan(projectId)
  const queryClient = useQueryClient()
  const files = scan?.structure.files ?? []

  console.log('scan>>>>>', scan)

  return (
    <>
      <h2 className='mb-4 font-semibold'>Project Files</h2>
      <div className='border-b p-3'>
        <ProjectUpload
          projectId={projectId}
          onSuccess={() =>
            queryClient.invalidateQueries({
              queryKey: ['project-scan', projectId]
            })
          }
        />
      </div>

      <div className='relative min-h-0 flex-1 overflow-visible'>
        <div className='h-full overflow-y-auto'>
          {isLoading || isFetching ? (
            <div className='flex items-center justify-center gap-2 rounded-lg border border-blue-500/30 bg-blue-500/10 px-3 py-2 text-sm text-blue-400 animate-pulse'>
              <Loader2 className='h-4 w-4 animate-spin' />
              <span>Neura is processing project files...</span>
            </div>
          ) : files && files.length > 0 ? (
            <FileTree
              nodes={buildFileTree(
                files ?? [],
                scan?.review?.file_issues ?? {}
              )}
            />
          ) : (
            <div className='flex flex-col items-center justify-center py-8 text-center'>
              <Folder className='h-8 w-8 text-muted-foreground mb-3' />

              <p className='text-sm font-medium'>No files found</p>

              <p className='mt-1 text-xs text-muted-foreground'>
                Upload a project containing source files to start analysis.
              </p>
            </div>
          )}
        </div>
      </div>
    </>
  )
}
