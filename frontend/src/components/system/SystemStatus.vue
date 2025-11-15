<template>
  <el-popover
    placement="bottom-end"
    width="300"
    trigger="click"
  >
    <template #reference>
      <el-button 
        :type="systemStatusType" 
        :icon="Connection" 
        text
        :loading="systemStore.loading"
      >
        {{ systemStatusText }}
      </el-button>
    </template>
    
    <div class="system-status-popover">
      <h4>系统状态</h4>
      
      <div class="status-item">
        <span class="label">AI 服务:</span>
        <el-tag 
          :type="systemStore.ollamaAvailable ? 'success' : 'danger'"
          size="small"
        >
          {{ systemStore.ollamaAvailable ? '正常运行' : '不可用' }}
        </el-tag>
      </div>
      
      <div class="status-item">
        <span class="label">当前模型:</span>
        <span class="value">{{ systemStore.currentModel || '未设置' }}</span>
      </div>
      
      <el-divider />
      
      <div class="models-section">
        <h5>可用模型</h5>
        <div v-if="systemStore.availableModels.length === 0" class="no-models">
          未检测到可用模型
        </div>
        <div v-else class="models-list">
          <div
            v-for="model in systemStore.availableModels"
            :key="model.name"
            :class="['model-item', { active: model.name === systemStore.currentModel }]"
          >
            <span class="model-name">{{ model.name }}</span>
            <el-button
              v-if="model.name !== systemStore.currentModel"
              type="primary"
              size="small"
              @click="handleSwitchModel(model.name)"
            >
              切换
            </el-button>
            <el-tag v-else type="success" size="small">当前</el-tag>
          </div>
        </div>
      </div>
      
      <el-divider />
      
      <div class="actions">
        <el-button 
          type="primary" 
          size="small" 
          @click="handleRefresh"
          :loading="systemStore.loading"
        >
          刷新状态
        </el-button>
      </div>
    </div>
  </el-popover>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { Connection } from '@element-plus/icons-vue'
import { useSystemStore } from '@/stores/system'
import { ElMessage } from 'element-plus'

const systemStore = useSystemStore()

const systemStatusType = computed(() => {
  return systemStore.ollamaAvailable ? 'success' : 'danger'
})

const systemStatusText = computed(() => {
  return systemStore.ollamaAvailable ? 'AI在线' : 'AI离线'
})

const handleSwitchModel = async (modelName) => {
  const result = await systemStore.changeModel(modelName)
  if (result.success) {
    ElMessage.success(result.message)
  } else {
    ElMessage.error(result.message)
  }
}

const handleRefresh = async () => {
  await systemStore.checkSystemHealth()
}

onMounted(() => {
  // 初始化时检查系统状态
  systemStore.checkSystemHealth()
})
</script>

<style scoped lang="scss">
.system-status-popover {
  h4 {
    margin: 0 0 16px 0;
    color: var(--text-primary);
  }
  
  h5 {
    margin: 0 0 12px 0;
    color: var(--text-primary);
    font-size: 14px;
  }
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  
  .label {
    color: var(--text-secondary);
    font-size: 14px;
  }
  
  .value {
    color: var(--text-primary);
    font-weight: 500;
  }
}

.models-section {
  .no-models {
    text-align: center;
    color: var(--text-light);
    font-size: 14px;
    padding: 8px 0;
  }
}

.models-list {
  max-height: 200px;
  overflow-y: auto;
}

.model-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  margin-bottom: 8px;
  border-radius: 6px;
  border: 1px solid var(--border-color);
  transition: all 0.2s;
  
  &:hover {
    background-color: var(--bg-gray);
  }
  
  &.active {
    border-color: var(--primary-color);
    background-color: rgba(59, 130, 246, 0.05);
  }
  
  .model-name {
    font-size: 14px;
    color: var(--text-primary);
    font-weight: 500;
  }
}

.actions {
  display: flex;
  justify-content: center;
}
</style>