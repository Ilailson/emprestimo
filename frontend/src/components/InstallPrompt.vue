<template>
  <div v-if="showPrompt" class="fixed bottom-4 left-4 right-4 md:left-auto md:right-4 md:w-96 bg-slate-800 border border-slate-700 rounded-xl p-4 shadow-2xl z-50">
    <div class="flex items-start gap-3">
      <div class="w-12 h-12 rounded-xl bg-emerald-500/20 flex items-center justify-center flex-shrink-0">
        <svg class="w-6 h-6 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"/>
        </svg>
      </div>
      <div class="flex-1">
        <h3 class="text-white font-semibold">Instalar Aplicativo</h3>
        <p class="text-slate-400 text-sm mt-1">Instale este app para uma melhor experiência</p>
        <div class="flex gap-2 mt-3">
          <button @click="install" class="flex-1 px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-sm font-medium transition-all">
            Instalar
          </button>
          <button @click="dismiss" class="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-slate-300 rounded-lg text-sm font-medium transition-all">
            Agora não
          </button>
        </div>
      </div>
      <button @click="dismiss" class="text-slate-500 hover:text-white p-1 -mt-1 -mr-1">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'InstallPrompt',
  data() {
    return {
      showPrompt: false,
      deferredPrompt: null
    }
  },
  mounted() {
    window.addEventListener('beforeinstallprompt', this.handleBeforeInstallPrompt)
  },
  beforeUnmount() {
    window.removeEventListener('beforeinstallprompt', this.handleBeforeInstallPrompt)
  },
  methods: {
    handleBeforeInstallPrompt(e) {
      e.preventDefault()
      this.deferredPrompt = e
      this.showPrompt = true
    },
    async install() {
      if (!this.deferredPrompt) return
      this.deferredPrompt.prompt()
      const { outcome } = await this.deferredPrompt.userChoice
      if (outcome === 'accepted') {
        console.log('PWA instalado')
      }
      this.deferredPrompt = null
      this.showPrompt = false
    },
    dismiss() {
      this.showPrompt = false
      this.deferredPrompt = null
    }
  }
}
</script>
