<template>
  <div class="card">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem">
      <div>
        <h2>{{ scenarioData.scenario_name }}</h2>
        <p style="color: var(--text-light)">Difficulty: {{ scenarioData.difficulty.toUpperCase() }}</p>
      </div>
      <div style="text-align: right">
        <div style="font-size: 2rem; font-weight: bold; color: var(--primary-color)">
          {{ formatTime(callDuration) }}
        </div>
        <p style="color: var(--text-light); font-size: 0.9rem">Call Duration</p>
      </div>
    </div>

    <div v-if="error" class="alert alert-error">
      {{ error }}
    </div>

    <!-- AI Response Display -->
    <div style="background: var(--light-bg); padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem">
      <h4 style="margin-bottom: 0.5rem; color: var(--primary-color)">Customer/Patient:</h4>
      <p style="font-size: 1.1rem; line-height: 1.6; color: var(--text-dark)">
        {{ currentAIResponse || scenarioData.ai_greeting }}
      </p>
    </div>

    <!-- Voice Input -->
    <div style="margin-bottom: 2rem">
      <div v-if="!speechSupported" class="alert alert-error">
        Your browser does not support speech recognition. Please use Chrome or Edge.
      </div>

      <div v-else style="display: flex; flex-direction: column; align-items: center; gap: 1rem">
        <!-- Mic Button -->
        <button
          @click="toggleListening"
          :disabled="isProcessing"
          :style="{
            width: '80px',
            height: '80px',
            borderRadius: '50%',
            border: 'none',
            cursor: isProcessing ? 'not-allowed' : 'pointer',
            fontSize: '2rem',
            background: isListening ? '#ef4444' : 'var(--primary-color)',
            color: 'white',
            boxShadow: isListening ? '0 0 0 8px rgba(239,68,68,0.25)' : '0 2px 8px rgba(0,0,0,0.15)',
            transition: 'all 0.2s',
          }"
        >
          {{ isListening ? '⏹' : '🎤' }}
        </button>

        <p style="color: var(--text-light); font-size: 0.9rem">
          {{ isListening ? 'Listening… speak now' : 'Tap to speak' }}
        </p>

        <!-- Transcript preview -->
        <div
          v-if="userResponse"
          style="width: 100%; background: var(--light-bg); padding: 1rem; border-radius: 8px; font-size: 1rem; color: var(--text-dark); min-height: 3rem"
        >
          {{ userResponse }}
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div style="display: flex; gap: 1rem; margin-bottom: 2rem">
      <button
        @click="sendResponse"
        :disabled="!userResponse.trim() || isProcessing"
        class="btn btn-primary"
        style="flex: 1"
      >
        <span v-if="isProcessing" class="loader" style="display: inline-block; margin-right: 0.5rem"></span>
        {{ isProcessing ? 'Processing...' : 'Send Response' }}
      </button>
      <button @click="endCall" :disabled="isProcessing" class="btn btn-secondary">
        End Call
      </button>
    </div>

    <!-- Conversation History -->
    <div v-if="conversationHistory.length > 0" style="margin-top: 2rem">
      <h4 style="margin-bottom: 1rem; color: var(--text-dark)">Conversation History</h4>
      <div style="background: var(--light-bg); padding: 1rem; border-radius: 8px; max-height: 300px; overflow-y: auto">
        <div
          v-for="(message, index) in conversationHistory"
          :key="index"
          style="margin-bottom: 0.5rem; padding: 0.5rem"
        >
          <strong :style="{ color: message.sender === 'ai' ? '#3b82f6' : '#10b981' }">
            {{ message.sender === 'ai' ? 'Customer/Patient' : 'You' }}:
          </strong>
          <p style="margin: 0.25rem 0 0 1rem; font-size: 0.9rem; color: var(--text-light)">
            {{ message.text }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { callsAPI } from '../services/api'

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition

export default {
  name: 'CallInterface',
  props: {
    callId: String,
    scenarioData: Object,
  },
  emits: ['end-call', 'back'],
  setup(props, { emit }) {
    const userResponse = ref('')
    const currentAIResponse = ref('')
    const isProcessing = ref(false)
    const isListening = ref(false)
    const speechSupported = ref(!!SpeechRecognition)
    const error = ref('')
    const callDuration = ref(0)
    const conversationHistory = ref([])

    let durationInterval = null
    let recognition = null

    if (SpeechRecognition) {
      recognition = new SpeechRecognition()
      recognition.continuous = false
      recognition.interimResults = true
      recognition.lang = 'en-US'

      recognition.onresult = (event) => {
        const transcript = Array.from(event.results)
          .map((r) => r[0].transcript)
          .join('')
        userResponse.value = transcript
      }

      recognition.onend = () => {
        isListening.value = false
      }

      recognition.onerror = (event) => {
        isListening.value = false
        if (event.error !== 'no-speech') {
          error.value = `Speech error: ${event.error}`
        }
      }
    }

    const toggleListening = () => {
      if (!recognition) return
      if (isListening.value) {
        recognition.stop()
      } else {
        userResponse.value = ''
        error.value = ''
        recognition.start()
        isListening.value = true
      }
    }

    const formatTime = (seconds) => {
      const mins = Math.floor(seconds / 60)
      const secs = seconds % 60
      return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
    }

    const sendResponse = async () => {
      if (!userResponse.value.trim()) return

      try {
        isProcessing.value = true
        error.value = ''

        // Add user message to history
        conversationHistory.value.push({
          sender: 'user',
          text: userResponse.value,
        })

        // Send to API
        const response = await callsAPI.respond(props.callId, userResponse.value)

        // Add AI response to history
        conversationHistory.value.push({
          sender: 'ai',
          text: response.data.ai_response,
        })

        currentAIResponse.value = response.data.ai_response
        userResponse.value = ''

        if (response.data.objection_raised) {
          // Show objection feedback
          setTimeout(() => {
            console.log('Objection raised:', response.data.ai_response)
          }, 500)
        }
      } catch (err) {
        error.value = 'Failed to send response. Please try again.'
        console.error(err)
      } finally {
        isProcessing.value = false
      }
    }

    const endCall = async () => {
      try {
        isProcessing.value = true
        error.value = ''

        const response = await callsAPI.end(props.callId, callDuration.value)
        emit('end-call', response.data)
      } catch (err) {
        error.value = 'Failed to end call. Please try again.'
        console.error(err)
      } finally {
        isProcessing.value = false
      }
    }

    onMounted(() => {
      // Initialize with AI greeting
      conversationHistory.value.push({
        sender: 'ai',
        text: props.scenarioData.ai_greeting,
      })
      currentAIResponse.value = props.scenarioData.ai_greeting

      // Start call duration timer
      durationInterval = setInterval(() => {
        callDuration.value += 1
      }, 1000)
    })

    onUnmounted(() => {
      if (durationInterval) clearInterval(durationInterval)
      if (recognition && isListening.value) recognition.stop()
    })

    return {
      userResponse,
      currentAIResponse,
      isProcessing,
      isListening,
      speechSupported,
      error,
      callDuration,
      conversationHistory,
      formatTime,
      toggleListening,
      sendResponse,
      endCall,
    }
  },
}
</script>
