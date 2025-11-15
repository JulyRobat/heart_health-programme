<template>
  <view class="login-container">
    <view class="login-header">
      <text class="title">心晴港湾</text>
      <text class="subtitle">基于AI情感计算的心理健康支持系统</text>
    </view>
    
    <view class="login-form">
      <view class="form-item">
        <text class="label">学号</text>
        <input 
          v-model="loginForm.student_id" 
          class="input" 
          placeholder="请输入学号"
          type="text"
        />
      </view>
      
      <view class="form-item">
        <text class="label">密码</text>
        <input 
          v-model="loginForm.password" 
          class="input" 
          placeholder="请输入密码"
          password
        />
      </view>
      
      <button class="login-btn" @click="handleLogin" :disabled="loading">
        {{ loading ? '登录中...' : '登录' }}
      </button>
      
      <view class="register-link">
        <text>还没有账号？</text>
        <text class="link" @click="navigateToRegister">立即注册</text>
      </view>

      <view class="test-accounts">
        <text class="test-title">测试账号：</text>
        <text class="test-account">管理员：admin / admin123</text>
        <text class="test-account">学生：20210001 / 123456</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const loading = ref(false)

const loginForm = ref({
  student_id: '',
  password: ''
})

const handleLogin = async () => {
  if (!loginForm.value.student_id || !loginForm.value.password) {
    uni.showToast({
      title: '请填写完整信息',
      icon: 'none'
    })
    return
  }

  loading.value = true
  try {
    // 模拟登录逻辑
    if (loginForm.value.student_id === 'admin' && loginForm.value.password === 'admin123') {
      // 管理员登录
      authStore.userInfo = {
        id: 1,
        student_id: 'admin',
        username: '系统管理员',
        role: 'admin'
      }
      authStore.isLoggedIn = true
      uni.reLaunch({ url: '/pages/admin/dashboard' })
    } else if (loginForm.value.student_id === '20210001' && loginForm.value.password === '123456') {
      // 学生登录
      authStore.userInfo = {
        id: 2,
        student_id: '20210001',
        username: '测试学生',
        role: 'student',
        emergency_contact: '13800138000'
      }
      authStore.isLoggedIn = true
      uni.reLaunch({ url: '/pages/index/index' })
    } else {
      throw new Error('学号或密码错误')
    }
    
    uni.showToast({
      title: '登录成功',
      icon: 'success'
    })
  } catch (error) {
    uni.showToast({
      title: error.message || '登录失败',
      icon: 'none'
    })
  } finally {
    loading.value = false
  }
}

const navigateToRegister = () => {
  uni.navigateTo({ url: '/pages/register/register' })
}
</script>

<style scoped>
.login-container {
  padding: 60rpx 40rpx;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-header {
  text-align: center;
  margin-bottom: 80rpx;
}

.title {
  display: block;
  font-size: 48rpx;
  font-weight: bold;
  color: white;
  margin-bottom: 20rpx;
}

.subtitle {
  display: block;
  font-size: 28rpx;
  color: rgba(255, 255, 255, 0.8);
}

.login-form {
  background: white;
  border-radius: 20rpx;
  padding: 60rpx 40rpx;
}

.form-item {
  margin-bottom: 40rpx;
}

.label {
  display: block;
  font-size: 28rpx;
  color: #333;
  margin-bottom: 20rpx;
}

.input {
  border: 2rpx solid #e0e0e0;
  border-radius: 12rpx;
  padding: 24rpx;
  font-size: 28rpx;
}

.login-btn {
  background: #667eea;
  color: white;
  border: none;
  border-radius: 12rpx;
  padding: 24rpx;
  font-size: 32rpx;
  margin-top: 40rpx;
}

.login-btn:disabled {
  background: #cccccc;
}

.register-link {
  text-align: center;
  margin-top: 40rpx;
  font-size: 26rpx;
  color: #666;
}

.link {
  color: #667eea;
  margin-left: 10rpx;
}

.test-accounts {
  margin-top: 40rpx;
  padding: 30rpx;
  background: #f8f9fa;
  border-radius: 12rpx;
}

.test-title {
  display: block;
  font-size: 26rpx;
  color: #666;
  margin-bottom: 15rpx;
  font-weight: bold;
}

.test-account {
  display: block;
  font-size: 24rpx;
  color: #888;
  margin-bottom: 8rpx;
}
</style>