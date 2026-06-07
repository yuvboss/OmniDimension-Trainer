<template>
  <nav class="navbar">
    <div class="navbar-content">
      <h1>🎤 Sales Training Voice Simulator</h1>
      <button v-if="currentView !== 'selector'" @click="goHome" class="btn btn-secondary">
        Home
      </button>
    </div>
  </nav>

  <div class="container">
    <ScenarioSelector
      v-if="currentView === 'selector'"
      @start-call="handleStartCall"
    />
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
      @try-again="goHome"
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
  components: {
    ScenarioSelector,
    CallInterface,
    FeedbackReport,
  },
  setup() {
    const currentView = ref('selector')
    const currentCallId = ref(null)
    const currentScenario = ref(null)
    const feedbackData = ref(null)

    const handleStartCall = (callData) => {
      currentCallId.value = callData.call_id
      currentScenario.value = callData
      currentView.value = 'call'
    }

    const handleEndCall = (feedback) => {
      feedbackData.value = feedback
      currentView.value = 'feedback'
    }

    const goHome = () => {
      currentView.value = 'selector'
      currentCallId.value = null
      currentScenario.value = null
      feedbackData.value = null
    }

    return {
      currentView,
      currentCallId,
      currentScenario,
      feedbackData,
      handleStartCall,
      handleEndCall,
      goHome,
    }
  },
}
</script>
