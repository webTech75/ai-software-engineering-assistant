export interface FileIssue {
  type: string
  severity: string
  message: string
  line?: number
}

export interface FileTreeNode {
  name: string
  path: string
  type: 'file' | 'directory'
  children: FileTreeNode[]
  issues?: FileIssue[]
}


export function buildFileTree(
  files: string[],
  complexityFindings: any[] = []
): FileTreeNode[] {

  const root: FileTreeNode[] = []

  const fileIssues: Record<string, FileIssue[]> = {}

  complexityFindings.forEach((finding) => {
    if (!fileIssues[finding.file]) {
      fileIssues[finding.file] = []
    }

    fileIssues[finding.file].push({
      type: "complexity",
      severity: finding.complexity >= 10 ? "high" : "medium",
      message: `Function '${finding.function}' has complexity ${finding.complexity}`,
    })
  })


  for (const file of files) {

    const parts = file.split('/')

    let current = root
    let currentPath = ''

    parts.forEach((part, index) => {

      currentPath = currentPath
        ? `${currentPath}/${part}`
        : part


      let node = current.find(
        item => item.name === part
      )


      if (!node) {

        node = {
          name: part,
          path: currentPath,
          type: index === parts.length - 1
            ? 'file'
            : 'directory',
          children: []
        }


        if (
          index === parts.length - 1 &&
          fileIssues[currentPath]
        ) {
          node.issues = fileIssues[currentPath]
        }


        current.push(node)
      }


      current = node.children
    })
  }


  return root
}