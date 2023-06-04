<template>
  <div
      class="container mx-auto rounded mt-5 p-5
      text-white w-[60rem]
      bg-gradient-to-r from-indigo-300 to-purple-400"
      v-for="quiz in quiz_list"
  >

    <div
      class="text-4xl text-center">
      {{ quiz.question }}

    </div>
    <div
        class="mt-5"
        style="text-align: center;"
    >

      <form
            v-on:submit.prevent="submitForm(quiz)"
            v-if="userStore.user.answered.includes(quiz.id) === false"
      >

        <div
            class="mx-auto bg-red-500 m-5 flex items-center justify-center rounded"
            style="height: 45px;"
            v-if="quiz.choiceIsWrong">
          <span class="text-xl font-bold m-auto">
            Не правильно!
          </span>
        </div>

        <input
          type="button"
          class="w-3/4 cursor-pointer text-sm
          text-gray-900 bg-white border border-gray-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-200 font-medium rounded-lg px-5 py-2.5 mr-2 mb-2 dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700"
          v-for="answer in quiz.quiz_answers"
          @click="form.answer_id=answer.id;"
          :value="answer.answer"    
        />

        <button
          v-if="userStore.user.isAuthenticated"
          class="w-3/4 text-2xl
          text-white bg-gray-800 hover:bg-gray-900 font-medium rounded-lg px-5 py-2.5 mr-2 mb-2 dark:bg-gray-800 dark:hover:bg-gray-700 dark:focus:ring-gray-700 dark:border-gray-700"
          type="submit">
              Отправить
        </button>

      </form>

      <div
          v-else
          class="bg-emerald-400 flex items-center justify-center rounded"
          style="height: 50px;"
      >
        <span class="text-2xl font-bold m-auto">
          Отвечено!
        </span>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios';
import { useToastStore } from '@/stores/toast'
import { useUserStore } from '@/stores/user';

export default {
  name: 'home',

  setup() {
    const toastStore = useToastStore()
    const userStore = useUserStore()


    return {
        toastStore,
        userStore
    }
  },

  data() {
    return {
      quiz_list: [],
      form: {
        answer_id: ''
      },
    }
  },
  
  mounted() {
    this.getQuizList()
  },
  
  methods: {
    async getQuizList() {
      await axios.get('/quiz/all')
                 .then(response => {
                  console.log('Quiz', response.data)
                  for (const quiz_id in response.data) {
                    response.data[quiz_id]['choiceIsWrong'] = false
                  }
                  this.quiz_list = response.data
                 })
                 .catch(error => {
                  console.log(error)
                 })
    },
    submitForm(quiz) {
      console.log(this.form)

      quiz.choiceIsWrong = false

      axios
            .post('/quiz/quiz_answer/', this.form)
            .then(response => {
              if (response.data.message === 'Correct') {
                this.userStore.user.answered.push(quiz.id)
                localStorage.setItem('user.answered', JSON.stringify(this.userStore.user.answered))
                quiz.choiceIsWrong = false
              } else {
                quiz.choiceIsWrong = true
              }
              this.form.answer_id = ''
            })
            .catch(error => {
              console.log(error)
              this.toastStore.showToast(5000, 'Что-то пошло не так! Попробуйте ещё раз.', 'bg-red-300')
            })
    },
  }

}
</script>