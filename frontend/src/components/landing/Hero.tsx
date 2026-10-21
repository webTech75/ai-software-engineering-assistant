import { motion } from 'framer-motion'
import { AIShowcase } from './AIShowcase'

export function Hero () {
  return (
    <section className='relative flex min-h-screen items-center justify-center overflow-hidden px-6'>
      {/* Background glow */}
      <div className='absolute inset-0 -z-10'>
        <div className='absolute left-1/2 top-1/2 h-[500px] w-[500px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-primary/20 blur-[120px]' />
      </div>

      <div className='mx-auto max-w-5xl text-center'>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className='mb-2 flex justify-center'
        >
          <img
            src='/neura_icon.png'
            alt='Neura'
            className='h-24 w-24 rounded-2xl shadow-lg'
          />
        </motion.div>
        <motion.h1
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className='text-4xl font-bold tracking-tight md:text-6xl'
        >
          Neura
          <br />
          Your AI Software Engineering Assistant
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.8 }}
          className='mx-auto mt-2 max-w-2xl text-lg text-muted-foreground md:text-xl'
        >
          Analyze your codebase, understand software architecture, detect
          issues, and improve your projects with intelligent AI assistance.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: 0.8 }}
          className='mt-10'
        ></motion.div>

        {/* Future AI visualization */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.6, duration: 0.8 }}
        >
          <AIShowcase />
        </motion.div>
      </div>
    </section>
  )
}
