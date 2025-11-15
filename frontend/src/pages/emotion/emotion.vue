<template>
  <view class="emotion-container">
    <view class="header-section">
      <text class="title">情感分析报告</text>
      <text class="subtitle">基于AI情感计算的心理状态分析</text>
    </view>
    
    <view class="stats-overview">
      <view class="stat-item">
        <text class="stat-value">{{ emotionStats.average_score?.toFixed(1) || '--' }}</text>
        <text class="stat-label">平均情绪指数</text>
      </view>
      <view class="stat-item">
        <text class="stat-value">{{ emotionStats.positive_days || 0 }}</text>
        <text class="stat-label">积极天数</text>
      </view>
      <view class="stat-item">
        <text class="stat-value">{{ emotionStats.negative_days || 0 }}</text>
        <text class="stat-label">关注天数</text>
      </view>
    </view>
    
    <view class="chart-section">
      <view class="section-header">
        <text class="section-title">情绪波动趋势</text>
        <view class="time-filter">
          <text 
            v-for="period in timePeriods" 
            :key="period.value"
            :class="['period-tab', { active: currentPeriod === period.value }]"
            @click="changePeriod(period.value)"
          >
            {{ period.label }}
          </text>
        </view>
      </view>
      
      <view class="chart-container">
        <canvas canvas-id="emotionChart" class="emotion-chart"></canvas>
      </view>
      
      <view class="chart-legend">
        <view class="legend-item">
          <view class="legend-color positive"></view>
          <text>积极 (7-10分)</text>
        </view>
        <view class="legend-item">
          <view class="legend-color neutral"></view>
          <text>一般 (4-6分)</text>
        </view>
        <view class="legend-item">
          <view class="legend-color negative"></view>
          <text>关注 (0-3分)</text>
        </view>
      </view>
    </view>
    
    <view class="insights-section">
      <view class="section-header">
        <text class="section-title">AI分析洞察</text>
      </view>
      
      <view class="insight-cards">
        <view class="insight-card positive" v-if="currentInsight.type === 'positive'">
          <view class="insight-icon">😊</view>
          <view class="insight-content">
            <text class="insight-title">情绪状态良好</text>
            <text class="insight-desc">近期您的情绪状态比较稳定，继续保持积极心态！</text>
          </view>
        </view>
        
        <view class="insight-card neutral" v-else-if="currentInsight.type === 'neutral'">
          <view class="insight-icon">😐</view>
          <view class="insight-content">
            <text class="insight-title">情绪波动正常</text>
            <text class="insight-desc">情绪有轻微波动，建议多关注自我调节。</text>
          </view>
        </view>
        
        <view class="insight-card negative" v-else>
          <view class="insight-icon">😔</view>
          <view class="insight-content">
            <text class="insight-title">需要关注</text>
            <text class="insight-desc">检测到情绪较低，建议与AI助手多交流或寻求支持。</text>
          </view>
        </view>
      </view>
      
      <view class="recommendations">
        <text class="recommend-title">个性化建议</text>
        <view class="recommend-list">
          <view class="recommend-item" v-for="(item, index) in recommendations" :key="index">
            <text class="recommend-number">{{ index + 1 }}</text>
            <text class="recommend-text">{{ item }}</text>
          </view>
        </view>
      </view>
    </view>
    
    <view class="detailed-records">
      <view class="section-header">
        <text class="section-title">详细记录</text>
      </view>
      
      <scroll-view class="records-list" scroll-y>
        <view 
          v-for="record in emotionRecords" 
          :key="record.id"
          class="record-item"
        >
          <view class="record-date">
            <text class="date">{{ formatRecordDate(record.date) }}</text>
            <text class="time">{{ record.time }}</text>
          </view>
          <view class="record-details">
            <text class="record-content">{{ record.content }}</text>
            <view class="record-score">
              <text class="score-value">{{ record.score.toFixed(1) }}</text>
              <view class="score-bar">
                <view 
                  class="score-fill" 
                  :style="{ width: (record.score * 10) + '%' }"
                  :class="getScoreClass(record.score)"
                ></view>
              </view>
            </view>
          </view>
        </view>
        
        <view v-if="emotionRecords.length === 0" class="empty-records">
          <text class="empty-icon">📊</text>
          <text class="empty-text">暂无情感分析记录</text>
          <text class="empty-desc">开始与AI助手对话，生成您的情绪分析报告</text>
        </view>
      </scroll-view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

const currentPeriod = ref('week')
const emotionStats = ref({})
const emotionRecords = ref([])
const currentInsight = ref({})

const timePeriods = [
  { label: '近7天', value: 'week' },
  { label: '近30天', value: 'month' },
  { label: '近3月', value: 'quarter' }
]

const recommendations = ref([
  '每天保持30分钟户外活动',
  '尝试正念冥想练习',
  '与朋友家人保持联系',
  '保证7-8小时充足睡眠',
  '记录每日情绪变化'
])

const loadEmotionData = () => {
  // 模拟情感统计数据
  emotionStats.value = {
    average_score: 6.8,
    positive_days: 18,
    negative_days: 3,
    total_records: 45
  }
  
  // 模拟情感记录
  emotionRecords.value = [
    {
      id: 1,
      date: '2024-11-15',
      time: '14:30',
      content: '今天完成了项目展示，感觉很有成就感',
      score: 8.5
    },
    {
      id: 2,
      date: '2024-11-14',
      time: '20:15',
      content: '晚上学习效率不高，有些焦虑',
      score: 4.2
    },
    {
      id: 3,
      date: '2024-11-13',
      time: '09:45',
      content: '早晨运动后心情很好，充满活力',
      score: 9.1
    },
    {
      id: 4,
      date: '2024-11-12',
      time: '16:20',
      content: '小组讨论时有些意见分歧，心情受影响',
      score: 5.8
    },
    {
      id: 5,
      date: '2024-11-11',
      time: '11:30',
      content: '收到朋友的关心消息，感觉很温暖',
      score: 7.9
    }
  ]
  
  // 根据平均分设置洞察
  const avgScore = emotionStats.value.average_score
  if (avgScore >= 7) {
    currentInsight.value = { type: 'positive', message: '情绪状态良好' }
  } else if (avgScore >= 5) {
    currentInsight.value = { type: 'neutral', message: '情绪波动正常' }
  } else {
    currentInsight.value = { type: 'negative', message: '需要关注情绪状态' }
  }
  
  drawEmotionChart()
}

const changePeriod = (period) => {
  currentPeriod.value = period
  loadEmotionData() // 重新加载数据
}

const formatRecordDate = (dateStr) => {
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}月${date.getDate()}日`
}

const getScoreClass = (score) => {
  if (score >= 7) return 'positive'
  if (score >= 4) return 'neutral'
  return 'negative'
}

const drawEmotionChart = () => {
  // 模拟图表数据
  const chartData = [
    { day: '11-09', score: 7.2 },
    { day: '11-10', score: 6.8 },
    { day: '11-11', score: 8.1 },
    { day: '11-12', score: 5.5 },
    { day: '11-13', score: 7.9 },
    { day: '11-14', score: 6.3 },
    { day: '11-15', score: 7.1 }
  ]
  
  const ctx = uni.createCanvasContext('emotionChart')
  const width = 600
  const height = 200
  const padding = 40
  
  // 清空画布
  ctx.clearRect(0, 0, width, height)
  
  // 绘制网格线
  ctx.setStrokeStyle('#e8e8e8')
  ctx.setLineWidth(1)
  
  // 水平网格线
  for (let i = 0; i <= 10; i++) {
    const y = padding + (i * (height - 2 * padding)) / 10
    ctx.moveTo(padding, y)
    ctx.lineTo(width - padding, y)
  }
  ctx.stroke()
  
  // 绘制数据线
  ctx.setStrokeStyle('#667eea')
  ctx.setLineWidth(3)
  
  chartData.forEach((point, index) => {
    const x = padding + (index * (width - 2 * padding)) / (chartData.length - 1)
    const y = height - padding - (point.score * (height - 2 * padding)) / 10
    
    if (index === 0) {
      ctx.moveTo(x, y)
    } else {
      ctx.lineTo(x, y)
    }
    
    // 绘制数据点
    ctx.setFillStyle('#667eea')
    ctx.beginPath()
    ctx.arc(x, y, 4, 0, 2 * Math.PI)
    ctx.fill()
  })
  
  ctx.stroke()
  
  // 绘制坐标轴标签
  ctx.setFillStyle('#666')
  ctx.setFontSize(20)
  
  // X轴标签
  chartData.forEach((point, index) => {
    const x = padding + (index * (width - 2 * padding)) / (chartData.length - 1)
    ctx.fillText(point.day, x - 15, height - padding + 20)
  })
  
  // Y轴标签
  for (let i = 0; i <= 10; i++) {
    const y = height - padding - (i * (height - 2 * padding)) / 10
    ctx.fillText(i.toString(), padding - 20, y + 5)
  }
  
  ctx.draw()
}

onMounted(() => {
  loadEmotionData()
})
</script>

<style scoped>
.emotion-container {
  padding: 40rpx;
  min-height: 100vh;
  background: linear-gradient(180deg, #f5f7fa 0%, #ffffff 100%);
}

.header-section {
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

.stats-overview {
  display: flex;
  justify-content: space-between;
  margin-bottom: 50rpx;
  background: white;
  border-radius: 20rpx;
  padding: 40rpx;
  box-shadow: 0 4rpx 20rpx rgba(0,0,0,0.06);
}

.stat-item {
  text-align: center;
  flex: 1;
}

.stat-value {
  display: block;
  font-size: 42rpx;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 8rpx;
}

.stat-label {
  font-size: 24rpx;
  color: #666;
}

.chart-section {
  background: white;
  border-radius: 20rpx;
  padding: 40rpx;
  margin-bottom: 40rpx;
  box-shadow: 0 4rpx 20rpx rgba(0,0,0,0.06);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.time-filter {
  display: flex;
  background: #f8f9fa;
  border-radius: 20rpx;
  padding: 8rpx;
}

.period-tab {
  padding: 12rpx 20rpx;
  font-size: 24rpx;
  color: #666;
  border-radius: 16rpx;
}

.period-tab.active {
  background: #667eea;
  color: white;
}

.chart-container {
  margin: 30rpx 0;
}

.emotion-chart {
  width: 100%;
  height: 200rpx;
}

.chart-legend {
  display: flex;
  justify-content: center;
  gap: 30rpx;
  margin-top: 20rpx;
}

.legend-item {
  display: flex;
  align-items: center;
  font-size: 24rpx;
  color: #666;
}

.legend-color {
  width: 20rpx;
  height: 20rpx;
  border-radius: 4rpx;
  margin-right: 10rpx;
}

.legend-color.positive {
  background: #52c41a;
}

.legend-color.neutral {
  background: #faad14;
}

.legend-color.negative {
  background: #f5222d;
}

.insights-section {
  background: white;
  border-radius: 20rpx;
  padding: 40rpx;
  margin-bottom: 40rpx;
  box-shadow: 0 4rpx 20rpx rgba(0,0,0,0.06);
}

.insight-cards {
  margin-bottom: 40rpx;
}

.insight-card {
  display: flex;
  align-items: center;
  padding: 30rpx;
  border-radius: 16rpx;
  margin-bottom: 20rpx;
}

.insight-card.positive {
  background: linear-gradient(135deg, #f6ffed 0%, #e6f7ff 100%);
  border-left: 6rpx solid #52c41a;
}

.insight-card.neutral {
  background: linear-gradient(135deg, #fffbe6 0%, #fff2e8 100%);
  border-left: 6rpx solid #faad14;
}

.insight-card.negative {
  background: linear-gradient(135deg, #fff2f0 0%, #f9f0ff 100%);
  border-left: 6rpx solid #f5222d;
}

.insight-icon {
  font-size: 48rpx;
  margin-right: 25rpx;
}

.insight-content {
  flex: 1;
}

.insight-title {
  display: block;
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 8rpx;
}

.insight-desc {
  font-size: 24rpx;
  color: #666;
  line-height: 1.4;
}

.recommendations {
  border-top: 1rpx solid #f0f0f0;
  padding-top: 30rpx;
}

.recommend-title {
  display: block;
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 25rpx;
}

.recommend-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.recommend-item {
  display: flex;
  align-items: flex-start;
}

.recommend-number {
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

.recommend-text {
  font-size: 26rpx;
  color: #333;
  line-height: 1.5;
  flex: 1;
}

.detailed-records {
  background: white;
  border-radius: 20rpx;
  padding: 40rpx;
  box-shadow: 0 4rpx 20rpx rgba(0,0,0,0.06);
}

.records-list {
  max-height: 600rpx;
}

.record-item {
  display: flex;
  padding: 25rpx 0;
  border-bottom: 1rpx solid #f0f0f0;
}

.record-item:last-child {
  border-bottom: none;
}

.record-date {
  width: 120rpx;
  flex-shrink: 0;
  margin-right: 25rpx;
}

.date {
  display: block;
  font-size: 26rpx;
  color: #333;
  font-weight: bold;
  margin-bottom: 5rpx;
}

.time {
  font-size: 22rpx;
  color: #999;
}

.record-details {
  flex: 1;
}

.record-content {
  display: block;
  font-size: 26rpx;
  color: #333;
  margin-bottom: 15rpx;
  line-height: 1.4;
}

.record-score {
  display: flex;
  align-items: center;
}

.score-value {
  font-size: 24rpx;
  color: #666;
  margin-right: 15rpx;
  width: 40rpx;
}

.score-bar {
  flex: 1;
  height: 8rpx;
  background: #f0f0f0;
  border-radius: 4rpx;
  overflow: hidden;
}

.score-fill {
  height: 100%;
  transition: width 0.3s ease;
}

.score-fill.positive {
  background: #52c41a;
}

.score-fill.neutral {
  background: #faad14;
}

.score-fill.negative {
  background: #f5222d;
}

.empty-records {
  text-align: center;
  padding: 80rpx 40rpx;
}

.empty-icon {
  font-size: 80rpx;
  display: block;
  margin-bottom: 20rpx;
}

.empty-text {
  display: block;
  font-size: 28rpx;
  color: #333;
  margin-bottom: 10rpx;
}

.empty-desc {
  font-size: 24rpx;
  color: #999;
}
</style>