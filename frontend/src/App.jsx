import { useState, useRef, useEffect, useCallback } from 'react'
import ChatWindow from './components/ChatWindow'
import Sidebar from './components/Sidebar'
import './App.css'

const WELCOME = {
  id: 'welcome',
  role: 'assistant',
  text: "Hi! I'm **TripBot**, your personal AI travel advisor.\n\nTell me where you'd like to go and I'll check the weather, find attractions, and suggest accommodation — all in one go!\n\nTry something like:\n> *\"Plan a trip to Barcelona, Spain. Dates: 20th July 2025. Duration: 5 days. Mid-range budget, love art and food.\"*",
  timestamp: new Date(),
}

const WS_BASE = 'ws://localhost:4173/api/v1/ws/chat'
const CONFIG_URL = '/nsapi/api/v1/set_ns_config'

export default function App() {
  const [messages, setMessages] = useState([WELCOME])
  const [loading, setLoading] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [connected, setConnected] = useState(false)

  const sessionId = useRef(crypto.randomUUID())
  const wsRef = useRef(null)
  const pendingRef = useRef(false)

  // Initialize nsflow config + open WebSocket on mount
  useEffect(() => {
    initSession()
    return () => wsRef.current?.close()
  }, [])

  async function initSession() {
    // 1. Tell nsflow where the Neuro SAN server is
    try {
      await fetch(CONFIG_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          NEURO_SAN_CONNECTION_TYPE: 'http',
          NEURO_SAN_SERVER_HOST: 'localhost',
          NEURO_SAN_SERVER_PORT: 8080,
        }),
      })
    } catch {
      // server may already have config — continue anyway
    }

    // 2. Open WebSocket for this session
    openWebSocket()
  }

  const openWebSocket = useCallback(() => {
    const url = `${WS_BASE}/trip_advisor/${sessionId.current}`
    const ws = new WebSocket(url)

    ws.onopen = () => setConnected(true)

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        const msg = data?.message

        // Skip non-AI messages (progress, internal logs, etc.)
        if (!msg) return
        if (typeof msg === 'object' && msg.type !== 'AI') return

        const text = typeof msg === 'string' ? msg : msg.text ?? JSON.stringify(msg)
        if (!text?.trim()) return

        setMessages(prev => [
          ...prev,
          { id: crypto.randomUUID(), role: 'assistant', text, timestamp: new Date() },
        ])
        setLoading(false)
        pendingRef.current = false
      } catch {
        // ignore parse errors on non-JSON frames
      }
    }

    ws.onerror = () => {
      setConnected(false)
      setLoading(false)
      pendingRef.current = false
      setMessages(prev => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: 'error',
          text: '**WebSocket error.** Make sure Neuro SAN Studio is running (`python -m run`).',
          timestamp: new Date(),
        },
      ])
    }

    ws.onclose = () => setConnected(false)

    wsRef.current = ws
  }, [])

  function sendMessage(text) {
    if (!text.trim() || loading) return

    setMessages(prev => [
      ...prev,
      { id: crypto.randomUUID(), role: 'user', text, timestamp: new Date() },
    ])
    setLoading(true)
    pendingRef.current = true

    const ws = wsRef.current
    if (!ws || ws.readyState !== WebSocket.OPEN) {
      setMessages(prev => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: 'error',
          text: '**Not connected.** Please refresh the page and ensure Neuro SAN Studio is running.',
          timestamp: new Date(),
        },
      ])
      setLoading(false)
      return
    }

    ws.send(JSON.stringify({ message: text }))
  }

  function clearChat() {
    wsRef.current?.close()
    sessionId.current = crypto.randomUUID()
    setMessages([WELCOME])
    setLoading(false)
    setConnected(false)
    setTimeout(openWebSocket, 100)
  }

  return (
    <div className="app-root">
      <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} onClear={clearChat} />
      <div className="main-panel">
        <header className="app-header">
          <button className="hamburger" onClick={() => setSidebarOpen(o => !o)} aria-label="Toggle sidebar">
            <span /><span /><span />
          </button>
          <div className="brand">
            <span className="brand-emoji">✈️</span>
            <div>
              <div className="brand-name">TripBot</div>
              <div className="brand-sub">AI Travel Advisor</div>
            </div>
          </div>
          <div className="status-pill" data-active={loading}>
            <span className="status-dot" />
            {loading ? 'Thinking…' : connected ? 'Ready' : 'Connecting…'}
          </div>
        </header>
        <ChatWindow messages={messages} loading={loading} onSend={sendMessage} />
      </div>
    </div>
  )
}
