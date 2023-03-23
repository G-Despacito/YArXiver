<template>
    <v-row>
    <v-col>
      <v-expand-transition>
        <v-alert v-show="alert" type="error" closable="true">
          Sign up failed! Username exists!
        </v-alert>
      </v-expand-transition>
    </v-col>
  </v-row>
  <v-row>
    <v-col>
    <div class="auth-wrapper d-flex align-center justify-center pa-4">
      <v-card
        class="auth-card pa-4 pt-7"
        max-width="448"
      >
      <v-card-item class="justify-center">
        <template #prepend>
            <div class="d-flex">
              <img
                src="../images/logo.jpg"
                class="logo"
              />
            </div>
        </template>

      </v-card-item>
  
        <v-card-text class="pt-2">
          <h5 class="text-h5 font-weight-semibold mb-1">
            Journey starts here 😀
          </h5>
          <p class="mb-0">
            Make your paper management easy and fun!
          </p>
        </v-card-text>
  
        <v-card-text>
          <v-form @submit.prevent="() => {}">
            <v-row>
              <!-- email -->
              <v-col cols="12">
                <v-text-field
                  v-model="form.username"
                  name="login"
                  label="Email"
                  type="email"
                />
              </v-col>
  
              <!-- password -->
              <v-col cols="12">
                <v-text-field
                  id="password"
                  v-model="form.password"
                  name="password"
                  label="Password"
                  :type="isPasswordVisible ? 'text' : 'password'"
                  :append-inner-icon="isPasswordVisible ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
                  @click:append-inner="isPasswordVisible = !isPasswordVisible"
                />
  
                <!-- login button -->
                <v-btn
                  block
                  color="primary"
                  type="submit"
                  @click="signUp"
                >
                    Sign up
                </v-btn>
              </v-col>
  
              <!-- login instead -->
              <v-col
                cols="12"
                class="text-center text-base"
              >
                <span>Already have an account?</span>
                <a
                  class="text-primary ms-2"
                  href="/#/login"
                >
                    Sign in instead
                </a>
              </v-col>
              
              <v-col
                cols="12"
                class="d-flex align-center"
              >
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
      name: "Register",
      data() {
          return {
              form: {
                  username: "",
                  password: "",
              },
              alert: false,
              isPasswordVisible: false,
          };
      },
      methods: {
          signUp() {
              const payload = {
                  username: this.form.username,
                  password: this.form.password,
              };
              axios.post("signup", payload).then((res) => {
                  const code = res.data.success;
                  console.log(code);
                  if (code == 1) {
                      this.alert = true;
                  }
                  else {
                    this.$router.push("library");
                      // this.$router.push("library");
                  }
              });
          },
      },
  };
  </script>
  
  
  <style>
  
  </style>
  
  