import { useEffect, useState } from "react";
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
        if (!response.ok) throw new Error(`History request failed (${response.status})`);
        return response.json();
      })
      .then((history) => {
        if (Array.isArray(history)) {
          setMessages(history.map((item) => ({
            role: item.role,
            content: item.content,
          })));
        }
      })
      .catch((err) => {
        if (err.name !== "AbortError") console.error("Could not restore history:", err);
      });

    return () => controller.abort();
  }, [sessionId]);

  const sendMessage = async () => {
    const userText = message.trim();
    if (!userText || loading) return;

    setMessages((prev) => [...prev, { role: "user", content: userText }]);
    setMessage("");
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
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userText, session_id: sessionId }),
      });

      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(data.detail || `AgentOS request failed (${response.status})`);
      }

      setSessionId(data.session_id);
      localStorage.setItem("agentos_session_id", String(data.session_id));
      setMessages((prev) => [...prev, { role: "assistant", content: data.response }]);
    } catch (err) {
      console.error("AgentOS request error:", err);
      setError(err.message || "Could not connect to AgentOS.");
      setMessages((prev) => [...prev, {
        role: "assistant",
        content: `Sorry, I couldn't complete that request. ${err.message || ""}`.trim(),
      }]);
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
    setMessage("");
    setActivePage("chat");
  };

  const choosePrompt = (prompt) => {
    setActivePage("chat");
    setMessage(prompt);
  };

  const pageTitles = {
    overview: "Overview",
    chat: "Agent workspace",
    history: "Conversation history",
    memory: "Persistent memory",
    tools: "Tools & integrations",
  };

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>AgentOS</h1>
          <p>AI Agent Assistant · Persistent chat memory</p>
        </div>
        <button className="new-chat" onClick={startNewChat} disabled={loading}>New chat</button>
      </header>
      <main className="chat-container">
        <div className="messages">
          {messages.length === 0 && (
            <div className="welcome">
              <h2>Welcome to AgentOS</h2>
              <p>Ask me anything. Your chat history is saved in AgentOS database.</p>
            </div>
          )}
          {messages.map((msg, index) => (
            <div key={`${index}-${msg.role}`} className={`message ${msg.role === "user" ? "user-message" : "ai-message"}`}>
              <div className="message-label">{msg.role === "user" ? "You" : "AgentOS"}</div>
              <div className="message-content">{msg.content}</div>
            </div>
          ))}
          {loading && (
            <div className="message ai-message">
              <div className="message-label">AgentOS</div>
              <div className="message-content">Thinking...</div>
            </div>
          )}
        </div>
        {error && <div className="error-banner">{error}</div>}
        <div className="input-area">
          <input
            type="text"
            value={message}
            onChange={(event) => setMessage(event.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Message AgentOS..."
            disabled={loading}
          />
          <button onClick={sendMessage} disabled={loading || !message.trim()}>
            {loading ? "Thinking…" : "Send"}
          </button>
        </div>
      </main>
    </div>
  );
}

export default App;
