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
    languages: string[]
    frameworks: string[]
    database: string | null
    orms: string[]
    migration_tools: string[]
    package_manager: string | null
    build_tools: string[]
    testing_tools: string[]
    styling_tools: string[]
  }

  structure: {
    files: string[]
  }
}