// import { useEffect, useState } from 'react'
import { scanProjectRequest } from '@/api/requests'
// import type { ProjectScan } from '@/types/projectScan'
import { buildFileTree } from '@/utils/buildFileTree'
import FileTree from './FileTree'
import ProjectUpload from './ProjectUpload'
import { Folder } from 'lucide-react'
import { useQuery, useQueryClient } from '@tanstack/react-query'

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

  const { data: scan, isLoading } = useQuery({
    queryKey: ['project-files', projectId],
    queryFn: () => scanProjectRequest(projectId)
  })
  const queryClient = useQueryClient()

  const hiddenFiles = [
    '.env',
    '.env.example',
    '.gitignore',
    '__init__.py',
    'assistant.db',
    'script.py.mako',
    'README'
  ]

  const files = scan?.structure.files.filter(file => {
    const filename = file.split('/').pop()
    return !hiddenFiles.includes(filename || '')
  })

  return (
    <>
      <h2 className='mb-4 font-semibold'>Project Files</h2>
      <div className='border-b p-3'>
        <ProjectUpload
          projectId={projectId}
          onSuccess={() =>
            queryClient.invalidateQueries({
              queryKey: ['project-files', projectId]
            })
          }
        />
      </div>

      <div className='min-h-0 flex-1 overflow-y-auto'>
        <div className='space-y-1 text-sm'>
          {isLoading ? (
            <p className='text-muted-foreground'>Loading files...</p>
          ) : files && files.length > 0 ? (
            <FileTree nodes={buildFileTree(files ?? [])} />
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
