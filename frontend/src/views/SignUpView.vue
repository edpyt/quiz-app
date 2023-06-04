<template>
    <div
        class="container mx-auto mt-5 text-center">
        <span class="text-3xl align-middle">Регистрация</span>
        
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
                    <input type="password" v-model="form.password1" placeholder="Введите пароль"
                        class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                </div>

                <div>
                    <label class="text-xl">Повтор пароля</label>
                    <input type="password" v-model="form.password2" placeholder="Повторите пароль"
                        class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
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
import { useToastStore } from '@/stores/toast'

export default {
    name: 'signup',

    setup() {
        const toastStore = useToastStore()

        return {
            toastStore
        }
    },

    data() {
        return {
            form: {
                name: '',
                password1: '',
                password2: '',
            },
            errors: []
        }
    },

    methods: {
        submitForm() {
            this.errors = []
            if (this.form.name === '') {
                this.errors.push('Вы забыли ввести имя')
            }

            if (this.form.password1 === '') {
                this.errors.push('Вы забыли ввести пароль')
            }

            if (this.form.password1 !== this.form.password2) {
                this.errors.push('Пароли не совпадают')
            }

            if (this.errors.length === 0) {
                axios
                    .post('/user/signup/', this.form)
                    .then(response => {
                        console.log(response.data)

                        if (response.data.message === 'success') {
                            this.toastStore.showToast(5000, 'Пользователь был успешно зарегистрирован', 'bg-emerald-500')

                            this.form.name = ''
                            this.form.password1 = ''
                            this.form.password2 = ''
                        } else {
                            this.toastStore.showToast(5000, response.data.message, 'bg-red-300')
                        }
                    })
                    .catch(error => {
                        this.toastStore.showToast(5000, 'Something went wrong. Please try again', 'bg-red-300')
                    })
            }

            console.log(this.errors)
        }
    }
}
</script>