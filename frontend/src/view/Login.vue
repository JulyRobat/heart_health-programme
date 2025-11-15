<template>
  <div class="login-container">
    <div class="login-card">
      <!-- Logo 区域 -->
      <div class="logo-section">
        <div class="logo">😊</div>
        <h2 class="app-name">心晴港湾</h2>
        <p class="app-desc">基于AI情感计算的心理健康支持系统</p>
      </div>
      
      <!-- 标签页 -->
      <el-tabs v-model="activeTab" class="login-tabs" stretch>
        <!-- 登录标签 -->
        <el-tab-pane name="login">
          <template #label>
            <span class="tab-label">登录</span>
          </template>
          
          <el-form
            ref="loginFormRef"
            :model="loginForm"
            :rules="loginRules"
            class="login-form"
          >
            <el-form-item prop="studentId">
              <el-input
                v-model="loginForm.studentId"
                placeholder="请输入学号"
                size="large"
                :prefix-icon="User"
              />
            </el-form-item>
            
            <el-form-item prop="password">
              <el-input
                v-model="loginForm.password"
                type="password"
                placeholder="请输入密码"
                size="large"
                :prefix-icon="Lock"
                show-password
              />
            </el-form-item>
            
            <el-form-item>
              <el-button
                type="primary"
                size="large"
                :loading="loading"
                @click="handleLogin"
                class="login-btn"
              >
                登录
              </el-button>
            </el-form-item>
            
            <div class="form-footer">
              <el-link type="primary" :underline="false">
                忘记密码?
              </el-link>
            </div>
          </el-form>
        </el-tab-pane>
        
        <!-- 注册标签 -->
        <el-tab-pane name="register">
          <template #label>
            <span class="tab-label">注册</span>
          </template>
          
          <el-form
            ref="registerFormRef"
            :model="registerForm"
            :rules="registerRules"
            class="register-form"
          >
            <el-form-item prop="studentId">
              <el-input
                v-model="registerForm.studentId"
                placeholder="请输入学号"
                size="large"
                :prefix-icon="User"
              />
            </el-form-item>
            
            <el-form-item prop="username">
              <el-input
                v-model="registerForm.username"
                placeholder="请输入用户名"
                size="large"
                :prefix-icon="User"
              />
            </el-form-item>
            
            <el-form-item prop="password">
              <el-input
                v-model="registerForm.password"
                type="password"
                placeholder="请设置密码"
                size="large"
                :prefix-icon="Lock"
                show-password
              />
            </el-form-item>
            
            <el-form-item prop="emergencyContact">
              <el-input
                v-model="registerForm.emergencyContact"
                placeholder="请输入紧急联系人电话"
                size="large"
                :prefix-icon="Phone"
              />
            </el-form-item>
            
            <el-form-item>
              <el-button
                type="success"
                size="large"
                :loading="loading"
                @click="handleRegister"
                class="register-btn"
              >
                注册
              </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, Phone } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const activeTab = ref('login')
const loading = ref(false)

const loginFormRef = ref()
const registerFormRef = ref()

const loginForm = reactive({
  studentId: '',
  password: ''
})

const registerForm = reactive({
  studentId: '',
  username: '',
  password: '',
  emergencyContact: ''
})

// 验证规则
const loginRules = {
  studentId: [
    { required: true, message: '请输入学号', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ]
}

const registerRules = {
  studentId: [
    { required: true, message: '请输入学号', trigger: 'blur' }
  ],
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请设置密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ]
}

// 登录处理
const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    await loginFormRef.value.validate()
    loading.value = true
    
    const result = await authStore.login(loginForm)
    
    if (result.success) {
      ElMessage.success('登录成功')
      router.push('/chat')
    } else {
      ElMessage.error(result.message)
    }
  } catch (error) {
    // 验证失败
  } finally {
    loading.value = false
  }
}

// 注册处理
const handleRegister = async () => {
  if (!registerFormRef.value) return
  
  try {
    await registerFormRef.value.validate()
    loading.value = true
    
    const result = await authStore.register(registerForm)
    
    if (result.success) {
      ElMessage.success('注册成功，请登录')
      activeTab.value = 'login'
      registerFormRef.value.resetFields()
    } else {
      ElMessage.error(result.message)
    }
  } catch (error) {
    // 验证失败
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.login-container {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 440px;
  background: white;
  border-radius: 16px;
  padding: 48px 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
}

.logo-section {
  text-align: center;
  margin-bottom: 40px;
}

.logo {
  font-size: 48px;
  margin-bottom: 16px;
}

.app-name {
  font-size: 28px;
  font-weight: bold;
  color: var(--text-primary);
  margin: 0 0 8px 0;
}

.app-desc {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
}

.login-tabs {
  :deep(.el-tabs__header) {
    margin-bottom: 32px;
  }
  
  :deep(.el-tabs__nav-wrap::after) {
    height: 1px;
  }
  
  :deep(.el-tabs__active-bar) {
    background: var(--primary-color);
  }
  
  :deep(.el-tabs__item) {
    font-size: 16px;
    font-weight: 500;
    
    &.is-active {
      color: var(--primary-color);
    }
  }
}

.tab-label {
  padding: 0 8px;
}

.login-form,
.register-form {
  .el-form-item {
    margin-bottom: 24px;
  }
}

.login-btn,
.register-btn {
  width: 100%;
  margin-top: 8px;
}

.form-footer {
  text-align: center;
  margin-top: 16px;
}
</style>