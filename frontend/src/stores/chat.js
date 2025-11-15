import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { sendMessage as sendMessageApi, analyzeEmotion } from '@/api/chat'
import { useSystemStore } from './system'
import { ElMessage } from 'element-plus'

export const useChatStore = defineStore('chat', () => {
  const messages = ref([])
  const currentEmotion = ref({ label: '中性', type: 'neutral', score: 0.5 })
  const loading = ref(false)
  const systemStore = useSystemStore()
  
  // 添加消息
  const addMessage = (message) => {
    messages.value.push({
      id: Date.now(),
      ...message,
      timestamp: new Date()
    })
  }
  
  // 发送消息
  const sendMessage = async (content) => {
    if (!content.trim()) return
    
    // 检查系统状态
    if (!systemStore.ollamaAvailable) {
      const healthResult = await systemStore.checkSystemHealth()
      if (!healthResult.success || !systemStore.ollamaAvailable) {
        ElMessage.error('AI 服务不可用，请检查 Ollama 是否正在运行')
        return
      }
    }
    
    // 添加用户消息
    const userMessage = {
      role: 'user',
      content: content.trim(),
      emotionScore: 0.5
    }
    addMessage(userMessage)
    
    loading.value = true
    
    try {
      // 发送到后端
      const response = await sendMessageApi({ message: content })
      
      if (response.success) {
        // 添加AI回复
        const aiMessage = {
          role: 'ai',
          content: response.response,
          emotionScore: null
        }
        addMessage(aiMessage)
        
        // 分析情感
        if (response.user_dialog_id) {
          await analyzeUserEmotion(content, response.user_dialog_id)
        }
      } else {
        ElMessage.error(response.message || '发送消息失败')
      }
    } catch (error) {
      console.error('发送消息失败:', error)
      ElMessage.error(error.message || '网络请求失败')
      
      // 添加错误回复
      addMessage({
        role: 'ai',
        content: '抱歉，我暂时无法回复。请检查 AI 服务是否正常运行。',
        emotionScore: null
      })
    } finally {
      loading.value = false
    }
  }
  
  // 分析用户情感
  const analyzeUserEmotion = async (text, dialogId) => {
    try {
      const response = await analyzeEmotion({
        text: text,
        dialog_id: dialogId
      })
      
      if (response.success) {
        updateCurrentEmotion(response.analysis.emotion_score)
        
        // 更新最后一条用户消息的情感得分
        const lastUserMessage = [...messages.value]
          .reverse()
          .find(msg => msg.role === 'user')
        
        if (lastUserMessage) {
          lastUserMessage.emotionScore = response.analysis.emotion_score
        }
      }
    } catch (error) {
      console.error('情感分析失败:', error)
    }
  }
  
  // 更新当前情绪
  const updateCurrentEmotion = (score) => {
    if (score >= 0.7) {
      currentEmotion.value = { 
        label: '积极', 
        type: 'positive', 
        score: score 
      }
    } else if (score >= 0.4) {
      currentEmotion.value = { 
        label: '中性', 
        type: 'neutral', 
        score: score 
      }
    } else {
      currentEmotion.value = { 
        label: '消极', 
        type: 'negative', 
        score: score 
      }
    }
  }
  
  // 清空对话
  const clearMessages = () => {
    messages.value = []
  }
  
  return {
    messages,
    currentEmotion,
    loading,
    sendMessage,
    addMessage,
    updateCurrentEmotion,
    clearMessages
  }
})