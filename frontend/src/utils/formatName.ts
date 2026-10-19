export function formatName (name?: string) {
  if (!name) return 'User'

  return name.charAt(0).toUpperCase() + name.slice(1).toLowerCase()
}
