import { defineStore } from "pinia";
import axios from "axios";

export const useUserStore = defineStore({
    id: 'user',

    state: () => ({
        user: {
            isAuthenticated: false,
            id: null,
            name: null,
            access: null,
            refresh: null,
            photo: null,
            answered: []
        }
    }),

    actions: {
        initStore() {
            console.log('InitStore', this.user.isAuthenticated)

            if (localStorage.getItem('user.access')) {
                console.log('User has Access!')
                this.user.access = localStorage.getItem('user.access')
                this.user.refresh = localStorage.getItem('user.refresh')
                this.user.id = localStorage.getItem('user.id')
                this.user.name = localStorage.getItem('user.name')
                this.user.photo = localStorage.getItem('user.photo')
                this.user.answered = JSON.parse(localStorage.getItem('user.answered'))
                this.user.isAuthenticated = true

                this.refreshToken()

                console.log('Initialized user:', this.user)
            }
        },

        setToken(data) {
            console.log('setToken', data)

            this.user.access = data.access
            this.user.refresh = data.refresh
            this.user.isAuthenticated = true

            localStorage.setItem('user.access', data.access)
            localStorage.setItem('user.refresh', data.refresh)
        },

        removeToken() {
            console.log('removeToken')

            this.user.refresh = null
            this.user.access = null
            this.user.isAuthenticated = false
            this.user.id = null
            this.user.name = null
            this.user.photo = null
            this.user.answered = []

            localStorage.setItem('user.access', '')
            localStorage.setItem('user.refresh', '')
            localStorage.setItem('user.id', '')
            localStorage.setItem('user.name', '')
            localStorage.setItem('user.photo', '')
            localStorage.setItem('user.answered', [])

        },

        setUserInfo(user) {
            console.log('setUserInfo', user)

            this.user.id = user.id
            this.user.name = user.name
            this.user.photo = user.photo
            this.user.answered = user.answered

            localStorage.setItem('user.id', this.user.id)
            localStorage.setItem('user.name', this.user.name)
            localStorage.setItem('user.photo', this.user.photo)
            localStorage.setItem('user.answered', JSON.stringify(this.user.answered))
        },

        refreshToken() {
            axios.post('/user/refresh/', {
                refresh: this.user.refresh
            })
                .then((response) => {
                    this.user.access = response.data.access

                    localStorage.setItem('user.access', response.data.access)

                    axios.defaults.headers.common['Authorization'] = 'Bearer ' + response.data.access
                })
                .catch((error) => {
                    console.log(error)

                    this.removeToken()
                })
        },
    }
})