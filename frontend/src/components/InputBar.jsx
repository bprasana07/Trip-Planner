import { useState, useRef, useEffect } from 'react'

const SUGGESTIONS = [
  '5 days in Tokyo, Japan — mid-range, love food & culture',
  'Weekend trip to Paris, France — luxury, art lover',
  'Budget trip to Lisbon, Portugal for 7 days',
  '10 days in New Zealand — adventure seeker',
]

export default function InputBar({ onSend, disabled }) {
  const [text, setText] = useState('')
  const [showHints, setShowHints] = useState(false)
  const textareaRef = useRef(null)

  useEffect(() => {
    if (!disabled) textareaRef.current?.focus()
  }, [disabled])

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      submit()
    }
  }

  function submit() {
    const trimmed = text.trim()
    if (!trimmed || disabled) return
    onSend(trimmed)
    setText('')
    setShowHints(false)
  }

  function useSuggestion(s) {
    setText(s)
    setShowHints(false)
    textareaRef.current?.focus()
  }

  return (
    <div className="input-area">
      {showHints && (
        <div className="suggestions">
          {SUGGESTIONS.map(s => (
            <button key={s} className="suggestion-chip" onClick={() => useSuggestion(s)}>
              ✈️ {s}
            </button>
          ))}
        </div>
      )}
      <div className="input-bar">
        <button
          className={`hint-btn ${showHints ? 'active' : ''}`}
          onClick={() => setShowHints(o => !o)}
          title="Show example prompts"
          disabled={disabled}
        >
          💡
        </button>
        <textarea
          ref={textareaRef}
          className="input-textarea"
          rows={1}
          placeholder="Where would you like to go? Press Enter to send…"
          value={text}
          onChange={e => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={disabled}
        />
        <button
          className="send-btn"
          onClick={submit}
          disabled={disabled || !text.trim()}
          aria-label="Send"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
            <line x1="22" y1="2" x2="11" y2="13" />
            <polygon points="22 2 15 22 11 13 2 9 22 2" />
          </svg>
        </button>
      </div>
    </div>
  )
}
