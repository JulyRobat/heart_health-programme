import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const token = ref('')
  const userInfo = ref({})
  const isLoggedIn = ref(false)

  const login = (userData) => {
    userInfo.value = userData
    isLoggedIn.value = true
    token.value = 'mock-jwt-token'
    
    // 保存到本地存储
    uni.setStorageSync('userInfo', userData)
    uni.setStorageSync('token', token.value)
  }

  const logout = () => {
    token.value = ''
    userInfo.value = {}
    isLoggedIn.value = false
    
    // 清除本地存储
    uni.removeStorageSync('userInfo')
    uni.removeStorageSync('token')
  }

  const checkAuth = () => {
    const storedUserInfo = uni.getStorageSync('userInfo')
    const storedToken = uni.getStorageSync('token')
    
    if (storedUserInfo && storedToken) {
      userInfo.value = storedUserInfo
      token.value = storedToken
      isLoggedIn.value = true
      return true
    }
    return false
  }

  return {
    token,
    userInfo,
    isLoggedIn,
    login,
    logout,
    checkAuth
  }
})