<template>
  <view class="container">
    <view class="header">
      <text class="welcome">你好，{{ userInfo.username }}！</text>
      <text class="subtitle">今天心情如何？</text>
      <text class="date">{{ currentDate }}</text>
    </view>
    
    <view class="quick-actions">
      <view class="action-item" @click="navigateTo('chat')">
        <view class="action-icon">💬</view>
        <text class="action-text">AI心理对话</text>
      </view>
      <view class="action-item" @click="navigateTo('emotion')">
        <view class="action-icon">📊</view>
        <text class="action-text">情感分析</text>
      </view>
      <view class="action-item" @click="navigateTo('knowledge')">
        <view class="action-icon">📚</view>
        <text class="action-text">知识库</text>
      </view>
      <view class="action-item" @click="navigateTo('emergency')">
        <view class="action-icon">🆘</view>
        <text class="action-text">紧急求助</text>
      </view>
    </view>
    
    <view class="mood-tracker">
      <view class="section-title">
        <text>今日情绪记录</text>
        <text class="see-more" @click="navigateTo('emotion')">详细分析</text>
      </view>
      <view class="mood-content">
        <view class="mood-score">
          <text class="score">{{ currentMood.score || '--' }}</text>
          <text class="score-label">情绪指数</text>
        </view>
        <view class="mood-description">
          <text class="mood-text">{{ currentMood.description || '暂无记录' }}</text>
          <text class="mood-time">{{ currentMood.time || '' }}</text>
        </view>
      </view>
    </view>
    
    <view class="recent-chats">
      <view class="section-title">
        <text>最近对话</text>
        <text class="see-all" @click="navigateTo('chat')">查看全部</text>
      </view>
      <view class="chat-list">
        <view v-for="chat in recentChats" :key="chat.id" class="chat-item" @click="navigateTo('chat')">
          <view class="chat-avatar">AI</view>
          <view class="chat-content">
            <text class="chat-preview">{{ chat.content }}</text>
            <text class="chat-time">{{ formatTime(chat.created_at) }}</text>
          </view>
        </view>
        <view v-if="recentChats.length === 0" class="empty-state">
          <text>还没有对话记录，开始与AI心理助手聊天吧</text>
        </view>
      </view>
    </view>
    
    <view class="daily-tip">
      <view class="tip-header">
        <text class="tip-icon">💡</text>
        <text class="tip-title">每日心理小贴士</text>
      </view>
      <text class="tip-content">保持规律作息和适度运动有助于缓解压力，提升心理健康水平。</text>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const userInfo = authStore.userInfo
const recentChats = ref([])

const currentDate = computed(() => {
  return new Date().toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  })
})

const currentMood = ref({
  score: 7.2,
  description: '情绪稳定，状态良好',
  time: '今日 14:30'
})

const navigateTo = (page) => {
  const pages = {
    chat: '/pages/chat/chat',
    emotion: '/pages/emotion/emotion',
    knowledge: '/pages/knowledge/knowledge',
    emergency: '/pages/emergency/emergency'
  }
  uni.navigateTo({ url: pages[page] })
}

const formatTime = (timeStr) => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  return `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
}

const loadRecentChats = () => {
  // 模拟数据
  recentChats.value = [
    {
      id: 1,
      content: '最近感觉压力有点大，不知道该怎么调节...',
      created_at: new Date().toISOString()
    },
    {
      id: 2,
      content: '我理解你的感受，可以尝试一些放松技巧...',
      created_at: new Date(Date.now() - 30 * 60 * 1000).toISOString()
    }
  ]
}

onMounted(() => {
  loadRecentChats()
})
</script>

<style scoped>
.container {
  padding: 40rpx;
  min-height: 100vh;
  background: linear-gradient(180deg, #f5f7fa 0%, #ffffff 100%);
}

.header {
  margin-bottom: 60rpx;
}

.welcome {
  display: block;
  font-size: 40rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 10rpx;
}

.subtitle {
  display: block;
  font-size: 28rpx;
  color: #666;
  margin-bottom: 8rpx;
}

.date {
  display: block;
  font-size: 24rpx;
  color: #999;
}

.quick-actions {
  display: flex;
  justify-content: space-between;
  margin-bottom: 60rpx;
  flex-wrap: wrap;
  gap: 20rpx;
}

.action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  min-width: 160rpx;
  background: white;
  border-radius: 20rpx;
  padding: 30rpx 20rpx;
  box-shadow: 0 4rpx 20rpx rgba(0,0,0,0.06);
}

.action-icon {
  font-size: 60rpx;
  margin-bottom: 20rpx;
}

.action-text {
  font-size: 24rpx;
  color: #333;
  text-align: center;
}

.mood-tracker {
  background: white;
  border-radius: 20rpx;
  padding: 40rpx;
  margin-bottom: 40rpx;
  box-shadow: 0 4rpx 20rpx rgba(0,0,0,0.06);
}

.section-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30rpx;
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.see-more, .see-all {
  font-size: 26rpx;
  color: #667eea;
}

.mood-content {
  display: flex;
  align-items: center;
  gap: 40rpx;
}

.mood-score {
  text-align: center;
}

.score {
  display: block;
  font-size: 48rpx;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 8rpx;
}

.score-label {
  font-size: 24rpx;
  color: #999;
}

.mood-description {
  flex: 1;
}

.mood-text {
  display: block;
  font-size: 28rpx;
  color: #333;
  margin-bottom: 8rpx;
}

.mood-time {
  font-size: 24rpx;
  color: #999;
}

.recent-chats {
  background: white;
  border-radius: 20rpx;
  padding: 40rpx;
  margin-bottom: 40rpx;
  box-shadow: 0 4rpx 20rpx rgba(0,0,0,0.06);
}

.chat-list {
  margin-top: 20rpx;
}

.chat-item {
  display: flex;
  align-items: flex-start;
  padding: 25rpx 0;
  border-bottom: 1rpx solid #f0f0f0;
}

.chat-item:last-child {
  border-bottom: none;
}

.chat-avatar {
  width: 80rpx;
  height: 80rpx;
  background: #667eea;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24rpx;
  margin-right: 25rpx;
  flex-shrink: 0;
}

.chat-content {
  flex: 1;
}

.chat-preview {
  display: block;
  font-size: 28rpx;
  color: #333;
  margin-bottom: 8rpx;
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.chat-time {
  font-size: 22rpx;
  color: #999;
}

.empty-state {
  text-align: center;
  padding: 60rpx 40rpx;
  color: #999;
  font-size: 28rpx;
}

.daily-tip {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20rpx;
  padding: 40rpx;
  color: white;
}

.tip-header {
  display: flex;
  align-items: center;
  margin-bottom: 20rpx;
}

.tip-icon {
  font-size: 36rpx;
  margin-right: 15rpx;
}

.tip-title {
  font-size: 28rpx;
  font-weight: bold;
}

.tip-content {
  font-size: 26rpx;
  line-height: 1.5;
  opacity: 0.9;
}
</style>