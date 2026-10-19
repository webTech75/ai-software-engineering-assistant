import { useState } from 'react'
import { ChevronDown, ChevronRight, File, Folder } from 'lucide-react'

import type { FileTreeNode } from '@/utils/buildFileTree'

interface FileTreeProps {
  nodes: FileTreeNode[]
}

export default function FileTree ({ nodes }: FileTreeProps) {
  return (
    <div>
      {nodes.map(node => (
        <FileTreeItem key={node.path} node={node} />
      ))}
    </div>
  )
}

function FileTreeItem ({ node }: { node: FileTreeNode }) {
  const [expanded, setExpanded] = useState(true)

  if (node.type === 'file') {
    return (
      <div className='flex items-center gap-2 py-1 text-sm'>
        <File className='h-4 w-4 text-muted-foreground' />
        <span className='text-foreground hover:text-primary'>{node.name}</span>
      </div>
    )
  }

  return (
    <div>
      <button
        onClick={() => setExpanded(!expanded)}
        className='flex items-center gap-2 py-1 text-sm hover:text-primary'
      >
        {expanded ? (
          <ChevronDown className='h-4 w-4' />
        ) : (
          <ChevronRight className='h-4 w-4' />
        )}

        <Folder className='h-4 w-4 text-yellow-500' />

        <span className='font-medium text-blue-600 dark:text-blue-400'>
          {node.name}
        </span>
      </button>

      {expanded && (
        <div className='ml-4'>
          <FileTree nodes={node.children} />
        </div>
      )}
    </div>
  )
}
