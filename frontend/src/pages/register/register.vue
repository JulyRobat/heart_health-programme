<template>
  <view class="register-container">
    <view class="register-header">
      <text class="title">用户注册</text>
      <text class="subtitle">心晴港湾 - 基于AI情感计算的心理健康支持系统</text>
    </view>
    
    <view class="register-form">
      <view class="form-item">
        <text class="label">学号</text>
        <input v-model="registerForm.student_id" class="input" placeholder="请输入学号" />
      </view>
      
      <view class="form-item">
        <text class="label">姓名</text>
        <input v-model="registerForm.username" class="input" placeholder="请输入真实姓名" />
      </view>
      
      <view class="form-item">
        <text class="label">密码</text>
        <input v-model="registerForm.password" class="input" password placeholder="请输入密码" />
      </view>
      
      <view class="form-item">
        <text class="label">确认密码</text>
        <input v-model="registerForm.confirmPassword" class="input" password placeholder="请再次输入密码" />
      </view>
      
      <view class="form-item">
        <text class="label">紧急联系人电话</text>
        <input v-model="registerForm.emergency_contact" class="input" placeholder="请输入紧急联系人电话" />
      </view>
      
      <button class="register-btn" @click="handleRegister" :disabled="loading">
        {{ loading ? '注册中...' : '注册' }}
      </button>
      
      <view class="login-link">
        <text>已有账号？</text>
        <text class="link" @click="navigateToLogin">立即登录</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'

const loading = ref(false)
const registerForm = ref({
  student_id: '',
  username: '',
  password: '',
  confirmPassword: '',
  emergency_contact: ''
})

const handleRegister = () => {
  if (!registerForm.value.student_id || !registerForm.value.username || 
      !registerForm.value.password || !registerForm.value.confirmPassword) {
    uni.showToast({
      title: '请填写完整信息',
      icon: 'none'
    })
    return
  }

  if (registerForm.value.password !== registerForm.value.confirmPassword) {
    uni.showToast({
      title: '两次密码输入不一致',
      icon: 'none'
    })
    return
  }

  loading.value = true
  
  // 模拟注册成功
  setTimeout(() => {
    loading.value = false
    uni.showToast({
      title: '注册成功',
      icon: 'success'
    })
    
    // 跳转到登录页面
    setTimeout(() => {
      uni.navigateBack()
    }, 1500)
  }, 1000)
}

const navigateToLogin = () => {
  uni.navigateBack()
}
</script>

<style scoped>
.register-container {
  padding: 60rpx 40rpx;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.register-header {
  text-align: center;
  margin-bottom: 60rpx;
}

.title {
  display: block;
  font-size: 40rpx;
  font-weight: bold;
  color: white;
  margin-bottom: 15rpx;
}

.subtitle {
  display: block;
  font-size: 26rpx;
  color: rgba(255, 255, 255, 0.8);
}

.register-form {
  background: white;
  border-radius: 20rpx;
  padding: 60rpx 40rpx;
}

.form-item {
  margin-bottom: 35rpx;
}

.label {
  display: block;
  font-size: 28rpx;
  color: #333;
  margin-bottom: 18rpx;
}

.input {
  border: 2rpx solid #e0e0e0;
  border-radius: 12rpx;
  padding: 22rpx;
  font-size: 28rpx;
}

.register-btn {
  background: #667eea;
  color: white;
  border: none;
  border-radius: 12rpx;
  padding: 24rpx;
  font-size: 32rpx;
  margin-top: 50rpx;
}

.register-btn:disabled {
  background: #cccccc;
}

.login-link {
  text-align: center;
  margin-top: 40rpx;
  font-size: 26rpx;
  color: #666;
}

.link {
  color: #667eea;
  margin-left: 10rpx;
}
</style>