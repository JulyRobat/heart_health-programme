<template>
  <MainLayout>
    <div class="emergency-container">
      <div class="emergency-content">
        <div class="emergency-header">
          <h2>紧急求助</h2>
          <p>如果您正在经历心理危机，请立即寻求帮助</p>
        </div>

        <el-alert
          title="紧急提示"
          type="error"
          description="如果你正在经历紧急的心理危机或有自伤倾向，请立即拨打下面的紧急求助电话。"
          :closable="false"
          show-icon
          class="emergency-alert"
        />

        <div class="emergency-resources">
          <el-card class="resource-card">
            <template #header>
              <span class="resource-title">紧急求助资源</span>
            </template>
            
            <div class="resource-list">
              <div class="resource-item">
                <div class="resource-icon">
                  <el-icon><Phone /></el-icon>
                </div>
                <div class="resource-info">
                  <h3>国家心理危机干预热线</h3>
                  <p>24小时服务，专业心理咨询师在线</p>
                  <div class="resource-phone">400-161-9995</div>
                </div>
              </div>
              
              <div class="resource-item">
                <div class="resource-icon">
                  <el-icon><Phone /></el-icon>
                </div>
                <div class="resource-info">
                  <h3>北京心理援助热线</h3>
                  <p>24小时服务，专业心理咨询师在线</p>
                  <div class="resource-phone">010-82951332</div>
                </div>
              </div>
              
              <div class="resource-item">
                <div class="resource-icon">
                  <el-icon><Phone /></el-icon>
                </div>
                <div class="resource-info">
                  <h3>校园心理咨询中心</h3>
                  <p>工作日 9:00-17:00</p>
                  <div class="resource-phone">010-12345678</div>
                </div>
              </div>
            </div>
          </el-card>
        </div>

        <div class="emergency-contact">
          <el-card>
            <template #header>
              <span>联系紧急联系人</span>
            </template>
            
            <div class="contact-content">
              <p class="contact-desc">我们可以立即通知您设置的紧急联系人。</p>
              
              <div class="contact-info">
                <h4>紧急联系人信息</h4>
                <div class="contact-detail">
                  <el-icon><User /></el-icon>
                  <span>{{ emergencyContact || '未设置紧急联系人' }}</span>
                </div>
              </div>
              
              <el-button
                type="danger"
                size="large"
                @click="notifyEmergencyContact"
                class="notify-btn"
                :disabled="!emergencyContact"
              >
                <el-icon><Bell /></el-icon>
                立即通知紧急联系人
              </el-button>
              
              <p class="contact-note">
                点击按钮后，系统将向您的紧急联系人发送通知短信，告知您可能需要帮助。
              </p>
            </div>
          </el-card>
        </div>

        <div class="self-help-section">
          <el-card>
            <template #header>
              <span>自助应对方法</span>
            </template>
            
            <div class="self-help-content">
              <el-collapse>
                <el-collapse-item title="深呼吸放松法" name="1">
                  <div class="self-help-item">
                    <p>1. 找一个安静的地方坐下或躺下</p>
                    <p>2. 缓慢吸气4秒，感受空气充满肺部</p>
                    <p>3. 屏住呼吸4秒</p>
                    <p>4. 缓慢呼气6秒，彻底排出空气</p>
                    <p>5. 重复5-10次，直到感觉平静</p>
                  </div>
                </el-collapse-item>
                
                <el-collapse-item title="安全环境建立" name="2">
                  <div class="self-help-item">
                    <p>• 确保身处安全的环境</p>
                    <p>• 远离可能伤害自己的物品</p>
                    <p>• 联系信任的朋友或家人</p>
                    <p>• 进行简单的身体活动（散步、伸展）</p>
                    <p>• 听舒缓的音乐或自然声音</p>
                  </div>
                </el-collapse-item>
                
                <el-collapse-item title="情绪稳定技巧" name="3">
                  <div class="self-help-item">
                    <p>• 5-4-3-2-1感官练习：说出5个看到的、4个触摸到的、3个听到的、2个闻到的、1个尝到的东西</p>
                    <p>• 冷水刺激：用冷水洗脸或洗手</p>
                    <p>• 渐进式肌肉放松：从头到脚逐步放松肌肉</p>
                    <p>• 正念观察：专注于当下的感受，不加评判</p>
                  </div>
                </el-collapse-item>
              </el-collapse>
            </div>
          </el-card>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Phone, User, Bell } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import MainLayout from '@/components/layout/MainLayout.vue'

const authStore = useAuthStore()
const emergencyContact = ref('')

const notifyEmergencyContact = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要通知紧急联系人吗？这将向他们发送求助信息。',
      '确认通知',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 模拟发送通知
    ElMessage.success(`已通知紧急联系人 ${emergencyContact.value}，他们将尽快与您联系。`)
    
    // 在实际应用中，这里会调用后端API发送通知
  } catch (error) {
    // 用户取消操作
  }
}

onMounted(() => {
  emergencyContact.value = authStore.user?.emergency_contact || ''
})
</script>

<style scoped lang="scss">
.emergency-container {
  height: 100%;
  overflow-y: auto;
}

.emergency-content {
  max-width: 800px;
  margin: 0 auto;
  padding: 24px;
}

.emergency-header {
  text-align: center;
  margin-bottom: 32px;
  
  h2 {
    font-size: 28px;
    color: var(--text-primary);
    margin-bottom: 8px;
  }
  
  p {
    color: var(--text-secondary);
    font-size: 16px;
  }
}

.emergency-alert {
  margin-bottom: 32px;
}

.emergency-resources {
  margin-bottom: 32px;
}

.resource-title {
  font-size: 18px;
  font-weight: bold;
}

.resource-list {
  .resource-item {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    padding: 20px 0;
    border-bottom: 1px solid var(--border-color);
    
    &:last-child {
      border-bottom: none;
    }
  }
}

.resource-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #EF4444, #DC2626);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
  
  .el-icon {
    font-size: 24px;
  }
}

.resource-info {
  flex: 1;
  
  h3 {
    font-size: 16px;
    font-weight: bold;
    color: var(--text-primary);
    margin-bottom: 4px;
  }
  
  p {
    color: var(--text-secondary);
    font-size: 14px;
    margin-bottom: 8px;
  }
}

.resource-phone {
  font-size: 20px;
  font-weight: bold;
  color: #EF4444;
}

.emergency-contact {
  margin-bottom: 32px;
}

.contact-content {
  text-align: center;
}

.contact-desc {
  color: var(--text-secondary);
  margin-bottom: 24px;
}

.contact-info {
  margin-bottom: 24px;
  
  h4 {
    color: var(--text-primary);
    margin-bottom: 16px;
  }
}

.contact-detail {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 16px;
  background: var(--bg-gray);
  border-radius: 8px;
  font-size: 18px;
  font-weight: 500;
}

.notify-btn {
  width: 100%;
  margin-bottom: 16px;
}

.contact-note {
  color: var(--text-light);
  font-size: 14px;
  line-height: 1.5;
}

.self-help-section {
  margin-bottom: 32px;
}

.self-help-item {
  p {
    margin-bottom: 8px;
    line-height: 1.6;
    
    &:last-child {
      margin-bottom: 0;
    }
  }
}

@media (max-width: 768px) {
  .emergency-content {
    padding: 16px;
  }
  
  .resource-item {
    flex-direction: column;
    text-align: center;
  }
  
  .resource-icon {
    align-self: center;
  }
}
</style>