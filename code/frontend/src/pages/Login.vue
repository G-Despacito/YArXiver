<template>
  <v-row>
    <v-col>
      <v-expand-transition>
        <v-alert v-show="alert_user_non_exist" type="error" closable="true">
          Login failed! Username not exists!
        </v-alert>
      </v-expand-transition>
      <v-expand-transition>
        <v-alert v-show="alert_pwd_err" type="error" closable="true">
          Login failed! Password error!
        </v-alert>
      </v-expand-transition>
    </v-col>
  </v-row>
  <v-row>
    <v-col>
      <div class="auth-wrapper d-flex align-center justify-center pa-4">
        <v-card class="auth-card pa-4 pt-7" max-width="448">
          <v-card-item class="justify-center">
            <template #prepend>
              <div class="d-flex">
                <img src="../images/logo.png" class="logo" />
              </div>
            </template>

          </v-card-item>

          <v-card-text class="pt-2">
            <h5 class="text-h5 font-weight-semibold mb-1">
              Welcome to YarXiver! 😆
            </h5>
            <p class="mb-0">
              Please sign-in to your account and start the journey
            </p>
          </v-card-text>

          <v-card-text>
            <v-form @submit.prevent="() => { }">
              <v-row>
                <!-- email -->
                <v-col cols="12">
                  <v-text-field v-model="form.username" name="login" label="Email" type="email" />
                </v-col>

                <!-- password -->
                <v-col cols="12">
                  <v-text-field id="password" v-model="form.password" name="password" label="Password"
                    :type="isPasswordVisible ? 'text' : 'password'"
                    :append-inner-icon="isPasswordVisible ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
                    @click:append-inner="isPasswordVisible = !isPasswordVisible" />

                  <!-- login button -->
                  <v-btn block color="primary" type="submit" @click="login">
                    Login
                  </v-btn>
                </v-col>

                <!-- create account -->
                <v-col cols="12" class="text-center text-base">
                  <span>New on our platform?</span>
                  <a class="text-primary ms-2" href="/#/register">
                    Create an account
                  </a>
                </v-col>

                <v-col cols="12" class="d-flex align-center">
                </v-col>
              </v-row>
            </v-form>
          </v-card-text>
        </v-card>
      </div>
    </v-col>
  </v-row>
</template>


<script>
import axios from "axios";

export default {
  name: "Login",
  data() {
    return {
      form: {
        username: "",
        password: "",
        remember: false,
      },
      isPasswordVisible: false,
      alert_user_non_exist: false,
      alert_pwd_err: false,
    };
  },
  methods: {
    login() {
      this.alert_user_non_exist = false;
      this.alert_pwd_err = false;
      console.log("start login");
      const payload = {
        username: this.form.username,
        password: this.form.password,
      };
      console.log(payload);
      axios.post("login", payload).then((res) => {
        console.log(res.data);
        const code = res.data.code;
        const status = res.data.status;
        console.log(code);
        if (code == 400) {
            if (status === "Username doesn't exist!") {
              console.log(status);
              this.alert_user_non_exist = true;
            }
            if (status === "Password error!") {
              console.log(status);
              this.alert_pwd_err = true;
            }
        }
        else {
            this.$router.go();
            // this.$router.push("library");
        }
      });
    },
  },
};
</script>


<style>

</style>

