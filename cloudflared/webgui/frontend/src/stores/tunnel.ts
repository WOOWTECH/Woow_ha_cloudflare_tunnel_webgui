import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { api } from '@/api'
import type { HealthStatus } from '@/types'

/**
 * Health / tunnel status store.
 *
 * Also tracks the "restarting" window: after a restart is requested the
 * add-on (including this GUI backend) goes down briefly. We keep polling;
 * once the backend answers again after having been unreachable, the restart
 * is considered complete.
 */
export const useTunnelStore = defineStore('tunnel', () => {
  const health = ref<HealthStatus | null>(null)
  const restarting = ref(false)
  const error = ref<string | null>(null)
  let pollInterval: ReturnType<typeof setInterval> | null = null
  let sawDown = false

  const tunnelStatus = computed(() => health.value?.tunnel.status ?? 'unknown')

  async function fetchHealth() {
    try {
      health.value = await api<HealthStatus>('api/health')
      error.value = null
      if (restarting.value && sawDown) {
        restarting.value = false
        sawDown = false
      }
    } catch (e: unknown) {
      if (restarting.value) {
        sawDown = true
      } else {
        error.value = e instanceof Error ? e.message : String(e)
      }
      health.value = null
    }
  }

  async function restartAddon() {
    error.value = null
    try {
      await api<{ result: string }>('api/restart', { method: 'POST' })
    } catch {
      // The backend may die mid-request while restarting — that's expected.
    }
    restarting.value = true
    sawDown = false
  }

  /** Mark a restart initiated elsewhere (e.g. Save & Restart on Config). */
  function markRestarting() {
    restarting.value = true
    sawDown = false
  }

  function startPolling(intervalMs = 4000) {
    stopPolling()
    fetchHealth()
    pollInterval = setInterval(fetchHealth, intervalMs)
  }

  function stopPolling() {
    if (pollInterval) {
      clearInterval(pollInterval)
      pollInterval = null
    }
  }

  return {
    health,
    restarting,
    error,
    tunnelStatus,
    fetchHealth,
    restartAddon,
    markRestarting,
    startPolling,
    stopPolling,
  }
})
