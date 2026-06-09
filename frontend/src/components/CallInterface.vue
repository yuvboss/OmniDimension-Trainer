<template>
  <div>
    <!-- Header card -->
    <div class="card" style="margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; padding: 1.25rem 1.5rem">
      <div>
        <div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: var(--text-muted); margin-bottom: 4px">Active Session</div>
        <div style="font-size: 1.05rem; font-weight: 700; color: var(--navy)">{{ scenarioData.scenario_name }}</div>
        <div style="font-size: 0.82rem; color: var(--text-muted); margin-top: 3px">
          <span :class="['badge', `badge-${scenarioData.difficulty}`]" style="margin-right: 8px">{{ scenarioData.difficulty }}</span>
          Calling {{ scenarioData.phone_number }}
        </div>
      </div>
      <div style="text-align: right">
        <div style="font-size: 1.8rem; font-weight: 800; color: var(--navy); font-variant-numeric: tabular-nums">{{ formatTime(elapsed) }}</div>
        <div style="font-size: 0.72rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em">Elapsed</div>
      </div>
    </div>

    <div v-if="error" class="alert alert-error" style="margin-bottom: 16px">
      <span>⚠</span> {{ error }}
    </div>

    <!-- Status panel -->
    <div class="card call-status-panel" style="margin-bottom: 16px">

      <!-- Ringing -->
      <template v-if="isRinging">
        <div class="pulse-ring" style="margin: 0 auto">
          <span class="pulse-ring-icon">📞</span>
        </div>
        <h3 style="font-size: 1.2rem; font-weight: 700; color: var(--navy); margin-bottom: 8px">Calling your phone...</h3>
        <p style="color: var(--text-muted); max-width: 360px; margin: 0 auto; font-size: 0.9rem">
          Your phone will ring shortly. Pick up and the AI customer will start the conversation.
        </p>
        <p style="color: var(--text-muted); max-width: 360px; margin: 0.75rem auto 0; font-size: 0.82rem; background: #fffbeb; border: 1px solid #fde68a; border-radius: 8px; padding: 8px 14px; color: #92400e">
          The call may take a couple of minutes to connect — keep your phone nearby.
        </p>
      </template>

      <!-- In progress -->
      <template v-else-if="isInProgress">
        <div style="font-size: 3rem; margin-bottom: 1rem">🎯</div>
        <div style="margin-bottom: 8px">
          <span class="live-dot"></span>
          <span style="font-size: 1.1rem; font-weight: 700; color: var(--success)">Call in Progress</span>
        </div>
        <p style="color: var(--text-muted); margin-bottom: 1.25rem; font-size: 0.9rem">
          You're live with the AI customer. Stay confident and address their concerns.
        </p>
        <div style="display: flex; flex-wrap: wrap; gap: 8px; justify-content: center">
          <span
            v-for="obj in topObjections"
            :key="obj"
            style="background: #fff7ed; border: 1px solid #fed7aa; color: #c2410c; border-radius: 100px; padding: 4px 14px; font-size: 0.78rem; font-weight: 500"
          >
            Watch for: {{ obj }}
          </span>
        </div>
      </template>

      <!-- Completed -->
      <template v-else-if="isCompleted">
        <div style="font-size: 3rem; margin-bottom: 1rem">✅</div>
        <h3 style="font-size: 1.1rem; font-weight: 700; color: var(--success); margin-bottom: 8px">Call Complete!</h3>
        <p style="color: var(--text-muted); font-size: 0.9rem">Analysing your performance and generating feedback...</p>
        <div style="margin-top: 1rem"><span class="loader loader-dark"></span></div>
      </template>

      <!-- Failed -->
      <template v-else-if="isFailed">
        <div style="font-size: 3rem; margin-bottom: 1rem">❌</div>
        <h3 style="font-size: 1.1rem; font-weight: 700; color: var(--danger); margin-bottom: 8px">Call Could Not Connect</h3>
        <p style="color: var(--text-muted); font-size: 0.88rem">Status: {{ callStatus }}. Check your number and try again.</p>
      </template>

      <!-- Default loading -->
      <template v-else>
        <span class="loader loader-dark" style="width: 28px; height: 28px; border-width: 3px; margin-bottom: 1rem"></span>
        <p style="color: var(--text-muted); font-size: 0.9rem">Connecting to OmniDimension...</p>
      </template>
    </div>

    <!-- Two-col info row -->
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px">
      <!-- Objective -->
      <div class="card" style="padding: 1.25rem">
        <div class="section-title">Your Objective</div>
        <p style="font-size: 0.88rem; color: var(--text); line-height: 1.6">{{ scenarioData.objective || '—' }}</p>
      </div>

      <!-- Tips -->
      <div class="card" style="padding: 1.25rem">
        <div class="section-title">Quick Tips</div>
        <div style="font-size: 0.83rem; color: var(--text-muted); line-height: 1.7">
          <div>• Acknowledge concerns before countering</div>
          <div>• Use specific numbers and facts</div>
          <div>• Always close with a next step</div>
        </div>
      </div>
    </div>

    <!-- End call button -->
    <div class="card" style="padding: 1.25rem; display: flex; align-items: center; gap: 16px">
      <button
        @click="handleEndCall"
        :disabled="isFetchingFeedback"
        class="btn btn-primary btn-lg"
        style="flex: 1"
      >
        <span v-if="isFetchingFeedback" class="loader" style="width: 14px; height: 14px"></span>
        {{ isFetchingFeedback ? 'Loading Feedback...' : 'End Session & Get Feedback' }}
      </button>
      <p style="font-size: 0.78rem; color: var(--text-muted); max-width: 200px; line-height: 1.5">
        Click anytime to score your session, or hang up and we'll auto-detect it.
      </p>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { callsAPI } from '../services/api'

export default {
  name: 'CallInterface',
  props: { callId: String, scenarioData: Object },
  emits: ['end-call', 'back'],
  setup(props, { emit }) {
    const callStatus = ref('calling')
    const isFetchingFeedback = ref(false)
    const error = ref('')
    const elapsed = ref(0)

    let elapsedInterval = null
    let pollInterval = null

    const RINGING = new Set(['calling', 'ringing', 'initiated', 'dispatched'])
    const IN_PROGRESS = new Set(['in_progress', 'ongoing', 'active', 'answered'])
    const DONE = new Set(['completed', 'ended', 'finished'])
    const FAILED = new Set(['failed', 'no_answer', 'busy', 'cancelled'])

    const isRinging = computed(() => RINGING.has(callStatus.value))
    const isInProgress = computed(() => IN_PROGRESS.has(callStatus.value))
    const isCompleted = computed(() => DONE.has(callStatus.value))
    const isFailed = computed(() => FAILED.has(callStatus.value))

    const topObjections = computed(() => (props.scenarioData?.common_objections || []).slice(0, 2))

    const formatTime = (s) => `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`

    const stopPolling = () => { if (pollInterval) { clearInterval(pollInterval); pollInterval = null } }

    const fetchFeedback = async () => {
      try {
        isFetchingFeedback.value = true
        error.value = ''
        const response = await callsAPI.end(props.callId)
        emit('end-call', response.data)
      } catch {
        error.value = 'Failed to load feedback. Please try again.'
      } finally {
        isFetchingFeedback.value = false
      }
    }

    const pollStatus = async () => {
      try {
        const response = await callsAPI.getStatus(props.callId)
        callStatus.value = response.data.status
        if (DONE.has(callStatus.value)) { stopPolling(); await fetchFeedback() }
        else if (FAILED.has(callStatus.value)) { stopPolling() }
      } catch { /* keep polling on network hiccup */ }
    }

    const handleEndCall = async () => { stopPolling(); await fetchFeedback() }

    onMounted(() => {
      elapsedInterval = setInterval(() => { elapsed.value++ }, 1000)
      pollInterval = setInterval(pollStatus, 6000)
      setTimeout(pollStatus, 3000)
    })

    onUnmounted(() => {
      if (elapsedInterval) clearInterval(elapsedInterval)
      stopPolling()
    })

    return { callStatus, isFetchingFeedback, error, elapsed, topObjections,
      isRinging, isInProgress, isCompleted, isFailed, formatTime, handleEndCall }
  },
}
</script>

<style scoped>
@keyframes ring-pulse {
  0% { transform: scale(0.8); opacity: 0.8; }
  100% { transform: scale(1.4); opacity: 0; }
}
</style>
