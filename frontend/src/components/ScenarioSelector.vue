<template>
  <div class="card">
    <h2 class="text-center" style="margin-bottom: 2rem">Select Your Training Scenario</h2>

    <div v-if="error" class="alert alert-error">
      {{ error }}
    </div>

    <div class="form-group">
      <label for="industry">Industry</label>
      <select v-model="selectedIndustry" id="industry">
        <option value="">Select an industry...</option>
        <option v-for="industry in industries" :key="industry.id" :value="industry.id">
          {{ industry.name.replace('_', ' ').toUpperCase() }}
        </option>
      </select>
    </div>

    <div v-if="selectedIndustry" class="form-group">
      <label>Difficulty Level</label>
      <div style="display: flex; gap: 1rem; margin-top: 0.5rem">
        <button
          v-for="level in ['easy', 'medium', 'hard']"
          :key="level"
          @click="selectedDifficulty = level"
          :class="['btn', selectedDifficulty === level ? 'btn-primary' : 'btn-secondary']"
          style="flex: 1"
        >
          {{ level.toUpperCase() }}
        </button>
      </div>
    </div>

    <div v-if="filteredScenarios.length > 0" style="margin-top: 2rem">
      <h3 style="margin-bottom: 1rem; color: var(--text-dark)">Available Scenarios</h3>
      <div class="grid grid-2">
        <div
          v-for="scenario in filteredScenarios"
          :key="scenario.id"
          class="scenario-card"
          @click="selectScenario(scenario)"
        >
          <h4 style="margin-bottom: 0.5rem">{{ scenario.name }}</h4>
          <p>{{ scenario.description }}</p>
          <div style="margin-top: 1rem; font-size: 0.9rem">
            <strong>Deal Stage:</strong> {{ scenario.deal_stage.replace('_', ' ') }}
          </div>
          <span :class="['badge', `badge-${scenario.difficulty}`]">
            {{ scenario.difficulty.toUpperCase() }}
          </span>
        </div>
      </div>
    </div>

    <div v-if="selectedIndustry && filteredScenarios.length === 0 && !loading" class="alert alert-error">
      No scenarios found for this industry and difficulty level.
    </div>

    <div v-if="loading" class="center-content">
      <span class="loader"></span>
      <span style="margin-left: 1rem">Loading scenarios...</span>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { industriesAPI, scenariosAPI, callsAPI } from '../services/api'

export default {
  name: 'ScenarioSelector',
  emits: ['start-call'],
  setup(props, { emit }) {
    const industries = ref([])
    const scenarios = ref([])
    const selectedIndustry = ref('')
    const selectedDifficulty = ref('medium')
    const loading = ref(false)
    const error = ref('')

    const filteredScenarios = computed(() => {
      return scenarios.value.filter((s) => {
        if (selectedDifficulty.value && s.difficulty !== selectedDifficulty.value) {
          return false
        }
        return true
      })
    })

    const loadIndustries = async () => {
      try {
        loading.value = true
        error.value = ''
        const response = await industriesAPI.getAll()
        industries.value = response.data
      } catch (err) {
        error.value = 'Failed to load industries. Please try again.'
        console.error(err)
      } finally {
        loading.value = false
      }
    }

    const selectIndustry = async () => {
      if (!selectedIndustry.value) {
        scenarios.value = []
        return
      }

      try {
        loading.value = true
        error.value = ''
        const response = await scenariosAPI.getByIndustry(selectedIndustry.value)
        scenarios.value = response.data
        selectedDifficulty.value = 'medium'
      } catch (err) {
        error.value = 'Failed to load scenarios. Please try again.'
        console.error(err)
        scenarios.value = []
      } finally {
        loading.value = false
      }
    }

    const selectScenario = async (scenario) => {
      try {
        loading.value = true
        error.value = ''

        // Fetch full scenario details
        const detailResponse = await scenariosAPI.getDetail(scenario.id)
        const scenarioDetail = detailResponse.data

        // Start call
        const callResponse = await callsAPI.start(scenario.id)

        emit('start-call', {
          call_id: callResponse.data.call_id,
          scenario_id: scenario.id,
          scenario_name: scenario.name,
          difficulty: scenario.difficulty,
          ai_greeting: callResponse.data.ai_greeting,
          ...scenarioDetail,
        })
      } catch (err) {
        error.value = 'Failed to start call. Please try again.'
        console.error(err)
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      loadIndustries()
    })

    // Watch selectedIndustry
    return {
      industries,
      scenarios,
      selectedIndustry,
      selectedDifficulty,
      filteredScenarios,
      loading,
      error,
      selectScenario,
      selectIndustry,
    }
  },
  watch: {
    selectedIndustry() {
      this.selectIndustry()
    },
  },
}
</script>
