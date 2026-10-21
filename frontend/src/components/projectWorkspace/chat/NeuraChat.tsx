import { Markdown } from './Markdown'
import { formatName } from '@/utils/formatName'

import type { ChatMessage } from '@/types/chat'

interface NeuraChatProps {
  messages: ChatMessage[]
  message: string
  loading: boolean
  loadingHistory: boolean

  username?: string

  setMessage: (value: string) => void
  handleSubmit: (event: FormEvent) => void

  messagesEndRef: React.RefObject<HTMLDivElement | null>
}

export function NeuraChat ({
  messages,
  message,
  loading,
  loadingHistory,
  username,
  setMessage,
  handleSubmit,
  messagesEndRef
}: NeuraChatProps) {
  return (
    <section className='rounded-xl border bg-background p-6'>
      <div className='flex items-center gap-3'>
        <img
          src='/neura_icon.png'
          alt='Neura'
          className='h-12 w-12 rounded-xl'
        />

        <div>
          <h2 className='text-xl font-semibold'>Neura</h2>

          <p className='text-sm text-muted-foreground'>
            Your AI Software Engineering Assistant
          </p>
        </div>
      </div>

      <div
        className='mt-6 h-[550px] overflow-y-auto space-y-4 rounded-xl border bg-card p-5 shadow-sm'
        aria-live='polite'
        aria-label='Chat conversation'
      >
        {loadingHistory ? (
          <p className='text-sm text-muted-foreground'>
            Loading conversation...
          </p>
        ) : messages.length === 0 ? (
          <p className='text-sm text-muted-foreground'>
            No messages yet. Ask your first question below.
          </p>
        ) : (
          messages.map((item, index) => (
            <div
              key={`${item.role}-${index}`}
              className={`rounded-xl p-4 ${
                item.role === 'user'
                  ? 'chat-message chat-user'
                  : 'mr-8 border bg-card text-card-foreground'
              }`}
            >
              <p className='mb-3 text-sm font-semibold'>
                {item.role === 'user' ? (
                  formatName(username) || 'User'
                ) : (
                  <>
                    <img
                      src='/neura_icon.png'
                      alt='Neura'
                      className='h-4 w-4 rounded'
                    />
                    <span>Neura</span>
                  </>
                )}
              </p>

              <div
                className='markdown'
                style={{
                  color: 'var(--foreground)'
                }}
              >
                <Markdown>{item.content}</Markdown>
              </div>
            </div>
          ))
        )}

        <div ref={messagesEndRef} />

        {loading && (
          <p className='text-sm text-muted-foreground'>Neura is thinking...</p>
        )}
      </div>

      <form onSubmit={handleSubmit} className='mt-6 space-y-3'>
        <label htmlFor='chat-message' className='block text-sm font-medium'>
          Your message
        </label>

        <input
          id='chat-message'
          value={message}
          onChange={event => setMessage(event.target.value)}
          placeholder='Example: Help me design a REST API using FastAPI...'
          disabled={loading}
          className='w-full rounded-lg border bg-background p-3 text-foreground outline-none focus:ring-2 focus:ring-ring'
        />

        <button
          type='submit'
          disabled={loading || !message.trim()}
          className='rounded-lg bg-primary px-5 py-2 text-primary-foreground transition-colors hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50'
        >
          {loading ? 'Sending...' : 'Send message'}
        </button>
      </form>
    </section>
  )
}
