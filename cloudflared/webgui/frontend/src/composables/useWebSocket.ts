import { ref, onUnmounted } from 'vue'
import { wsUrl } from '@/api'

export function useWebSocket(path: string) {
  const messages = ref<string[]>([])
  const connected = ref(false)
  const error = ref<string | null>(null)
  let ws: WebSocket | null = null
  let reconnectTimer: ReturnType<typeof setTimeout> | null = null
  let disposed = false
  const MAX_LINES = 2000

  function connect() {
    if (disposed) return
    // Resolved relative to the current document so the WebSocket stays
    // inside the Home Assistant Ingress path prefix.
    ws = new WebSocket(wsUrl(path))

    ws.onopen = () => {
      connected.value = true
      error.value = null
      // The server replays its buffer on connect — start from a clean slate
      // to avoid duplicated lines after a reconnect.
      messages.value = []
    }

    ws.onmessage = (event) => {
      messages.value.push(event.data)
      if (messages.value.length > MAX_LINES) {
        messages.value = messages.value.slice(-MAX_LINES)
      }
    }

    ws.onerror = () => {
      error.value = 'WebSocket connection error'
    }

    ws.onclose = () => {
      connected.value = false
      if (!disposed) {
        reconnectTimer = setTimeout(connect, 3000)
      }
    }
  }

  function disconnect() {
    disposed = true
    if (reconnectTimer) {
      clearTimeout(reconnectTimer)
      reconnectTimer = null
    }
    if (ws) {
      ws.close()
      ws = null
    }
  }

  function clear() {
    messages.value = []
  }

  onUnmounted(disconnect)

  return { messages, connected, error, connect, disconnect, clear }
}
