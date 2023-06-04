<template>
<div
        class="container mx-auto mt-5 text-center">
        <span class="text-3xl align-middle">Войти</span>
        
        <div>
            <form
                class="space-y-6 mt-5 w-1/2 mx-auto text-left"
                v-on:submit.prevent="submitForm">

                <div>
                    <label class="text-xl">Имя</label>
                    <input type="text" v-model="form.name" placeholder="Введите имя"
                        class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                </div>

                <div>

                    <label class="text-xl">Пароль</label>
                    <button
                            style="margin-left: 80%;"
                            type="button">
                        <svg
                        v-if="input_type === 'text'"
                        @click="input_type = 'password'"
                        xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
                            <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        </svg>
                        <svg
                            v-else
                            @click="input_type = 'text'"
                            xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
                        </svg>
                    </button>
                    <div
                        class="items-center">
                    <input :type="input_type" v-model="form.password" placeholder="Введите пароль"
                        class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                </div>

                <template v-if="errors.length > 0">
                    <div class="bg-red-500 text-white rounded-lg p-6" v-for="error in errors" v-bind:key="error">
                        <p>{{ error }}</p>
                    </div>
                </template>

                <div>
                    <button
                            class="w-full
                            py-4 px-6 bg-purple-600 text-white rounded-lg">
                        Отправить    
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'

export default {
    name: 'login',

    setup() {
        const userStore = useUserStore()
        const toastStore = useToastStore()

        return {
            userStore,
            toastStore
        }
    },

    data() {
        return {
            form: {
                name: '',
                password: ''
            },
            errors: [],
            input_type: 'password'
        }
    },

    methods: {
        async submitForm() {
            this.errors = []

            if (this.form.name === '') {
                this.errors.push('Вы забыли ввести имя')
            }

            if (this.form.password === '') {
                this.errors.push('Вы забыли ввести пароль')
            }

            if (this.errors.length === 0) {
                await axios
                            .post('/user/login/', this.form)
                            .then(response => {
                                this.userStore.setToken(response.data)

                                axios.defaults.headers.common['Authorization'] = 'Bearer ' + response.data.access
                            })
                            .catch(error => {
                                console.log('error', error.response.data.detail)
                                this.errors.push('Имя или пароль неверные! Или пользователя не существует.')                            
                            })
                if (this.errors.length === 0) {
                    axios
                        .get('/user/me/')
                        .then(response => {
                            this.userStore.setUserInfo(response.data)
                            this.toastStore.showToast(5000, 'Добро пожаловать!', 'bg-emerald-500 text-white')

                            this.$router.push('/')
                        })
                        .catch(error => {
                            console.log('error', error)
                        })
                }
            }
            
        },
    }
    
}
</script>