export interface ProjectScan {
  statistics: {
    total_files: number
    total_directories: number
    extensions: Record<string, number>
    total_size: number
    average_file_size: number
    largest_file: string | null
    largest_file_size: number
  }

  technology: {
    language: string | null
    framework: string | null
    database: string | null
    orm: string | null
    migration_tool: string | null
  }

  structure: {
    files: string[]
  }
}
