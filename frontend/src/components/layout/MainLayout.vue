<template>
  <div class="main-layout">
    <header class="layout-header">
      <div class="header-content">
        <div class="header-left">
          <img src="@/assets/logo.png" alt="心晴港湾" class="logo">
          <h1 class="app-name">心晴港湾</h1>
        </div>
        
        <div class="header-right">
          <SystemStatus />
          
          <div class="emotion-status">
            <span class="emotion-label">当前情绪:</span>
            <span :class="['emotion-value', `emotion-${currentEmotion.type}`]">
              {{ currentEmotion.label }}
            </span>
            <div :class="['emotion-icon', `emotion-${currentEmotion.type}`]">
              <el-icon v-if="currentEmotion.type === 'positive'">
                <SuccessFilled />
              </el-icon>
              <el-icon v-else-if="currentEmotion.type === 'negative'">
                <WarningFilled />
              </el-icon>
              <el-icon v-else>
                <InfoFilled />
              </el-icon>
            </div>
          </div>
          
          <el-dropdown @command="handleUserCommand" trigger="click">
            <div class="user-menu-trigger">
              <div class="user-avatar">
                {{ userInitial }}
              </div>
              <span class="username">{{ userInfo.username }}</span>
              <el-icon><ArrowDown /></el-icon>
            </div>
            
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="emotion">
                  <el-icon><DataAnalysis /></el-icon>
                  情感分析
                </el-dropdown-item>
                <el-dropdown-item command="knowledge">
                  <el-icon><Reading /></el-icon>
                  知识库
                </el-dropdown-item>
                <el-dropdown-item divided command="emergency">
                  <el-icon style="color: #EF4444;"><Warning /></el-icon>
                  <span style="color: #EF4444;">紧急求助</span>
                </el-dropdown-item>
                <el-dropdown-item command="logout">
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </header>
    
    <main class="layout-main">
      <router-view />
    </main>
    
    <div class="emergency-float-btn" @click="goToEmergency">
      <el-icon><Warning /></el-icon>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useChatStore } from '@/stores/chat'
import { ElMessageBox } from 'element-plus'
import {
  SuccessFilled,
  WarningFilled,
  InfoFilled,
  ArrowDown,
  DataAnalysis,
  Reading,
  Warning,
  SwitchButton
} from '@element-plus/icons-vue'
import SystemStatus from '@/components/system/SystemStatus.vue'

const router = useRouter()
const authStore = useAuthStore()
const chatStore = useChatStore()

const userInfo = computed(() => authStore.user || {})
const userInitial = computed(() => authStore.userInitial)
const currentEmotion = computed(() => chatStore.currentEmotion)

const handleUserCommand = (command) => {
  switch (command) {
    case 'emotion':
      router.push('/emotion')
      break
    case 'knowledge':
      router.push('/knowledge')
      break
    case 'emergency':
      router.push('/emergency')
      break
    case 'logout':
      handleLogout()
      break
  }
}

const goToEmergency = () => {
  router.push('/emergency')
}

const handleLogout = () => {
  ElMessageBox.confirm('确定要退出登录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    authStore.logout()
    router.push('/login')
  })
}
</script>

<style scoped lang="scss">
.main-layout {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.layout-header {
  background: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border-bottom: 1px solid var(--border-color);
  z-index: 1000;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  height: 64px;
  max-width: 1400px;
  margin: 0 auto;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo {
  width: 32px;
  height: 32px;
}

.app-name {
  font-size: 20px;
  font-weight: bold;
  color: var(--text-primary);
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 24px;
}

.emotion-status {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.emotion-label {
  color: var(--text-secondary);
}

.emotion-value {
  font-weight: 500;
  
  &.emotion-positive {
    color: var(--success-color);
  }
  &.emotion-neutral {
    color: var(--primary-color);
  }
  &.emotion-negative {
    color: var(--warning-color);
  }
}

.emotion-icon {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  
  &.emotion-positive {
    color: var(--success-color);
  }
  &.emotion-neutral {
    color: var(--primary-color);
  }
  &.emotion-negative {
    color: var(--warning-color);
  }
}

.user-menu-trigger {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s;
  
  &:hover {
    background-color: var(--bg-gray);
  }
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 14px;
}

.username {
  font-weight: 500;
  color: var(--text-primary);
}

.layout-main {
  flex: 1;
  overflow: hidden;
  background-color: var(--bg-gray);
}

.emergency-float-btn {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, #EF4444, #DC2626);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
  transition: all 0.3s;
  z-index: 1000;
  
  &:hover {
    transform: scale(1.1);
    box-shadow: 0 6px 16px rgba(239, 68, 68, 0.4);
  }
  
  .el-icon {
    font-size: 24px;
  }
}

@media (max-width: 768px) {
  .header-content {
    padding: 0 16px;
  }
  
  .app-name {
    font-size: 18px;
  }
  
  .emotion-status {
    font-size: 12px;
  }
  
  .username {
    display: none;
  }
}
</style>