import { useEffect, useRef } from 'react'
import Message from './Message'
import InputBar from './InputBar'

export default function ChatWindow({ messages, loading, onSend }) {
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  return (
    <div className="chat-window">
      <div className="messages-area">
        {messages.map(msg => (
          <Message key={msg.id} message={msg} />
        ))}
        {loading && <TypingIndicator />}
        <div ref={bottomRef} />
      </div>
      <InputBar onSend={onSend} disabled={loading} />
    </div>
  )
}

function TypingIndicator() {
  return (
    <div className="message-row assistant">
      <div className="avatar">🤖</div>
      <div className="bubble typing-bubble">
        <span className="dot" />
        <span className="dot" />
        <span className="dot" />
      </div>
    </div>
  )
}
