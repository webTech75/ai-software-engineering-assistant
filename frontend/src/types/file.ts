export interface ProjectFile {
  name: string
  path: string
  type: 'file' | 'directory'
  children?: ProjectFile[]
}
