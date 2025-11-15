import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getSystemHealth, getAvailableModels, switchModel } from '@/api/system'

export const useSystemStore = defineStore('system', () => {
  const ollamaAvailable = ref(false)
  const availableModels = ref([])
  const currentModel = ref('')
  const loading = ref(false)
  
  // 检查系统状态
  const checkSystemHealth = async () => {
    loading.value = true
    try {
      const response = await getSystemHealth()
      
      if (response.success) {
        ollamaAvailable.value = response.ollama_available
        availableModels.value = response.available_models || []
        currentModel.value = response.current_model
        
        return {
          success: true,
          ollamaAvailable: response.ollama_available,
          currentModel: response.current_model
        }
      }
    } catch (error) {
      console.error('检查系统状态失败:', error)
      ollamaAvailable.value = false
      return {
        success: false,
        message: error.message || '检查系统状态失败'
      }
    } finally {
      loading.value = false
    }
  }
  
  // 获取可用模型
  const fetchAvailableModels = async () => {
    try {
      const response = await getAvailableModels()
      if (response.success) {
        availableModels.value = response.models || []
        return availableModels.value
      }
    } catch (error) {
      console.error('获取模型列表失败:', error)
      return []
    }
  }
  
  // 切换模型
  const changeModel = async (modelName) => {
    try {
      const response = await switchModel(modelName)
      if (response.success) {
        currentModel.value = modelName
        return { success: true, message: response.message }
      }
    } catch (error) {
      return { 
        success: false, 
        message: error.message || '切换模型失败' 
      }
    }
  }
  
  return {
    ollamaAvailable,
    availableModels,
    currentModel,
    loading,
    checkSystemHealth,
    fetchAvailableModels,
    changeModel
  }
})