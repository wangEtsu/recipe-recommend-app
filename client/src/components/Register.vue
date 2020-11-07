<template>
  <div>
    <!-- two way binding, reactivity, v-model -->
    <h1>{{ msg }}</h1>
    <input type="email" name="email" v-model="email" placeholder="Enter your email here" />
    <br />
    <input type="password" name="password" v-model="password" placeholder="Enter your password here" />
    <br />
    <button @click="register">Register!</button>
  </div>
</template>

<script>
import AuthenticationService from '@/services/AuthenticationService'
export default {
  data() {
    return {
      msg: "Welcome to Recipee!",
      email: "assd",
      password: ""
    };
  },
//   monitor any value changes in email and password
  watch: {
    email (value) {
        console.log("Email Changed");
    }
  },
  methods: {
    async register () {
        console.log("Register button is clicked");
        const response = await AuthenticationService.register({
            email: this.email,
            password: this.password
        })
        console.log(response.data);
    }
  },
  mounted () {
  }


};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
