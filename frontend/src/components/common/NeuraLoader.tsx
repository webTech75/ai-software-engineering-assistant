import { motion } from 'framer-motion'

interface NeuraLoaderProps {
  show?: boolean
  text?: string
}

export default function NeuraLoader ({
  show = true,
  text = 'Processing...'
}: NeuraLoaderProps) {
  if (!show) return null

  return (
    <div className='fixed inset-0 z-[9999] flex items-center justify-center bg-background/80 backdrop-blur-sm'>
      <div className='flex flex-col items-center gap-5'>
        <div className='relative overflow-hidden rounded-xl px-10 py-5'>
          {/* AI glow */}
          <motion.div
            className='absolute inset-0 bg-blue-500/20 blur-3xl'
            animate={{
              opacity: [0.3, 0.9, 0.3],
              scale: [0.9, 1.15, 0.9]
            }}
            transition={{
              duration: 2.5,
              repeat: Infinity,
              ease: 'easeInOut'
            }}
          />

          {/* Neura Logo */}
          <motion.h1
            className='relative text-5xl font-bold tracking-[0.45em] text-blue-500'
            animate={{
              opacity: [0.6, 1, 0.6]
            }}
            transition={{
              duration: 2,
              repeat: Infinity
            }}
          >
            NEURA
          </motion.h1>

          {/* Scanning beam */}
          <motion.div
            className='absolute left-0 top-1/2 h-[2px] w-full bg-blue-400 shadow-lg shadow-blue-500'
            animate={{
              x: ['-100%', '100%']
            }}
            transition={{
              duration: 1.8,
              repeat: Infinity,
              ease: 'linear'
            }}
          />
        </div>

        {/* Status text */}
        <motion.p
          className='text-sm text-muted-foreground'
          animate={{
            opacity: [0.4, 1, 0.4]
          }}
          transition={{
            duration: 1.5,
            repeat: Infinity
          }}
        >
          {text}
        </motion.p>
      </div>
    </div>
  )
}
