export interface FileTreeNode {
  name: string
  path: string
  type: 'file' | 'directory'
  children: FileTreeNode[]
}

export function buildFileTree (files: string[]): FileTreeNode[] {
  const root: FileTreeNode[] = []

  for (const file of files) {
    const parts = file.split('/')

    let current = root
    let currentPath = ''

    parts.forEach((part, index) => {
      currentPath = currentPath ? `${currentPath}/${part}` : part

      let node = current.find(item => item.name === part)

      if (!node) {
        node = {
          name: part,
          path: currentPath,
          type: index === parts.length - 1 ? 'file' : 'directory',
          children: []
        }

        current.push(node)
      }

      current = node.children
    })
  }

  return root
}
