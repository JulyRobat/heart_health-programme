<template>
  <view class="chat-container">
    <!-- 紧急情况提示 -->
    <view v-if="currentEmergencyLevel === 'high'" class="emergency-alert">
      <view class="alert-content">
        <text class="alert-icon">⚠️</text>
        <text class="alert-text">检测到紧急情况，已通知您的紧急联系人</text>
      </view>
      <view class="emergency-contacts">
        <text class="contact-item">心理危机干预热线: 400-161-9995</text>
        <text class="contact-item">希望24热线: 400-161-9995</text>
      </view>
    </view>
    
    <!-- 聊天区域 -->
    <scroll-view 
      class="chat-messages" 
      scroll-y 
      :scroll-top="scrollTop"
      scroll-with-animation
      @scrolltoupper="loadMoreMessages"
    >
      <view v-if="loadingMore" class="loading-more">
        <text>加载中...</text>
      </view>
      
      <view 
        v-for="message in messages" 
        :key="message.id"
        :class="['message', message.role]"
      >
        <view class="message-avatar">
          <text>{{ message.role === 'user' ? '我' : 'AI' }}</text>
        </view>
        <view class="message-content-wrapper">
          <view class="message-bubble">
            <text class="message-text">{{ message.content }}</text>
            <view v-if="message.role === 'user' && message.emotion_score !== undefined" class="emotion-indicator">
              <text class="emotion-text">情绪值: {{ (message.emotion_score * 10).toFixed(1) }}</text>
              <view class="emotion-bar">
                <view 
                  class="emotion-fill" 
                  :style="{ width: (message.emotion_score * 100) + '%' }"
                  :class="getEmotionClass(message.emotion_score)"
                ></view>
              </view>
            </view>
          </view>
          <text class="message-time">{{ formatTime(message.created_at) }}</text>
        </view>
      </view>
      
      <view v-if="loading" class="typing-indicator">
        <view class="typing-dots">
          <view class="dot"></view>
          <view class="dot"></view>
          <view class="dot"></view>
        </view>
        <text class="typing-text">AI心理助手正在思考...</text>
      </view>
    </scroll-view>
    
    <!-- 输入区域 -->
    <view class="input-area">
      <input 
        v-model="inputMessage" 
        class="message-input" 
        placeholder="告诉我您现在的感受和想法..."
        :disabled="loading"
        @confirm="sendMessage"
        maxlength="500"
      />
      <view class="input-actions">
        <text class="char-count">{{ inputMessage.length }}/500</text>
        <button 
          class="send-btn" 
          @click="sendMessage" 
          :disabled="loading || !inputMessage.trim()"
        >
          <text class="send-icon">↑</text>
        </button>
      </view>
    </view>
    
    <!-- 快速回复建议 -->
    <view v-if="showQuickReplies" class="quick-replies">
      <scroll-view class="replies-scroll" scroll-x>
        <view 
          v-for="reply in quickReplies" 
          :key="reply.id"
          class="reply-item"
          @click="useQuickReply(reply.text)"
        >
          <text>{{ reply.text }}</text>
        </view>
      </scroll-view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted, nextTick, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const messages = ref([])
const inputMessage = ref('')
const loading = ref(false)
const loadingMore = ref(false)
const scrollTop = ref(0)
const currentEmergencyLevel = ref('')
const showQuickReplies = ref(true)

const quickReplies = ref([
  { id: 1, text: '最近压力很大，怎么办？' },
  { id: 2, text: '如何改善睡眠质量？' },
  { id: 3, text: '感觉焦虑不安，如何缓解？' },
  { id: 4, text: '人际关系处理不好，很烦恼' },
  { id: 5, text: '学习压力大，感觉很累' }
])

const getEmotionText = (score) => {
  if (score >= 0.7) return '积极'
  if (score >= 0.4) return '一般'
  return '低落'
}

const getEmotionClass = (score) => {
  if (score >= 0.7) return 'positive'
  if (score >= 0.4) return 'neutral'
  return 'negative'
}

const formatTime = (timeStr) => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  return `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
}

const scrollToBottom = () => {
  nextTick(() => {
    scrollTop.value = 999999
  })
}

const loadChatHistory = () => {
  // 模拟历史消息
  messages.value = [
    {
      id: 1,
      role: 'ai',
      content: '您好！我是心晴港湾AI心理助手，很高兴为您服务。请告诉我您现在的感受和想法，我会尽力为您提供支持和帮助。',
      created_at: new Date(Date.now() - 5 * 60 * 1000).toISOString()
    }
  ]
  scrollToBottom()
}

const sendMessage = async () => {
  if (!inputMessage.value.trim() || loading.value) return

  const userMessage = {
    id: Date.now(),
    role: 'user',
    content: inputMessage.value,
    emotion_score: Math.random(), // 模拟情感分析分数
    created_at: new Date().toISOString()
  }
  
  messages.value.push(userMessage)
  const messageText = inputMessage.value
  inputMessage.value = ''
  loading.value = true
  showQuickReplies.value = false
  
  scrollToBottom()

  try {
    // 模拟AI回复
    await new Promise(resolve => setTimeout(resolve, 1500 + Math.random() * 1000))
    
    const aiResponses = [
      '我理解您的感受。这种情况下，建议您先深呼吸几次，让自己平静下来。',
      '听起来您正在经历一段艰难的时期。请记住，您不是一个人，很多人都经历过类似的感受。',
      '感谢您分享这些感受。我们可以一起探讨一些应对策略，帮助您更好地处理当前的情况。',
      '我明白这很不容易。或许可以尝试将大问题分解成小步骤，这样会感觉更容易应对。',
      '您的感受很重要。让我们一起来寻找适合您的放松和应对方法。'
    ]
    
    const randomResponse = aiResponses[Math.floor(Math.random() * aiResponses.length)]
    
    const aiMessage = {
      id: Date.now() + 1,
      role: 'ai',
      content: randomResponse,
      created_at: new Date().toISOString()
    }
    
    messages.value.push(aiMessage)
    
    // 模拟情感分析结果
    const emotionScore = Math.random()
    if (emotionScore < 0.3) {
      currentEmergencyLevel.value = 'high'
      uni.showModal({
        title: '重要提示',
        content: '系统检测到您可能需要紧急帮助，请记得：您不是一个人，我们都在关心您。如果需要，请立即使用紧急求助功能。',
        showCancel: false,
        confirmText: '我知道了'
      })
    } else {
      currentEmergencyLevel.value = 'low'
    }
    
    scrollToBottom()
    
  } catch (error) {
    console.error('发送消息失败:', error)
    uni.showToast({
      title: '发送失败，请重试',
      icon: 'none'
    })
  } finally {
    loading.value = false
  }
}

const useQuickReply = (text) => {
  inputMessage.value = text
}

const loadMoreMessages = () => {
  if (loadingMore.value) return
  loadingMore.value = true
  
  // 模拟加载更多消息
  setTimeout(() => {
    const moreMessages = [
      {
        id: messages.value.length + 1,
        role: 'user',
        content: '之前我咨询过类似的问题',
        created_at: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString()
      },
      {
        id: messages.value.length + 2,
        role: 'ai',
        content: '很高兴看到您持续关注自己的心理健康。我们可以继续深入探讨您关心的话题。',
        created_at: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString()
      }
    ]
    
    messages.value.unshift(...moreMessages)
    loadingMore.value = false
  }, 1000)
}

onMounted(() => {
  loadChatHistory()
})
</script>

<style scoped>
.chat-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f7fa;
}

.emergency-alert {
  background: #fff2f0;
  border: 1rpx solid #ffccc7;
  border-radius: 12rpx;
  margin: 20rpx;
  padding: 25rpx;
}

.alert-content {
  display: flex;
  align-items: center;
  margin-bottom: 15rpx;
}

.alert-icon {
  font-size: 36rpx;
  margin-right: 15rpx;
}

.alert-text {
  font-size: 26rpx;
  color: #a8071a;
  font-weight: bold;
}

.emergency-contacts {
  border-top: 1rpx solid #ffccc7;
  padding-top: 15rpx;
}

.contact-item {
  display: block;
  font-size: 22rpx;
  color: #a8071a;
  margin-bottom: 8rpx;
}

.chat-messages {
  flex: 1;
  padding: 20rpx;
  background: #f5f7fa;
}

.loading-more {
  text-align: center;
  padding: 20rpx;
  color: #999;
  font-size: 26rpx;
}

.message {
  display: flex;
  margin-bottom: 40rpx;
  animation: fadeIn 0.3s ease;
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 80rpx;
  height: 80rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24rpx;
  font-weight: bold;
  flex-shrink: 0;
  margin: 0 20rpx;
}

.message.user .message-avatar {
  background: #667eea;
  color: white;
}

.message.ai .message-avatar {
  background: #52c41a;
  color: white;
}

.message-content-wrapper {
  max-width: 70%;
}

.message-bubble {
  padding: 25rpx 30rpx;
  border-radius: 20rpx;
  position: relative;
  margin-bottom: 10rpx;
}

.message.user .message-bubble {
  background: #667eea;
  color: white;
  border-bottom-right-radius: 8rpx;
}

.message.ai .message-bubble {
  background: white;
  border: 1rpx solid #e8e8e8;
  border-bottom-left-radius: 8rpx;
  box-shadow: 0 2rpx 12rpx rgba(0,0,0,0.06);
}

.message-text {
  font-size: 28rpx;
  line-height: 1.5;
}

.emotion-indicator {
  margin-top: 15rpx;
  padding-top: 15rpx;
  border-top: 1rpx solid rgba(255,255,255,0.3);
}

.emotion-text {
  font-size: 22rpx;
  opacity: 0.8;
  margin-bottom: 10rpx;
  display: block;
}

.emotion-bar {
  width: 120rpx;
  height: 8rpx;
  background: rgba(255,255,255,0.3);
  border-radius: 4rpx;
  overflow: hidden;
}

.emotion-fill {
  height: 100%;
  transition: width 0.3s ease;
}

.emotion-fill.positive {
  background: #52c41a;
}

.emotion-fill.neutral {
  background: #faad14;
}

.emotion-fill.negative {
  background: #f5222d;
}

.message-time {
  font-size: 22rpx;
  color: #999;
  text-align: center;
}

.message.user .message-time {
  text-align: right;
  padding-right: 10rpx;
}

.message.ai .message-time {
  text-align: left;
  padding-left: 10rpx;
}

.typing-indicator {
  display: flex;
  align-items: center;
  padding: 20rpx;
  color: #999;
}

.typing-dots {
  display: flex;
  margin-right: 15rpx;
}

.dot {
  width: 8rpx;
  height: 8rpx;
  background: #999;
  border-radius: 50%;
  margin: 0 4rpx;
  animation: typing 1.4s infinite ease-in-out;
}

.dot:nth-child(1) { animation-delay: -0.32s; }
.dot:nth-child(2) { animation-delay: -0.16s; }

.typing-text {
  font-size: 26rpx;
}

.input-area {
  background: white;
  border-top: 1rpx solid #e8e8e8;
  padding: 20rpx;
}

.message-input {
  border: 2rpx solid #e8e8e8;
  border-radius: 25rpx;
  padding: 20rpx 30rpx;
  font-size: 28rpx;
  margin-bottom: 15rpx;
  background: #f8f9fa;
}

.input-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.char-count {
  font-size: 24rpx;
  color: #999;
}

.send-btn {
  background: #667eea;
  color: white;
  border: none;
  border-radius: 50%;
  width: 80rpx;
  height: 80rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32rpx;
}

.send-btn:disabled {
  background: #ccc;
}

.quick-replies {
  background: white;
  border-top: 1rpx solid #e8e8e8;
  padding: 20rpx;
}

.replies-scroll {
  white-space: nowrap;
}

.reply-item {
  display: inline-block;
  background: #f8f9fa;
  border: 1rpx solid #e8e8e8;
  border-radius: 20rpx;
  padding: 15rpx 25rpx;
  margin-right: 20rpx;
  font-size: 26rpx;
  color: #666;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10rpx); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes typing {
  0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
  40% { transform: scale(1); opacity: 1; }
}
</style>