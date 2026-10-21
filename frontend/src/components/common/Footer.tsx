import { GitBranch, BookOpen, Sparkles } from 'lucide-react'

export function Footer () {
  return (
    <footer className='w-full mt-5 border-t border-slate-700/70 bg-slate-900/85 text-white backdrop-blur'>
      <div className='mx-auto max-w-7xl px-6 py-8'>
        <div className='grid gap-8 md:grid-cols-4'>
          {/* Brand */}
          <div className='space-y-3'>
            <div className='flex items-center gap-2'>
              <Sparkles className='h-5 w-5' />

              <span className='font-semibold'>Neura</span>
            </div>

            <p className='text-sm text-white/60'>
              AI Software Engineering Assistant for analyzing, understanding,
              and improving software projects.
            </p>
          </div>

          {/* Product */}
          <div>
            <h3 className='mb-3 text-sm font-semibold'>Product</h3>

            <ul className='space-y-2 text-sm text-white/60'>
              <li>Project Analysis</li>
              <li>AI Code Review</li>
              <li>Security Insights</li>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h3 className='mb-3 text-sm font-semibold'>Resources</h3>

            <ul className='space-y-2 text-sm text-white/60'>
              <li>
                <a
                  href='https://github.com/webTech75/ai-software-engineering-assistant'
                  target='_blank'
                  rel='noopener noreferrer'
                  className='flex items-center gap-2 hover:text-white transition'
                >
                  <GitBranch className='h-4 w-4' />
                  GitHub
                </a>
              </li>

              <li className='flex items-center gap-2'>
                <BookOpen className='h-4 w-4' />
                Documentation
              </li>

              <li>Changelog</li>
            </ul>
          </div>

          {/* Developer */}
          <div>
            <h3 className='mb-3 text-sm font-semibold'>Developer</h3>

            <ul className='space-y-2 text-sm text-white/60'>
              <li>
                <a
                  href='https://webtech75.github.io/amr-elhabbal/'
                  target='_blank'
                  rel='noopener noreferrer'
                  className='hover:text-white transition'
                >
                  Amr Elhabbal
                </a>
              </li>

              <li>
                <a
                  href='https://github.com/webTech75'
                  target='_blank'
                  rel='noopener noreferrer'
                  className='hover:text-white transition'
                >
                  GitHub Profile
                </a>
              </li>

              <li>
                <a
                  href='https://linkedin.com/in/amr-elhabbal'
                  target='_blank'
                  rel='noopener noreferrer'
                  className='hover:text-white transition'
                >
                  LinkedIn
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Copyright */}
        <div className='mt-6 border-t border-white/10 pt-4 text-center justify-center text-sm text-white/60'>
          <img src='/neura_icon.png' alt='Neura' className='h-5 w-5 rounded' />
          <p>
            © {new Date().getFullYear()} Neura • AI Software Engineering
            Assistant • v1.0.0
          </p>

          <p className='mt-1'>Built by Amr Elhabbal</p>
        </div>
      </div>
    </footer>
  )
}
