
import { useEffect, useRef, useState } from "react";
import "./app.css";

const API_BASE = "http://127.0.0.1:8000";
const SESSION_KEY = "agentos_session_id";
const PENDING_KEY = "agentos_pending_request";

function App() {
  const [sessionId, setSessionId] = useState(() => {
    const saved = localStorage.getItem(SESSION_KEY);
    return saved ? Number(saved) : null;
  });

  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [pending, setPending] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem(PENDING_KEY) || "null");
    } catch {
      return null;
    }
  });

  const sendingRef = useRef(false);

  useEffect(() => {
    if (!sessionId) return;

    const controller = new AbortController();

    fetch(`${API_BASE}/chat/sessions/${sessionId}/messages`, {
      signal: controller.signal,
    })
      .then(async (response) => {
        if (response.status === 404) {
          localStorage.removeItem(SESSION_KEY);
          setSessionId(null);
          return [];
        }

        if (!response.ok) {
          throw new Error(
            `History request failed (${response.status})`
          );
        }

        return response.json();
      })
      .then((history) => {
        if (!controller.signal.aborted && Array.isArray(history)) {
          setMessages(
            history.map((item) => ({
              role: item.role,
              content: item.content,
            }))
          );
        }
      })
      .catch((err) => {
        if (err.name !== "AbortError") {
          console.error("History restoration failed:", err);
        }
      });

    return () => controller.abort();
  }, [sessionId]);

  const saveSession = (id) => {
    setSessionId(id);
    localStorage.setItem(SESSION_KEY, String(id));
  };

  const clearPending = () => {
    setPending(null);
    localStorage.removeItem(PENDING_KEY);
  };

  const submitRequest = async (payload, isRetry = false) => {
    if (sendingRef.current) return;

    sendingRef.current = true;
    setLoading(true);
    setError("");

    if (!isRetry) {
      setMessages((prev) => [
        ...prev,
        { role: "user", content: payload.message },
      ]);
    }

    setPending(payload);
    localStorage.setItem(PENDING_KEY, JSON.stringify(payload));

    try {
      const response = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        const detail =
          typeof data.detail === "string"
            ? data.detail
            : `AgentOS request failed (${response.status})`;

        throw new Error(detail);
      }

      saveSession(data.session_id);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.response,
        },
      ]);

      clearPending();
    } catch (err) {
      console.error("AgentOS request error:", err);

      setError(
        err.message || "Could not connect to AgentOS."
      );
    } finally {
      sendingRef.current = false;
      setLoading(false);
    }
  };

  const sendMessage = () => {
    const userText = message.trim();

    if (!userText || loading || pending) return;

    const payload = {
      message: userText,
      session_id: sessionId,
      request_id: crypto.randomUUID(),
    };

    setMessage("");
    submitRequest(payload);
  };

  const retryMessage = () => {
    if (!pending || loading) return;

    // Reuse the original request ID.
    submitRequest(pending, true);
  };

  const discardPending = () => {
    if (loading) return;

    clearPending();
    setError("");
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  const startNewChat = () => {
    if (loading) return;

    clearPending();
    localStorage.removeItem(SESSION_KEY);

    setSessionId(null);
    setMessages([]);
    setMessage("");
    setError("");
  };

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>AgentOS</h1>
          <p>AI Agent Assistant · Persistent chat memory</p>
        </div>

        <button
          className="new-chat"
          onClick={startNewChat}
          disabled={loading}
        >
          New chat
        </button>
      </header>

      <main className="chat-container">
        <div className="messages">
          {messages.length === 0 && (
            <div className="welcome">
              <h2>Welcome to AgentOS</h2>
              <p>
                Ask me anything. Your conversation history
                is saved in the AgentOS database.
              </p>
            </div>
          )}

          {messages.map((msg, index) => (
            <div
              key={`${index}-${msg.role}`}
              className={`message ${
                msg.role === "user"
                  ? "user-message"
                  : "ai-message"
              }`}
            >
              <div className="message-label">
                {msg.role === "user" ? "You" : "AgentOS"}
              </div>

              <div className="message-content">
                {msg.content}
              </div>
            </div>
          ))}

          {loading && (
            <div className="message ai-message">
              <div className="message-label">AgentOS</div>
              <div className="message-content">
                Thinking...
              </div>
            </div>
          )}
        </div>

        {error && (
          <div className="error-banner">
            {error}
          </div>
        )}

        {pending && !loading && (
          <div className="retry-area">
            <button onClick={retryMessage}>
              Retry request
            </button>

            <button onClick={discardPending}>
              Dismiss
            </button>
          </div>
        )}

        <div className="input-area">
          <input
            type="text"
            value={message}
            onChange={(event) =>
              setMessage(event.target.value)
            }
            onKeyDown={handleKeyDown}
            placeholder="Message AgentOS..."
            disabled={loading || Boolean(pending)}
          />

          <button
            onClick={sendMessage}
            disabled={
              loading ||
              Boolean(pending) ||
              !message.trim()
            }
          >
            {loading ? "Thinking…" : "Send"}
          </button>
        </div>
      </main>
    </div>
  );
}

export default App;
