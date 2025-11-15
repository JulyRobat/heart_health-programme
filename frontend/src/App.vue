<script setup>
import { onLaunch, onShow, onHide } from '@dcloudio/uni-app'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

onLaunch(() => {
  console.log('心晴港湾 App 启动')
  
  // 检查登录状态
  authStore.checkAuth()
})

onShow(() => {
  console.log('心晴港湾 App 显示')
})

onHide(() => {
  console.log('心晴港湾 App 隐藏')
})
</script>

<style>
/* 全局样式 */
page {
  background-color: #f5f5f5;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}

/* 统一按钮样式 */
button {
  border-radius: 12rpx;
}

button:active {
  opacity: 0.8;
}

/* 统一输入框样式 */
input {
  border-radius: 12rpx;
  padding: 20rpx;
  background: #f8f9fa;
  border: 2rpx solid #e8e8e8;
}

input:focus {
  border-color: #667eea;
  background: white;
}

/* 卡片阴影 */
.card-shadow {
  box-shadow: 0 4rpx 20rpx rgba(0,0,0,0.08);
}

/* 渐变背景 */
.gradient-bg {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
</style>