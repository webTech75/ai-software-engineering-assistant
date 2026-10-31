import { motion } from 'framer-motion'

const steps = [
  'Scanning repository',
  'Understanding architecture',
  'Analyzing code quality',
  'Checking security',
  'Generating recommendations'
]

export function AIShowcase() {
  return (
    <div className='relative mx-auto mt-8 w-full max-w-3xl'>
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className='
        mt-2
        rounded-3xl
        border
        border-border
        bg-card/60
        p-5
        shadow-2xl
        backdrop-blur-xl
        sm:p-8
        '
      >
        <div className='mb-0'>
          <p className='text-sm font-medium text-primary'>
            AI SOFTWARE ANALYSIS
          </p>
          <h3 className='mt-1 text-xl font-semibold'>
            Understanding your codebase...
          </h3>
        </div>

        <div className='space-y-3'>
          {steps.map((step, index) => (
            <motion.div
              key={step}
              initial={{ opacity: 0, x: -15 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{
                delay: 1 + index * 1,
                duration: 0.8,
                ease: 'easeOut'
              }}
              className='
                flex
                items-center
                gap-3
                rounded-xl
                border
                border-border
                bg-background/40
                px-4
                py-3
                '
            >
              <motion.span
                initial={{ scale: 0, rotate: -180 }}
                animate={{ scale: 1, rotate: 0 }}
                transition={{
                  delay: 1.8 + index * 1,
                  duration: 0.8,
                  ease: 'backOut'
                }}
                className='text-primary'
              >
                ✓
              </motion.span>

              <span className='text-sm'>{step}</span>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  )
}
