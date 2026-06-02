import { useMemo } from 'react'

// Minimal markdown renderer: bold, italic, blockquote, inline code, line breaks
function renderMarkdown(text) {
  const lines = text.split('\n')
  const elements = []
  let i = 0

  while (i < lines.length) {
    const line = lines[i]

    if (line.startsWith('> ')) {
      elements.push(
        <blockquote key={i} className="md-quote">
          {inlineRender(line.slice(2))}
        </blockquote>
      )
    } else if (line === '') {
      elements.push(<div key={i} className="md-spacer" />)
    } else {
      elements.push(<p key={i}>{inlineRender(line)}</p>)
    }
    i++
  }
  return elements
}

function inlineRender(text) {
  // Handle **bold**, *italic*, `code`
  const parts = []
  const regex = /(\*\*(.+?)\*\*|\*(.+?)\*|`(.+?)`)/g
  let last = 0
  let m

  while ((m = regex.exec(text)) !== null) {
    if (m.index > last) parts.push(text.slice(last, m.index))
    if (m[2]) parts.push(<strong key={m.index}>{m[2]}</strong>)
    else if (m[3]) parts.push(<em key={m.index}>{m[3]}</em>)
    else if (m[4]) parts.push(<code key={m.index} className="md-code">{m[4]}</code>)
    last = m.index + m[0].length
  }
  if (last < text.length) parts.push(text.slice(last))
  return parts
}

export default function Message({ message }) {
  const { role, text, timestamp } = message
  const isUser = role === 'user'
  const isError = role === 'error'

  const timeStr = useMemo(() =>
    timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    [timestamp]
  )

  return (
    <div className={`message-row ${isUser ? 'user' : 'assistant'} ${isError ? 'error' : ''}`}>
      {!isUser && <div className="avatar">{isError ? '⚠️' : '🤖'}</div>}
      <div className="bubble-wrap">
        <div className="bubble">
          {renderMarkdown(text)}
        </div>
        <div className="msg-time">{timeStr}</div>
      </div>
      {isUser && <div className="avatar user-avatar">👤</div>}
    </div>
  )
}
