import { useState } from 'react'
import {
  ChevronDown,
  ChevronRight,
  File,
  Folder,
  AlertTriangle
} from 'lucide-react'

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

  const [showTooltip, setShowTooltip] = useState(false)

  const [position, setPosition] = useState({
    top: 0,
    left: 0
  })

  function handleMouseEnter (event: React.MouseEvent<HTMLDivElement>) {
    const rect = event.currentTarget.getBoundingClientRect()

    setPosition({
      top: rect.top,
      left: rect.right
    })

    setShowTooltip(true)
  }

  function handleMouseLeave () {
    setShowTooltip(false)
  }

  if (node.type === 'file') {
    return (
      <div
        className='flex items-center gap-2 py-1 text-sm'
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
      >
        <File className='h-4 w-4 text-muted-foreground' />

        <span className='text-foreground hover:text-primary'>{node.name}</span>

        {node.issues && node.issues.length > 0 && (
          <AlertTriangle className='h-4 w-4 text-red-500' />
        )}

        {showTooltip && node.issues && node.issues.length > 0 && (
          <div
            className='fixed z-[99999] w-80 rounded-md border bg-background p-3 shadow-lg'
            style={{
              top: position.top,
              left: position.left
            }}
          >
            {node.issues.map((issue, index) => (
              <div key={index} className='mb-3 last:mb-0'>
                <p className='font-semibold'>{issue.type}</p>

                <p className='text-xs text-muted-foreground'>
                  Severity: {issue.severity}
                </p>

                {issue.line && (
                  <p className='text-xs text-muted-foreground'>
                    Line: {issue.line}
                  </p>
                )}

                <p className='text-sm'>{issue.message}</p>
              </div>
            ))}
          </div>
        )}
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
