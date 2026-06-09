<template>
  <div>
    <!-- Welcome banner -->
    <div style="background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 60%, #1e40af 100%); border-radius: var(--radius); padding: 2.5rem 2rem; margin-bottom: 20px; position: relative; overflow: hidden">
      <!-- Background decoration -->
      <div style="position: absolute; top: -40px; right: -40px; width: 200px; height: 200px; background: rgba(255,255,255,0.03); border-radius: 50%"></div>
      <div style="position: absolute; bottom: -60px; right: 60px; width: 160px; height: 160px; background: rgba(255,255,255,0.03); border-radius: 50%"></div>

      <div style="position: relative; z-index: 1; max-width: 680px">
        <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(255,255,255,0.1); border-radius: 100px; padding: 5px 14px; margin-bottom: 1rem">
          <span style="font-size: 0.75rem">🎤</span>
          <span style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #93c5fd">Powered by OmniDimension</span>
        </div>
        <h1 style="font-size: 1.75rem; font-weight: 800; color: white; margin-bottom: 0.75rem; line-height: 1.25; letter-spacing: -0.02em">
          Practice sales calls with AI customers, before the real thing.
        </h1>
        <p style="font-size: 0.95rem; color: #94a3b8; line-height: 1.65; margin-bottom: 0">
          This platform is powered by OmniDimension voice agents and helps employees across different industries practice talking to customers. This helps improve their communication, handle tough objections, and give real customers the best experience possible.
        </p>
      </div>
    </div>

    <!-- How it works -->
    <div class="card" style="margin-bottom: 20px; padding: 1.5rem 2rem">
      <div class="section-title" style="margin-bottom: 1.25rem">How it works</div>
      <div class="how-it-works-grid" style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0">
        <div class="how-it-works-step" style="display: flex; align-items: flex-start; gap: 14px; padding-right: 2rem">
          <div style="width: 36px; height: 36px; border-radius: 10px; background: var(--primary-pale); border: 1.5px solid #bfdbfe; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; flex-shrink: 0">🏢</div>
          <div>
            <div style="font-size: 0.88rem; font-weight: 700; color: var(--navy); margin-bottom: 3px">1. Choose a scenario</div>
            <div style="font-size: 0.8rem; color: var(--text-muted); line-height: 1.55">Pick your industry, difficulty level, and a specific customer situation to practice.</div>
          </div>
        </div>
        <div class="how-it-works-step" style="display: flex; align-items: flex-start; gap: 14px; padding: 0 2rem; border-left: 1px solid var(--border); border-right: 1px solid var(--border)">
          <div style="width: 36px; height: 36px; border-radius: 10px; background: #fff7ed; border: 1.5px solid #fed7aa; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; flex-shrink: 0">📞</div>
          <div>
            <div style="font-size: 0.88rem; font-weight: 700; color: var(--navy); margin-bottom: 3px">2. Take the call</div>
            <div style="font-size: 0.8rem; color: var(--text-muted); line-height: 1.55">Enter your phone number: the AI customer calls you directly and runs a real conversation.</div>
          </div>
        </div>
        <div class="how-it-works-step" style="display: flex; align-items: flex-start; gap: 14px; padding-left: 2rem">
          <div style="width: 36px; height: 36px; border-radius: 10px; background: var(--success-pale); border: 1.5px solid #a7f3d0; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; flex-shrink: 0">📊</div>
          <div>
            <div style="font-size: 0.88rem; font-weight: 700; color: var(--navy); margin-bottom: 3px">3. Review your feedback</div>
            <div style="font-size: 0.8rem; color: var(--text-muted); line-height: 1.55">Get a scored breakdown of your performance with specific tips to improve each area.</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Hero -->
    <div style="margin-bottom: 20px">
      <h2 style="font-size: 1.4rem; font-weight: 800; color: var(--navy); margin-bottom: 4px; letter-spacing: -0.02em">
        Start a Training Session
      </h2>
      <p style="color: var(--text-muted); font-size: 0.9rem">
        Pick an industry, set your difficulty, and take a live call with an AI customer.
      </p>
    </div>

    <div v-if="error" class="alert alert-error">
      <span>⚠</span> {{ error }}
    </div>

    <!-- Step 1: Industry -->
    <div class="card" style="margin-bottom: 16px">
      <div class="section-title">Step 1 — Choose Industry</div>
      <div class="industry-grid">
        <div
          class="industry-card"
          :class="{ selected: selectedIndustry === ind.id }"
          v-for="ind in industries"
          :key="ind.id"
          @click="selectedIndustry = ind.id"
        >
          <span class="industry-icon">{{ ind.name === 'real_estate' ? '🏠' : '🏥' }}</span>
          <h3>{{ ind.name === 'real_estate' ? 'Real Estate' : 'Healthcare' }}</h3>
          <p>{{ ind.name === 'real_estate' ? 'Buyers, investors & site visits' : 'Patients, costs & appointments' }}</p>
        </div>
      </div>
    </div>

    <!-- Step 2: Difficulty -->
    <div v-if="selectedIndustry" class="card" style="margin-bottom: 16px">
      <div class="section-title">Step 2 — Select Difficulty</div>
      <div class="difficulty-pills">
        <div
          v-for="level in difficulties"
          :key="level.value"
          class="pill"
          :class="selectedDifficulty === level.value ? `active-${level.value}` : ''"
          @click="selectedDifficulty = level.value"
        >
          {{ level.icon }} {{ level.label }}
        </div>
      </div>
      <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 10px">
        {{ difficultyHint }}
      </p>
    </div>

    <!-- Step 3: Scenario -->
    <div v-if="selectedIndustry" class="card" style="margin-bottom: 16px">
      <div class="section-title">Step 3 — Pick a Scenario</div>

      <div v-if="loading" style="text-align: center; padding: 2rem; color: var(--text-muted)">
        <span class="loader loader-dark"></span>
        <span style="margin-left: 10px; font-size: 0.9rem">Loading scenarios...</span>
      </div>

      <div v-else-if="filteredScenarios.length === 0" class="alert alert-info">
        No scenarios available for this difficulty. Try a different level.
      </div>

      <div v-else class="scenario-grid">
        <div
          v-for="scenario in filteredScenarios"
          :key="scenario.id"
          class="scenario-card"
          :class="{ selected: pendingScenario && pendingScenario.id === scenario.id }"
          @click="selectScenario(scenario)"
        >
          <h4>{{ scenario.name }}</h4>
          <p>{{ scenario.description }}</p>
          <div class="scenario-meta">
            <span class="badge badge-stage">{{ scenario.deal_stage.replace(/_/g, ' ') }}</span>
            <span :class="['badge', `badge-${scenario.difficulty}`]">{{ scenario.difficulty }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Step 4: Phone + launch -->
    <div v-if="pendingScenario" class="card">
      <div class="section-title">Step 4 — Enter Your Number & Start</div>

      <div style="display: flex; align-items: flex-start; gap: 16px; margin-bottom: 1.25rem; padding: 14px; background: var(--bg); border-radius: 8px; border: 1px solid var(--border)">
        <div style="font-size: 1.5rem">📋</div>
        <div>
          <div style="font-weight: 600; font-size: 0.9rem; color: var(--text); margin-bottom: 2px">{{ pendingScenario.name }}</div>
          <div style="font-size: 0.82rem; color: var(--text-muted)">{{ pendingScenario.description }}</div>
        </div>
      </div>

      <div style="margin-bottom: 1rem">
        <label class="form-label" for="phone">Your Phone Number</label>
        <input
          id="phone"
          v-model="phoneNumber"
          type="tel"
          placeholder="+14155550123"
          @keyup.enter="confirmStart"
          style="font-size: 1rem; letter-spacing: 0.02em"
        />
        <p style="font-size: 0.78rem; color: var(--text-muted); margin-top: 6px">
          Include country code — e.g. +1 for US, +44 for UK, +91 for India
        </p>
      </div>

      <div style="background: #fffbeb; border: 1px solid #fde68a; border-radius: 8px; padding: 12px 14px; margin-bottom: 1.25rem; font-size: 0.83rem; color: #92400e">
        <strong>How it works:</strong> The AI customer will call your phone. Have a natural sales conversation, handle their objections, then hang up to see your score.
      </div>

      <div style="display: flex; gap: 10px">
        <button
          @click="confirmStart"
          :disabled="!phoneNumber.trim() || loading"
          class="btn btn-primary btn-lg"
          style="flex: 1"
        >
          <span v-if="loading" class="loader" style="width: 14px; height: 14px; margin-right: 4px"></span>
          {{ loading ? 'Connecting...' : '📞 Call Me Now' }}
        </button>
        <button @click="pendingScenario = null" class="btn btn-secondary btn-lg">
          Cancel
        </button>
      </div>
    </div>

    <!-- Empty state -->
    <div v-if="!selectedIndustry" style="text-align: center; padding: 2rem; color: var(--text-muted)">
      <div style="font-size: 3rem; margin-bottom: 1rem">👆</div>
      <p style="font-size: 0.95rem">Select an industry above to get started</p>
    </div>

    <!-- Adding a new industry -->
    <div style="margin-top: 32px; padding: 1.25rem 1.5rem; border-radius: var(--radius); border: 1.5px dashed var(--border); background: var(--bg); display: flex; align-items: flex-start; gap: 14px">
      <div style="font-size: 1.2rem; margin-top: 1px">🏗️</div>
      <div>
        <div style="font-size: 0.85rem; font-weight: 700; color: var(--navy); margin-bottom: 4px">Want to add a new industry?</div>
        <div style="font-size: 0.8rem; color: var(--text-muted); line-height: 1.6">
          No code changes needed. New industries can be added by providing a set of scenario configurations: industry name, customer type, deal stages, common questions, common objections, ideal responses, and difficulty level. The core system automatically handles the voice agent setup and feedback generation for any industry.
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { industriesAPI, scenariosAPI, callsAPI } from '../services/api'

export default {
  name: 'ScenarioSelector',
  props: { retryData: { type: Object, default: null } },
  emits: ['start-call'],
  setup(props, { emit }) {
    const industries = ref([])
    const scenarios = ref([])
    const selectedIndustry = ref('')
    const selectedDifficulty = ref('medium')
    const pendingScenario = ref(null)
    const phoneNumber = ref(localStorage.getItem('omnidim_phone') || '')
    const loading = ref(false)
    const error = ref('')
    const retryPending = ref(null)

    const difficulties = [
      { value: 'easy', label: 'Easy', icon: '🟢' },
      { value: 'medium', label: 'Medium', icon: '🟡' },
      { value: 'hard', label: 'Hard', icon: '🔴' },
    ]

    const difficultyHint = computed(() => ({
      easy: 'Friendly prospect with 1 objection — great for first-time practice.',
      medium: 'Moderately skeptical with 2 objections — standard training level.',
      hard: 'Tough, well-researched prospect with 3+ objections — advanced challenge.',
    }[selectedDifficulty.value]))

    const filteredScenarios = computed(() =>
      scenarios.value.filter(s => !selectedDifficulty.value || s.difficulty === selectedDifficulty.value)
    )

    const loadIndustries = async () => {
      try {
        const response = await industriesAPI.getAll()
        industries.value = response.data
      } catch {
        error.value = 'Failed to load industries. Make sure the backend is running.'
      }
    }

    const selectIndustry = async () => {
      if (!selectedIndustry.value) { scenarios.value = []; return }
      try {
        loading.value = true
        error.value = ''
        const response = await scenariosAPI.getByIndustry(selectedIndustry.value)
        scenarios.value = response.data
        selectedDifficulty.value = retryPending.value?.difficulty || 'medium'
        pendingScenario.value = null
        if (retryPending.value) {
          const { scenario_id } = retryPending.value
          retryPending.value = null
          const match = scenarios.value.find(s => s.id === scenario_id)
          if (match) {
            pendingScenario.value = match
            setTimeout(() => document.getElementById('phone')?.scrollIntoView({ behavior: 'smooth', block: 'center' }), 150)
          }
        }
      } catch {
        error.value = 'Failed to load scenarios.'
        scenarios.value = []
      } finally {
        loading.value = false
      }
    }

    const selectScenario = (scenario) => {
      pendingScenario.value = scenario
      error.value = ''
      setTimeout(() => {
        document.getElementById('phone')?.scrollIntoView({ behavior: 'smooth', block: 'center' })
      }, 100)
    }

    const confirmStart = async () => {
      const phone = phoneNumber.value.trim()
      if (!phone || !pendingScenario.value) return
      if (!phone.startsWith('+')) {
        error.value = 'Phone number must start with + and country code (e.g. +14155550123)'
        return
      }
      try {
        loading.value = true
        error.value = ''
        localStorage.setItem('omnidim_phone', phone)
        const [detailRes, callRes] = await Promise.all([
          scenariosAPI.getDetail(pendingScenario.value.id),
          callsAPI.start(pendingScenario.value.id, phone),
        ])
        emit('start-call', {
          call_id: callRes.data.call_id,
          scenario_id: pendingScenario.value.id,
          scenario_name: pendingScenario.value.name,
          difficulty: pendingScenario.value.difficulty,
          industry_id: selectedIndustry.value,
          phone_number: phone,
          message: callRes.data.message,
          ...detailRes.data,
        })
      } catch (err) {
        error.value = err.response?.data?.detail || 'Failed to start call. Please try again.'
      } finally {
        loading.value = false
      }
    }

    onMounted(async () => {
      await loadIndustries()
      if (props.retryData) {
        retryPending.value = props.retryData
        selectedIndustry.value = props.retryData.industry_id
      }
    })

    return {
      industries, scenarios, selectedIndustry, selectedDifficulty,
      filteredScenarios, pendingScenario, phoneNumber, loading, error,
      difficulties, difficultyHint, selectIndustry, selectScenario, confirmStart,
    }
  },
  watch: {
    selectedIndustry() { this.pendingScenario = null; this.selectIndustry() },
  },
}
</script>
