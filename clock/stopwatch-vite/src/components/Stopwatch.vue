<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const displayRef = ref(null)
const isRunning = ref(false)
const startTime = ref(0)
const elapsed = ref(0)
const rafId = ref(0)
const laps = ref([])
let lapId = 0
let lastLapTime = 0

function formatTime(ms) {
  const totalSeconds = Math.floor(ms / 1000)
  const hours = Math.floor(totalSeconds / 3600)
  const minutes = Math.floor((totalSeconds % 3600) / 60)
  const seconds = totalSeconds % 60
  const milliseconds = ms % 1000
  return `${String(hours).padStart(2,'0')}:${String(minutes).padStart(2,'0')}:${String(seconds).padStart(2,'0')}.${String(milliseconds).padStart(3,'0')}`
}

function update() {
  const now = Date.now()
  elapsed.value = now - startTime.value
  if (displayRef.value) displayRef.value.textContent = formatTime(elapsed.value)
  rafId.value = requestAnimationFrame(update)
}

function start() {
  if (isRunning.value) return
  startTime.value = Date.now() - elapsed.value
  isRunning.value = true
  update()
}

function pause() {
  if (!isRunning.value) return
  cancelAnimationFrame(rafId.value)
  isRunning.value = false
}

function lap() {
  if (!isRunning.value) return
  const currentTime = Date.now() - startTime.value
  const lapTime = currentTime - lastLapTime
  laps.value.push({ id: lapId++, lapTime, totalTime: currentTime })
  lastLapTime = currentTime
}

function reset() {
  cancelAnimationFrame(rafId.value)
  isRunning.value = false
  elapsed.value = 0
  startTime.value = 0
  lastLapTime = 0
  laps.value = []
  if (displayRef.value) displayRef.value.textContent = formatTime(0)
}

onMounted(() => {
  if (displayRef.value) displayRef.value.textContent = formatTime(0)
})

onBeforeUnmount(() => {
  cancelAnimationFrame(rafId.value)
})
</script>

<template>
  <div class="wrap">
    <div ref="displayRef" class="display">00:00:00.000</div>
    <div class="controls">
      <button @click="start" :disabled="isRunning">开始</button>
      <button @click="pause" :disabled="!isRunning">暂停</button>
      <button @click="lap" :disabled="!isRunning">记圈</button>
      <button @click="reset">重置</button>
    </div>
    <ul class="laps">
      <li v-for="l in laps" :key="l.id">{{ formatTime(l.totalTime) }}</li>
    </ul>
  </div>
</template>

<style scoped>
.wrap {
  display: grid;
  place-items: center;
  gap: 1rem;
}
.display {
  font: 700 15vmin/1 monospace;
  letter-spacing: 0.05em;
}
.controls {
  display: flex;
  gap: 0.5rem;
}
button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  border: 1px solid #333;
  background: white;
  cursor: pointer;
}
button:disabled { opacity: .5; cursor: not-allowed }
.laps {
  max-height: 200px;
  overflow-y: auto;
  list-style: none;
  padding: 0;
  margin: 0;
}
.laps li { padding: .25rem 0; border-bottom: 1px solid #eee }
</style>

