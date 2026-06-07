<template>
  <div class="card">
    <div style="text-align: center; margin-bottom: 2rem">
      <h2>Call Complete! 🎉</h2>
      <p style="color: var(--text-light)">Here's your performance summary</p>
    </div>

    <!-- Average Score -->
    <div style="text-align: center; margin-bottom: 2rem">
      <div style="font-size: 3rem; font-weight: bold; color: var(--primary-color)">
        {{ feedbackData.average_score }}
      </div>
      <div style="font-size: 1.5rem; color: #fbbf24">
        <span v-for="i in 10" :key="i" style="margin: 0 2px">
          {{ i <= Math.round(feedbackData.average_score) ? '★' : '☆' }}
        </span>
      </div>
      <p style="color: var(--text-light); margin-top: 0.5rem">Overall Performance</p>
    </div>

    <!-- Scores Grid -->
    <div class="grid" style="margin-bottom: 2rem">
      <div
        v-for="(score, key) in feedbackData.feedback"
        :key="key"
        style="
          background: var(--light-bg);
          padding: 1rem;
          border-radius: 8px;
          text-align: center;
        "
      >
        <div style="font-size: 1.5rem; font-weight: bold; color: var(--primary-color)">
          {{ score }}/10
        </div>
        <div style="font-size: 0.9rem; color: var(--text-dark); text-transform: capitalize">
          {{ key.replace('_', ' ') }}
        </div>
        <div style="font-size: 0.8rem; color: var(--text-light); margin-top: 0.25rem">
          <span v-for="i in 10" :key="i">{{ i <= score ? '★' : '☆' }}</span>
        </div>
      </div>
    </div>

    <!-- Strengths -->
    <div style="margin-bottom: 2rem">
      <h3 style="color: var(--secondary-color); margin-bottom: 1rem">✓ Strengths</h3>
      <ul style="list-style: none; padding: 0">
        <li v-for="(strength, index) in feedbackData.strengths" :key="index" style="margin-bottom: 0.5rem">
          <span style="color: var(--secondary-color); font-weight: bold">•</span>
          {{ strength }}
        </li>
      </ul>
    </div>

    <!-- Areas for Improvement -->
    <div style="margin-bottom: 2rem">
      <h3 style="color: #f97316; margin-bottom: 1rem">⬆ Areas for Improvement</h3>
      <ul style="list-style: none; padding: 0">
        <li v-for="(improvement, index) in feedbackData.improvements" :key="index" style="margin-bottom: 0.5rem">
          <span style="color: #f97316; font-weight: bold">•</span>
          {{ improvement }}
        </li>
      </ul>
    </div>

    <!-- Objection Handling -->
    <div v-if="feedbackData.objection_responses.length > 0" style="margin-bottom: 2rem">
      <h3 style="color: var(--primary-color); margin-bottom: 1rem">💬 Objection Handling</h3>
      <div v-for="(response, index) in feedbackData.objection_responses" :key="index" style="margin-bottom: 1.5rem">
        <div style="background: #eff6ff; padding: 1rem; border-left: 4px solid var(--primary-color); border-radius: 4px">
          <h4 style="color: var(--primary-color); margin-bottom: 0.5rem">Objection:</h4>
          <p style="margin-bottom: 1rem">{{ response.objection }}</p>

          <h4 style="color: #6b7280; margin-bottom: 0.5rem">You said:</h4>
          <p style="color: var(--text-light); margin-bottom: 1rem; font-style: italic">{{ response.user_said }}</p>

          <h4 style="color: var(--secondary-color); margin-bottom: 0.5rem">💡 Better response:</h4>
          <p style="color: var(--text-dark)">{{ response.better_response }}</p>
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div style="display: flex; gap: 1rem; margin-top: 2rem">
      <button @click="tryAgain" class="btn btn-primary" style="flex: 1">
        Try Another Scenario
      </button>
      <button @click="viewDetails" class="btn btn-secondary" style="flex: 1">
        View Call Details
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FeedbackReport',
  props: {
    feedbackData: Object,
  },
  emits: ['try-again'],
  setup(props, { emit }) {
    const tryAgain = () => {
      emit('try-again')
    }

    const viewDetails = () => {
      alert('Call details view coming in Phase 2!')
    }

    return {
      tryAgain,
      viewDetails,
    }
  },
}
</script>
