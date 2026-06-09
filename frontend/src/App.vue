<template>
  <nav class="navbar">
    <div class="navbar-content">
      <div class="navbar-brand">
        <img src="/omnidimension_logo.jpeg" alt="OmniDimension" style="height: 36px; width: auto; border-radius: 6px; object-fit: contain" />
        <div>
          <div class="navbar-title">OmniDimension Trainer</div>
          <div class="navbar-subtitle">Powered by OmniDimension Voice Agents</div>
        </div>
      </div>
      <button v-if="currentView !== 'selector'" @click="goHome" class="btn btn-ghost" style="color: #94a3b8; font-size: 0.85rem">
        ← Back to Scenarios
      </button>
    </div>

    <!-- Step bar -->
    <div class="step-bar">
      <div class="step-bar-inner">
        <div :class="['step', currentView === 'selector' ? 'active' : 'done']">
          <div class="step-num">{{ currentView === 'selector' ? '1' : '✓' }}</div>
          Choose Scenario
        </div>
        <div class="step-divider"></div>
        <div :class="['step', currentView === 'call' ? 'active' : currentView === 'feedback' ? 'done' : '']">
          <div class="step-num">{{ currentView === 'feedback' ? '✓' : '2' }}</div>
          Live Call
        </div>
        <div class="step-divider"></div>
        <div :class="['step', currentView === 'feedback' ? 'active' : '']">
          <div class="step-num">3</div>
          Review Results
        </div>
      </div>
    </div>
  </nav>

  <div class="container">
    <ScenarioSelector v-if="currentView === 'selector'" :retry-data="retryScenario" @start-call="handleStartCall" />
    <CallInterface
      v-else-if="currentView === 'call'"
      :call-id="currentCallId"
      :scenario-data="currentScenario"
      @end-call="handleEndCall"
      @back="goHome"
    />
    <FeedbackReport
      v-else-if="currentView === 'feedback'"
      :feedback-data="feedbackData"
      :scenario-data="currentScenario"
      @try-again="goHome"
      @retry="handleRetry"
    />
  </div>
</template>

<script>
import { ref } from 'vue'
import ScenarioSelector from './components/ScenarioSelector.vue'
import CallInterface from './components/CallInterface.vue'
import FeedbackReport from './components/FeedbackReport.vue'

export default {
  name: 'App',
  components: { ScenarioSelector, CallInterface, FeedbackReport },
  setup() {
    const currentView = ref('selector')
    const currentCallId = ref(null)
    const currentScenario = ref(null)
    const feedbackData = ref(null)
    const retryScenario = ref(null)

    const handleStartCall = (callData) => {
      currentCallId.value = callData.call_id
      currentScenario.value = callData
      retryScenario.value = null
      currentView.value = 'call'
    }

    const handleEndCall = (feedback) => {
      feedbackData.value = feedback
      currentView.value = 'feedback'
    }

    const handleRetry = () => {
      retryScenario.value = {
        industry_id: currentScenario.value.industry_id,
        scenario_id: currentScenario.value.id || currentScenario.value.scenario_id,
        difficulty: currentScenario.value.difficulty,
      }
      currentView.value = 'selector'
      currentCallId.value = null
      feedbackData.value = null
    }

    const goHome = () => {
      retryScenario.value = null
      currentView.value = 'selector'
      currentCallId.value = null
      currentScenario.value = null
      feedbackData.value = null
    }

    return { currentView, currentCallId, currentScenario, feedbackData, retryScenario, handleStartCall, handleEndCall, handleRetry, goHome }
  },
}
</script>
