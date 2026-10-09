import { useState, useRef, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";

import {
  sendChatMessageRequest,
  getChatHistoryRequest,
} from "@/api/requests";

import { Markdown } from "@/components/chat/Markdown";

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export function Project() {
  const { projectId } = useParams<{ projectId: string }>();

  const navigate = useNavigate();

  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const [loadingHistory, setLoadingHistory] = useState(true);
  const [error, setError] = useState("");

  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    loadChatHistory();
  }, [projectId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  async function loadChatHistory() {
    if (!projectId) {
      setLoadingHistory(false);
      return;
    }

    try {
      const history = await getChatHistoryRequest(
        Number(projectId)
      );

      setMessages(history);
    } catch (error) {
      console.error(error);
    } finally {
      setLoadingHistory(false);
    }
  }

  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    const text = message.trim();
    const id = Number(projectId);

    if (
      !text ||
      !projectId ||
      !Number.isInteger(id) ||
      id <= 0
    ) {
      setError(
        "Enter a message and open a valid project."
      );
      return;
    }

    setError("");
    setMessage("");

    setMessages((current) => [
      ...current,
      {
        role: "user",
        content: text,
      },
    ]);

    setLoading(true);

    try {
      const response =
        await sendChatMessageRequest(id, text);

      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content: response.answer,
        },
      ]);
    } catch {
      setError(
        "Unable to get a response. Please try again."
      );

      setMessage(text);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mx-auto w-full max-w-5xl space-y-8">

      <section>
        <button
          type="button"
          onClick={() => navigate("/")}
          className="mb-4 rounded-lg border bg-card px-4 py-2 transition-colors hover:bg-accent"
        >
          Back to Dashboard
        </button>

        <h1 className="text-3xl font-bold">
          Project Workspace
        </h1>

        <p className="mt-2 text-muted-foreground">
          Project ID: {projectId}
        </p>
      </section>

      <section className="rounded-xl border bg-background text-foreground p-6">

        <h2 className="text-xl font-semibold">
          AI Assistant
        </h2>

        <p className="mt-2 text-muted-foreground">
          Describe the software engineering task
          you need help with.
        </p>

        <div
          className="mt-6 h-[550px] overflow-y-auto space-y-4 rounded-xl border bg-card p-5 shadow-sm"
          aria-live="polite"
          aria-label="Chat conversation"
        >
          {loadingHistory ? (

            <p className="text-sm text-muted-foreground">
              Loading conversation...
            </p>

          ) : messages.length === 0 ? (

            <p className="text-sm text-muted-foreground">
              No messages yet. Ask your first
              question below.
            </p>

          ) : (

            messages.map((item, index) => (

              <div
                key={`${item.role}-${index}`}
                className={`rounded-xl p-4 ${
                  item.role === "user"
                    ? "chat-message chat-user"
                    : "mr-8 border bg-card text-card-foreground"
                }`}
              >
                <p className="mb-3 text-sm font-semibold">
                  {item.role === "user"
                    ? "You"
                    : "AI Assistant"}
                </p>

                <div  
                  className="markdown"
                  style={{ color: "var(--foreground)" }}
                >
                  <Markdown>
                    {item.content}
                  </Markdown>
                </div>
              </div>

            ))

          )}

          <div ref={messagesEndRef} />

          {loading && (
            <p className="text-sm text-muted-foreground">
              AI is thinking...
            </p>
          )}

        </div>

        {error && (
          <p
            role="alert"
            className="mt-4 text-sm text-destructive"
          >
            {error}
          </p>
        )}

        <form
          onSubmit={handleSubmit}
          className="mt-6 space-y-3"
        >

          <label
            htmlFor="chat-message"
            className="block text-sm font-medium"
          >
            Your message
          </label>

          <textarea
            id="chat-message"
            value={message}
            onChange={(event) =>
              setMessage(event.target.value)
            }
            placeholder="Example: Help me design a REST API using FastAPI..."
            rows={4}
            disabled={loading}
            className="w-full rounded-lg border bg-background p-3 text-foreground outline-none focus:ring-2 focus:ring-ring"
          />

          <button
            type="submit"
            disabled={loading || !message.trim()}
            className="rounded-lg bg-primary px-5 py-2 text-primary-foreground transition-colors hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading
              ? "Sending..."
              : "Send message"}
          </button>

        </form>

      </section>

    </div>
  );
}