<template>
    Выходим...
</template>

<script>
import { useToastStore } from '@/stores/toast'
import { useUserStore } from '@/stores/user';

export default {
    setup() {
        const toastStore = useToastStore()
        const userStore = useUserStore()


        return {
            toastStore,
            userStore
        }
  },
  
  mounted() {
    this.userLogout()
  },

  methods: {
    userLogout() {
        this.userStore.removeToken()
        
        this.toastStore.showToast(5000, 'Всего доброго! :)', 'bg-yellow-300 text-white')

        this.$router.push('/login')
    }
  }
}
</script>