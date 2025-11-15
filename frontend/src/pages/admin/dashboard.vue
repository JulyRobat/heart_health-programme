<template>
  <view class="emergency-container">
    <view class="emergency-header">
      <text class="title">紧急求助</text>
      <text class="subtitle">当您需要紧急心理支持时，请立即联系我们</text>
    </view>

    <view class="emergency-cards">
      <view class="emergency-card hotline">
        <view class="card-icon">📞</view>
        <view class="card-content">
          <text class="card-title">心理危机干预热线</text>
          <text class="card-desc">24小时免费心理援助热线，专业心理咨询师为您服务</text>
          <view class="hotline-number">400-161-9995</view>
          <button class="call-btn" @click="makeCall('400-161-9995')">立即拨打</button>
        </view>
      </view>

      <view class="emergency-card contact">
        <view class="card-icon">👨‍👩‍👧</view>
        <view class="card-content">
          <text class="card-title">紧急联系人</text>
          <text class="card-desc">系统将自动通知您的紧急联系人</text>
          <view class="contact-info">
            <text class="contact-name">{{ emergencyContact.name || '未设置' }}</text>
            <text class="contact-phone">{{ emergencyContact.phone || '请设置紧急联系人' }}</text>
          </view>
          <button class="notify-btn" @click="notifyEmergencyContact" :disabled="!emergencyContact.phone">
            {{ emergencyContact.phone ? '通知紧急联系人' : '请先设置紧急联系人' }}
          </button>
        </view>
      </view>

      <view class="emergency-card support">
        <view class="card-icon">💬</view>
        <view class="card-content">
          <text class="card-title">在线心理支持</text>
          <text class="card-desc">立即联系在线心理顾问，获得即时帮助</text>
          <button class="chat-btn" @click="contactOnlineSupport">联系在线顾问</button>
        </view>
      </view>
    </view>

    <view class="self-help-section">
      <view class="section-header">
        <text class="section-title">自助应对方法</text>
      </view>
      <view class="self-help-list">
        <view class="self-help-item" v-for="(item, index) in selfHelpMethods" :key="index">
          <text class="help-number">{{ index + 1 }}</text>
          <text class="help-text">{{ item }}</text>
        </view>
      </view>
    </view>

    <view class="safety-plan">
      <view class="section-header">
        <text class="section-title">安全计划</text>
      </view>
      <view class="plan-steps">
        <view class="plan-step" v-for="(step, index) in safetyPlan" :key="index">
          <view class="step-number">{{ index + 1 }}</view>
          <view class="step-content">
            <text class="step-title">{{ step.title }}</text>
            <text class="step-desc">{{ step.description }}</text>
          </view>
        </view>
      </view>
    </view>

    <view class="emergency-resources">
      <view class="section-header">
        <text class="section-title">紧急资源</text>
      </view>
      <view class="resources-list">
        <view class="resource-item" v-for="resource in emergencyResources" :key="resource.id">
          <text class="resource-name">{{ resource.name }}</text>
          <text class="resource-phone">{{ resource.phone }}</text>
          <button class="resource-call" @click="makeCall(resource.phone)">拨打</button>
        </view>
      </view>
    </view>

    <view class="emergency-footer">
      <text class="footer-text">请记住，您不是一个人，我们都在关心您</text>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const emergencyContact = ref({})
const selfHelpMethods = ref([
  '深呼吸：缓慢深呼吸，吸气4秒，屏息4秒，呼气6秒',
  '安全环境：确保自己处于安全的环境中',
  '分散注意力：尝试想一些愉快的事情或做简单活动',
  '联系信任的人：立即给朋友或家人打电话',
  '使用放松技巧：尝试肌肉放松或冥想'
])

const safetyPlan = ref([
  {
    title: '识别预警信号',
    description: '了解自己情绪危机的早期信号'
  },
  {
    title: '内部应对策略',
    description: '使用对自己有效的放松和分心技巧'
  },
  {
    title: '联系社会支持',
    description: '列出可以联系的朋友、家人或专业人士'
  },
  {
    title: '联系专业人士',
    description: '保存心理医生、危机热线的联系方式'
  },
  {
    title: '确保环境安全',
    description: '移除可能用于自我伤害的物品'
  }
])

const emergencyResources = ref([
  { id: 1, name: '全国心理援助热线', phone: '400-161-9995' },
  { id: 2, name: '北京心理危机干预中心', phone: '010-82951332' },
  { id: 3, name: '上海市心理援助热线', phone: '021-12320-5' },
  { id: 4, name: '广州市心理援助热线', phone: '020-81899120' }
])

const loadEmergencyContact = () => {
  // 从用户信息中获取紧急联系人
  const userInfo = authStore.userInfo
  if (userInfo && userInfo.emergency_contact) {
    emergencyContact.value = {
      name: '紧急联系人',
      phone: userInfo.emergency_contact
    }
  }
}

const makeCall = (phoneNumber) => {
  uni.makePhoneCall({
    phoneNumber: phoneNumber,
    success: () => {
      console.log('拨打电话成功')
    },
    fail: (err) => {
      uni.showToast({
        title: '拨打电话失败',
        icon: 'none'
      })
    }
  })
}

const notifyEmergencyContact = () => {
  if (!emergencyContact.value.phone) {
    uni.showToast({
      title: '请先设置紧急联系人',
      icon: 'none'
    })
    return
  }

  uni.showModal({
    title: '通知紧急联系人',
    content: '确定要通知您的紧急联系人吗？系统将发送求助信息。',
    success: (res) => {
      if (res.confirm) {
        // 模拟发送通知
        uni.showLoading({
          title: '发送中...'
        })

        setTimeout(() => {
          uni.hideLoading()
          uni.showToast({
            title: '已通知紧急联系人',
            icon: 'success'
          })
        }, 2000)
      }
    }
  })
}

const contactOnlineSupport = () => {
  uni.navigateTo({
    url: '/pages/chat/chat',
    success: () => {
      // 可以传递参数表示紧急求助
    }
  })
}

onMounted(() => {
  loadEmergencyContact()
})
</script>

<style scoped>
.emergency-container {
  padding: 40rpx;
  min-height: 100vh;
  background: linear-gradient(180deg, #fff5f5 0%, #ffffff 100%);
}

.emergency-header {
  text-align: center;
  margin-bottom: 50rpx;
}

.title {
  display: block;
  font-size: 40rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 10rpx;
}

.subtitle {
  display: block;
  font-size: 26rpx;
  color: #666;
}

.emergency-cards {
  margin-bottom: 50rpx;
}

.emergency-card {
  display: flex;
  background: white;
  border-radius: 20rpx;
  padding: 40rpx;
  margin-bottom: 30rpx;
  box-shadow: 0 4rpx 20rpx rgba(0,0,0,0.08);
  border-left: 6rpx solid #f5222d;
}

.emergency-card.hotline {
  border-left-color: #f5222d;
}

.emergency-card.contact {
  border-left-color: #fa8c16;
}

.emergency-card.support {
  border-left-color: #52c41a;
}

.card-icon {
  font-size: 60rpx;
  margin-right: 30rpx;
}

.card-content {
  flex: 1;
}

.card-title {
  display: block;
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 10rpx;
}

.card-desc {
  display: block;
  font-size: 24rpx;
  color: #666;
  margin-bottom: 20rpx;
  line-height: 1.4;
}

.hotline-number {
  font-size: 36rpx;
  font-weight: bold;
  color: #f5222d;
  margin-bottom: 20rpx;
  text-align: center;
  background: #fff2f0;
  padding: 20rpx;
  border-radius: 12rpx;
}

.contact-info {
  margin-bottom: 20rpx;
  padding: 20rpx;
  background: #fff7e6;
  border-radius: 12rpx;
}

.contact-name {
  display: block;
  font-size: 28rpx;
  color: #333;
  margin-bottom: 5rpx;
}

.contact-phone {
  font-size: 24rpx;
  color: #666;
}

.call-btn, .notify-btn, .chat-btn {
  border: none;
  border-radius: 12rpx;
  padding: 20rpx 30rpx;
  font-size: 28rpx;
  font-weight: bold;
  color: white;
}

.call-btn {
  background: #f5222d;
}

.notify-btn {
  background: #fa8c16;
}

.notify-btn:disabled {
  background: #ccc;
}

.chat-btn {
  background: #52c41a;
}

.self-help-section, .safety-plan, .emergency-resources {
  background: white;
  border-radius: 20rpx;
  padding: 40rpx;
  margin-bottom: 40rpx;
  box-shadow: 0 4rpx 20rpx rgba(0,0,0,0.06);
}

.section-header {
  margin-bottom: 30rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.self-help-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.self-help-item {
  display: flex;
  align-items: flex-start;
}

.help-number {
  width: 40rpx;
  height: 40rpx;
  background: #667eea;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22rpx;
  font-weight: bold;
  margin-right: 20rpx;
  flex-shrink: 0;
}

.help-text {
  font-size: 26rpx;
  color: #333;
  line-height: 1.5;
  flex: 1;
}

.plan-steps {
  display: flex;
  flex-direction: column;
  gap: 25rpx;
}

.plan-step {
  display: flex;
  align-items: flex-start;
}

.step-number {
  width: 50rpx;
  height: 50rpx;
  background: #52c41a;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24rpx;
  font-weight: bold;
  margin-right: 25rpx;
  flex-shrink: 0;
}

.step-content {
  flex: 1;
  padding-top: 5rpx;
}

.step-title {
  display: block;
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 8rpx;
}

.step-desc {
  font-size: 24rpx;
  color: #666;
  line-height: 1.4;
}

.resources-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.resource-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 25rpx;
  background: #f8f9fa;
  border-radius: 12rpx;
}

.resource-name {
  font-size: 26rpx;
  color: #333;
  flex: 1;
}

.resource-phone {
  font-size: 24rpx;
  color: #666;
  margin: 0 20rpx;
}

.resource-call {
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8rpx;
  padding: 12rpx 20rpx;
  font-size: 22rpx;
}

.emergency-footer {
  text-align: center;
  padding: 40rpx;
}

.footer-text {
  font-size: 26rpx;
  color: #666;
  font-style: italic;
}
</style>