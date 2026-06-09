<template>
  <div>
    <!-- Score hero -->
    <div class="card" style="margin-bottom: 16px; text-align: center; padding: 2.5rem 2rem">
      <div style="font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-muted); margin-bottom: 1.25rem">
        Session Complete
      </div>

      <div class="score-circle" :style="{ background: scoreGradient }">
        <div class="score-circle-inner">
          <div class="score-circle-value">{{ feedbackData.average_score }}</div>
          <div class="score-circle-max">/10</div>
        </div>
      </div>

      <div style="font-size: 1.3rem; font-weight: 800; color: var(--navy); margin-bottom: 6px">{{ scoreLabel }}</div>
      <div style="font-size: 0.88rem; color: var(--text-muted)">{{ scoreSubtitle }}</div>

      <div v-if="scenarioData" style="margin-top: 1rem; display: inline-flex; align-items: center; gap: 10px; background: var(--bg); border-radius: 100px; padding: 6px 16px; font-size: 0.8rem; color: var(--text-muted)">
        <span :class="['badge', `badge-${scenarioData.difficulty}`]">{{ scenarioData.difficulty }}</span>
        {{ scenarioData.scenario_name }}
      </div>
    </div>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px">
      <!-- Score breakdown -->
      <div class="card">
        <div class="section-title">Score Breakdown</div>
        <div
          v-for="(score, key) in feedbackData.feedback"
          :key="key"
          class="score-bar-row"
        >
          <div class="score-bar-label">{{ formatKey(key) }}</div>
          <div class="score-bar-track">
            <div
              class="score-bar-fill"
              :style="{ width: `${score * 10}%`, background: scoreColor(score) }"
            ></div>
          </div>
          <div class="score-bar-value">{{ score }}/10</div>
        </div>
      </div>

      <!-- Strengths + improvements -->
      <div style="display: flex; flex-direction: column; gap: 16px">
        <div class="card" style="flex: 1">
          <div class="section-title" style="color: var(--success)">Strengths</div>
          <div
            v-for="(s, i) in feedbackData.strengths"
            :key="i"
            class="feedback-item"
          >
            <div class="feedback-dot" style="background: var(--success)"></div>
            {{ s }}
          </div>
        </div>

        <div class="card" style="flex: 1">
          <div class="section-title" style="color: var(--warning)">Areas to Improve</div>
          <div
            v-for="(imp, i) in feedbackData.improvements"
            :key="i"
            class="feedback-item"
          >
            <div class="feedback-dot" style="background: var(--warning)"></div>
            {{ imp }}
          </div>
        </div>
      </div>
    </div>

    <!-- Objection handling -->
    <div v-if="feedbackData.objection_responses.length > 0" class="card" style="margin-bottom: 16px">
      <div class="section-title">Objection Handling Review</div>
      <div v-for="(resp, i) in feedbackData.objection_responses" :key="i" class="objection-card">
        <div class="objection-card-header">Objection {{ i + 1 }}: "{{ resp.objection }}"</div>
        <div class="objection-card-body">
          <div class="objection-label">You said</div>
          <div class="objection-text" style="color: var(--text-muted); font-style: italic">
            "{{ resp.user_said }}"
          </div>
          <div class="objection-label">Stronger response</div>
          <div class="objection-tip">{{ resp.better_response }}</div>
        </div>
      </div>
    </div>

    <!-- Actions -->
    <div class="card" style="display: flex; gap: 12px; align-items: center; padding: 1.25rem">
      <button @click="$emit('try-again')" class="btn btn-primary btn-lg" style="flex: 1">
        Try Another Scenario
      </button>
      <button @click="$emit('try-again')" class="btn btn-secondary btn-lg" style="flex: 1">
        Retry This Scenario
      </button>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'FeedbackReport',
  props: {
    feedbackData: Object,
    scenarioData: Object,
  },
  emits: ['try-again'],
  setup(props) {
    const avg = computed(() => props.feedbackData.average_score)

    const scoreLabel = computed(() => {
      if (avg.value >= 8) return 'Outstanding Performance'
      if (avg.value >= 6) return 'Good Performance'
      if (avg.value >= 4) return 'Needs Improvement'
      return 'Keep Practicing'
    })

    const scoreSubtitle = computed(() => {
      if (avg.value >= 8) return 'You handled this call like a seasoned professional.'
      if (avg.value >= 6) return 'Solid effort — a few tweaks and you\'ll nail it.'
      if (avg.value >= 4) return 'You\'re getting there — focus on the improvement areas below.'
      return 'Every expert started as a beginner. Review the tips below and try again.'
    })

    const scoreGradient = computed(() => {
      if (avg.value >= 8) return 'conic-gradient(#059669 calc(var(--pct) * 1%), #e2e8f0 0)'
        .replace('var(--pct)', avg.value * 10)
      if (avg.value >= 5) return `conic-gradient(#d97706 ${avg.value * 10}%, #e2e8f0 0)`
      return `conic-gradient(#dc2626 ${avg.value * 10}%, #e2e8f0 0)`
    })

    const scoreColor = (score) => {
      if (score >= 7) return 'var(--success)'
      if (score >= 4) return 'var(--warning)'
      return 'var(--danger)'
    }

    const formatKey = (key) => key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())

    return { scoreLabel, scoreSubtitle, scoreGradient, scoreColor, formatKey }
  },
}
</script>
