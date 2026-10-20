import { useState } from 'react'
import { Moon, Sun } from 'lucide-react'

import { getTheme, setTheme, themes } from '@/utils/theme'

export function ThemeSwitcher () {
  const [theme, setCurrentTheme] = useState(getTheme())
  const [open, setOpen] = useState(false)

  function handleChange (value: string) {
    setCurrentTheme(value)
    setTheme(value)
    setOpen(false)
  }

  const currentTheme = themes.find(item => item.id === theme)

  return (
    <div className='relative'>
      <button
        type='button'
        onClick={() => setOpen(!open)}
        className='rounded-lg p-2 transition-colors hover:bg-accent'
        title='Change theme'
      >
        {theme === 'dark' ? (
          <Moon className='h-5 w-5' />
        ) : (
          <Sun className='h-5 w-5' />
        )}
      </button>

      {open && (
        <div className='absolute right-0 z-50 mt-2 w-40 rounded-lg border bg-card p-2 shadow-lg'>
          <p className='px-2 py-1 text-xs text-muted-foreground'>Theme</p>

          {themes.map(item => (
            <button
              key={item.id}
              type='button'
              onClick={() => handleChange(item.id)}
              className='flex w-full items-center justify-between rounded-md px-2 py-2 text-sm hover:bg-accent'
            >
              <span>{item.label}</span>

              {currentTheme?.id === item.id && <span>✓</span>}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
