
import { useEffect, useState } from "react";
import "./app.css";

const API_BASE = "http://127.0.0.1:8000";

function App() {
  const [sessionId, setSessionId] = useState(() => {
    const saved = localStorage.getItem("agentos_session_id");
    return saved ? Number(saved) : null;
  });

  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [activePage, setActivePage] = useState("chat");
  const [sidebarOpen, setSidebarOpen] = useState(true);

  useEffect(() => {
    if (!sessionId) return;

    const controller = new AbortController();

    fetch(`${API_BASE}/chat/sessions/${sessionId}/messages`, {
      signal: controller.signal,
    })
      .then(async (response) => {
        if (response.status === 404) {
          localStorage.removeItem("agentos_session_id");
          setSessionId(null);
          return [];
        }

        if (!response.ok) {
          throw new Error(`History request failed (${response.status})`);
        }

        return response.json();
      })
      .then((history) => {
        if (Array.isArray(history)) {
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
          console.error("Could not restore history:", err);
        }
      });

    return () => controller.abort();
  }, [sessionId]);

  const sendMessage = async () => {
    const userText = message.trim();

    if (!userText || loading) return;

    setMessages((previous) => [
      ...previous,
      { role: "user", content: userText },
    ]);

    setMessage("");
    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
        message: userText,
        session_id: sessionId,
        request_id: crypto.randomUUID(),
        }),
      });

      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(
          data.detail || `AgentOS request failed (${response.status})`
        );
      }

      setSessionId(data.session_id);

      localStorage.setItem(
        "agentos_session_id",
        String(data.session_id)
      );

      setMessages((previous) => [
        ...previous,
        { role: "assistant", content: data.response },
      ]);
    } catch (err) {
      console.error("AgentOS request error:", err);

      setError(err.message || "Could not connect to AgentOS.");

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: `Sorry, I couldn't complete that request. ${
            err.message || ""
          }`.trim(),
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  const startNewChat = () => {
    localStorage.removeItem("agentos_session_id");
    setSessionId(null);
    setMessages([]);
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
    <div
      className={`dashboard ${
        sidebarOpen ? "" : "sidebar-collapsed"
      }`}
    >
      <aside className="sidebar">
        <div className="brand-row">
          <div className="brand-mark">
            <span />
            <span />
            <span />
          </div>

          {sidebarOpen && (
            <div className="brand-copy">
              <strong>agentos</strong>
              <span>AGENT PLATFORM</span>
            </div>
          )}

          <button
            className="sidebar-toggle"
            onClick={() => setSidebarOpen(!sidebarOpen)}
            aria-label="Toggle sidebar"
          >
            {sidebarOpen ? "‹" : "›"}
          </button>
        </div>

        {sidebarOpen && (
          <p className="nav-caption">WORKSPACE</p>
        )}

        <nav className="navigation">
          {[
            { id: "overview", icon: "▦", label: "Overview" },
            { id: "chat", icon: "↗", label: "Agent workspace" },
            { id: "history", icon: "◷", label: "History" },
            { id: "memory", icon: "◇", label: "Memory" },
            { id: "tools", icon: "⌘", label: "Tools & integrations" },
          ].map((item) => (
            <button
              key={item.id}
              className={`nav-item ${
                activePage === item.id ? "active" : ""
              }`}
              onClick={() => setActivePage(item.id)}
              title={!sidebarOpen ? item.label : undefined}
            >
              <span className="nav-icon">{item.icon}</span>
              {sidebarOpen && <span>{item.label}</span>}
              {item.id === "chat" &&
                messages.length > 0 &&
                sidebarOpen && (
                  <span className="nav-indicator" />
                )}
            </button>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="connection-mark" />
          {sidebarOpen && (
            <div>
              <strong>Local environment</strong>
              <span>Development workspace</span>
            </div>
          )}
        </div>
      </aside>

      <main className="main-panel">
        <header className="topbar">
          <div className="breadcrumbs">
            <span>AgentOS</span>
            <span className="breadcrumb-divider">/</span>
            <strong>{pageTitles[activePage]}</strong>
          </div>

          <div className="topbar-actions">
            <span className="environment-label">
              <span className="environment-dot" />
              LOCAL
            </span>

            <button
              className="new-chat"
              onClick={startNewChat}
              disabled={loading}
            >
              <span>+</span> New task
            </button>
          </div>
        </header>

        {activePage === "chat" && (
          <section className="workspace">
            <div className="workspace-heading">
              <div>
               
                <h1>What are we working on?</h1>
                <p className="section-description">
                  Describe a task to begin a conversation with your agent.
                </p>
              </div>

              <div className="workspace-index">
                <span>SESSION</span>
                <strong>{sessionId ? `#${sessionId}` : "NEW"}</strong>
              </div>
            </div>

            <div className="task-area">
              <div className="task-area-top">
                <div className="task-symbol">↗</div>
                <div>
                  <strong>Task input</strong>
                  <p>Natural language · Agent interaction</p>
                </div>
              </div>

              <div className="messages">
                {messages.length === 0 ? (
                  <div className="empty-workspace">
                    <div className="empty-rule" />
                    <p className="empty-title">READY WHEN YOU ARE</p>
                    <p className="empty-description">
                      Start with a question or describe the outcome
                      you want to achieve.
                    </p>

                    <div className="prompt-list">
                      <button
                        onClick={() =>
                          choosePrompt(
                            "Help me break a complex project into smaller tasks."
                          )
                        }
                      >
                        <span className="prompt-number">01</span>
                        <span className="prompt-copy">
                          <strong>Break down a complex task</strong>
                          <small>Plan steps toward an outcome</small>
                        </span>
                        <span className="prompt-arrow">↗</span>
                      </button>

                      <button
                        onClick={() =>
                          choosePrompt(
                            "Help me research a topic and organize the findings."
                          )
                        }
                      >
                        <span className="prompt-number">02</span>
                        <span className="prompt-copy">
                          <strong>Research and organize</strong>
                          <small>Explore a topic and structure findings</small>
                        </span>
                        <span className="prompt-arrow">↗</span>
                      </button>

                      <button
                        onClick={() =>
                          choosePrompt(
                            "Explain how AI agents can use tools to complete tasks."
                          )
                        }
                      >
                        <span className="prompt-number">03</span>
                        <span className="prompt-copy">
                          <strong>Explore agent capabilities</strong>
                          <small>Learn about agents and tool usage</small>
                        </span>
                        <span className="prompt-arrow">↗</span>
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="conversation">
                    {messages.map((msg, index) => (
                      <article
                        key={`${index}-${msg.role}`}
                        className={`message ${
                          msg.role === "user"
                            ? "user-message"
                            : "ai-message"
                        }`}
                      >
                        <div className="message-label">
                          <span className="message-avatar">
                            {msg.role === "user" ? "U" : "A"}
                          </span>
                          <strong>
                            {msg.role === "user" ? "You" : "AgentOS"}
                          </strong>
                          <span className="message-role">
                            {msg.role === "user"
                              ? "REQUEST"
                              : "RESPONSE"}
                          </span>
                        </div>

                        <div className="message-content">
                          {msg.content}
                        </div>
                      </article>
                    ))}

                    {loading && (
                      <div className="loading-line">
                        <span className="loading-dot" />
                        AgentOS is processing your request...
                      </div>
                    )}
                  </div>
                )}
              </div>

              {error && (
                <div className="error-banner">
                  <strong>Request failed</strong>
                  <span>{error}</span>
                </div>
              )}

              <div className="input-area">
                <input
                  type="text"
                  value={message}
                  onChange={(event) => setMessage(event.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Describe a task or ask a question..."
                  disabled={loading}
                  aria-label="Describe a task"
                />

                <button
                  onClick={sendMessage}
                  disabled={loading || !message.trim()}
                  aria-label="Send request"
                >
                  {loading ? "Working..." : "Run request ↗"}
                </button>
              </div>

              
            </div>

          
          </section>
        )}

        {activePage === "overview" && (
          <section className="secondary-page">
            <p className="section-kicker">WORKSPACE / OVERVIEW</p>
            <h1>Agent workspace overview</h1>
            <p className="section-description">
              A starting point for monitoring tasks, sessions, and agent activity.
            </p>

            <div className="overview-grid">
              <article className="overview-card">
                <span>ACTIVE SESSION</span>
                <strong>{sessionId ? `#${sessionId}` : "—"}</strong>
                <small>{sessionId ? "Local session ID" : "No active session"}</small>
              </article>
              <article className="overview-card">
                <span>MESSAGES</span>
                <strong>{messages.length}</strong>
                <small>Current conversation</small>
              </article>
              <article className="overview-card">
                <span>REQUEST STATUS</span>
                <strong>{loading ? "Running" : "Idle"}</strong>
                <small>Current browser state</small>
              </article>
            </div>

            <button
              className="primary-action"
              onClick={() => setActivePage("chat")}
            >
              Open agent workspace ↗
            </button>
          </section>
        )}

        {activePage === "history" && (
          <section className="secondary-page">
            <p className="section-kicker">WORKSPACE / HISTORY</p>
            <h1>Conversation history</h1>
            <p className="section-description">
              Review the current conversation restored from the saved session.
              A multi-session history view needs a backend endpoint.
            </p>

            {messages.length > 0 ? (
              <div className="history-list">
                {messages.map((item, index) => (
                  <article className="history-row" key={index}>
                    <span>{String(index + 1).padStart(2, "0")}</span>
                    <div>
                      <strong>
                        {item.role === "user" ? "Your request" : "Agent response"}
                      </strong>
                      <p>{item.content}</p>
                    </div>
                  </article>
                ))}
              </div>
            ) : (
              <div className="empty-secondary">
                <span>◷</span>
                <strong>No conversation loaded</strong>
                <p>Start a conversation to see its messages here.</p>
              </div>
            )}

            <button
              className="primary-action"
              onClick={() => setActivePage("chat")}
            >
              Return to workspace ↗
            </button>
          </section>
        )}

        {activePage === "memory" && (
          <section className="secondary-page">
            <p className="section-kicker">WORKSPACE / MEMORY</p>
            <h1>Persistent memory</h1>
            <p className="section-description">
              This page is a UI placeholder until the backend's memory
              retrieval and management endpoints are confirmed.
            </p>

            <div className="notice-panel">
              <span>◇</span>
              <div>
                <strong>Memory integration pending</strong>
                <p>
                  Connect this screen to the existing memory API before
                  displaying or modifying saved memories.
                </p>
              </div>
            </div>
          </section>
        )}

        {activePage === "tools" && (
          <section className="secondary-page">
            <p className="section-kicker">WORKSPACE / INTEGRATIONS</p>
            <h1>Tools & integrations</h1>
            <p className="section-description">
              An interface for future tool integrations. No plugin execution
              is claimed until the backend exposes the relevant tools.
            </p>

            <div className="notice-panel">
              <span>⌘</span>
              <div>
                <strong>Integration registry not connected</strong>
                <p>
                  Available plugins, permissions, and connection states
                  need to come from a real backend registry.
                </p>
              </div>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
