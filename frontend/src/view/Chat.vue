<template>
  <MainLayout>
    <div class="chat-container">
      <div class="chat-content">
        <!-- 消息列表 -->
        <div ref="messagesContainer" class="messages-container">
          <!-- 欢迎消息 -->
          <div class="welcome-section">
            <div class="welcome-badge">
              今天 · 心晴港湾
            </div>
          </div>
          
          <!-- 消息列表 -->
          <div
            v-for="message in messages"
            :key="message.id"
            :class="['message-item', `message-${message.role}`]"
          >
            <!-- AI 消息 -->
            <div v-if="message.role === 'ai'" class="message ai-message">
              <div class="message-avatar ai-avatar">
                <el-icon><ChatRound /></el-icon>
              </div>
              <div class="message-content">
                <div class="message-bubble ai-bubble">
                  <div class="message-text">{{ message.content }}</div>
                </div>
                <div class="message-meta">
                  <span class="message-time">{{ formatTime(message.timestamp) }}</span>
                </div>
              </div>
            </div>
            
            <!-- 用户消息 -->
            <div v-else class="message user-message">
              <div class="message-content">
                <div class="message-bubble user-bubble">
                  <div class="message-text">{{ message.content }}</div>
                </div>
                <div class="message-meta">
                  <span class="message-time">{{ formatTime(message.timestamp) }}</span>
                  <div class="emotion-indicator">
                    <el-icon 
                      v-if="message.emotionScore !== null"
                      :class="['emotion-icon', getEmotionClass(message.emotionScore)]"
                    >
                      <CircleFilled />
                    </el-icon>
                  </div>
                </div>
              </div>
              <div class="message-avatar user-avatar">
                {{ userInitial }}
              </div>
            </div>
          </div>
          
          <!-- 加载状态 -->
          <div v-if="loading" class="loading-indicator">
            <el-icon class="is-loading"><Loading /></el-icon>
            <span>AI正在思考...</span>
          </div>
        </div>
        
        <!-- 输入区域 -->
        <div class="input-section">
          <div class="input-container">
            <el-input
              v-model="inputMessage"
              type="textarea"
              :rows="1"
              :autosize="{ minRows: 1, maxRows: 4 }"
              placeholder="输入消息..."
              resize="none"
              @keydown="handleKeydown"
            />
            <el-button
              type="primary"
              :disabled="!inputMessage.trim() || loading"
              @click="sendMessage"
              class="send-btn"
            >
              <el-icon><Promotion /></el-icon>
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, computed, nextTick, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useChatStore } from '@/stores/chat'
import { ElMessage } from 'element-plus'
import { 
  ChatRound, 
  Promotion, 
  Loading,
  CircleFilled 
} from '@element-plus/icons-vue'
import MainLayout from '@/components/layout/MainLayout.vue'

const authStore = useAuthStore()
const chatStore = useChatStore()

const inputMessage = ref('')
const messagesContainer = ref(null)

const userInitial = computed(() => authStore.userInitial)
const messages = computed(() => chatStore.messages)
const loading = computed(() => chatStore.loading)

// 格式化时间
const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  return `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
}

// 获取情感图标类名
const getEmotionClass = (score) => {
  if (score >= 0.7) return 'emotion-positive'
  if (score >= 0.4) return 'emotion-neutral'
  return 'emotion-negative'
}

// 发送消息
const sendMessage = async () => {
  if (!inputMessage.value.trim()) return
  
  await chatStore.sendMessage(inputMessage.value)
  inputMessage.value = ''
  
  // 滚动到底部
  nextTick(() => {
    scrollToBottom()
  })
}

// 处理键盘事件
const handleKeydown = (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    sendMessage()
  }
}

// 滚动到底部
const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// 初始化欢迎消息
onMounted(() => {
  if (chatStore.messages.length === 0) {
    chatStore.addMessage({
      role: 'ai',
      content: '你好！我是你的AI心理助手。无论你有什么烦恼或困惑，都可以和我分享。我会认真倾听并尽力帮助你。今天感觉如何？',
      emotionScore: null
    })
  }
  
  nextTick(() => {
    scrollToBottom()
  })
})
</script>

<style scoped lang="scss">
.chat-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  max-width: 1200px;
  margin: 0 auto;
}

.chat-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.welcome-section {
  display: flex;
  justify-content: center;
  margin-bottom: 16px;
}

.welcome-badge {
  background: var(--bg-gray);
  color: var(--text-secondary);
  padding: 8px 16px;
  border-radius: 16px;
  font-size: 14px;
}

.message-item {
  display: flex;
  
  &.message-user {
    justify-content: flex-end;
  }
}

.message {
  display: flex;
  gap: 12px;
  max-width: 70%;
  
  &.user-message {
    flex-direction: row-reverse;
  }
}

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  
  &.ai-avatar {
    background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
    color: white;
  }
  
  &.user-avatar {
    background: var(--bg-gray);
    color: var(--text-primary);
    font-weight: bold;
  }
}

.message-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.message-bubble {
  padding: 12px 16px;
  border-radius: 16px;
  max-width: 100%;
  word-wrap: break-word;
  
  &.ai-bubble {
    background: white;
    border: 1px solid var(--border-color);
    border-top-left-radius: 4px;
  }
  
  &.user-bubble {
    background: var(--primary-color);
    color: white;
    border-top-right-radius: 4px;
  }
}

.message-text {
  line-height: 1.5;
  white-space: pre-wrap;
}

.message-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  
  .user-message & {
    justify-content: flex-end;
  }
}

.message-time {
  color: var(--text-light);
}

.emotion-indicator {
  display: flex;
  align-items: center;
}

.emotion-icon {
  font-size: 12px;
  
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

.loading-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 16px;
  color: var(--text-secondary);
  font-size: 14px;
}

.input-section {
  padding: 20px 24px;
  background: white;
  border-top: 1px solid var(--border-color);
}

.input-container {
  display: flex;
  gap: 12px;
  align-items: flex-end;
  max-width: 800px;
  margin: 0 auto;
}

:deep(.el-textarea) {
  .el-textarea__inner {
    border-radius: 20px;
    padding: 12px 16px;
    resize: none;
    border: 1px solid var(--border-color);
    
    &:focus {
      border-color: var(--primary-color);
    }
  }
}

.send-btn {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  flex-shrink: 0;
  
  &:disabled {
    background: var(--text-light);
    border-color: var(--text-light);
  }
}

// 响应式设计
@media (max-width: 768px) {
  .messages-container {
    padding: 16px;
  }
  
  .message {
    max-width: 85%;
  }
  
  .input-section {
    padding: 16px;
  }
}
</style>