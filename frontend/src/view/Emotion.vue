<template>
  <MainLayout>
    <div class="emotion-container">
      <div class="emotion-content">
        <div class="analysis-header">
          <h2>情感分析报告</h2>
          <p>基于您与AI助手的对话分析</p>
        </div>

        <div class="time-filter">
          <el-radio-group v-model="activePeriod" @change="loadEmotionData">
            <el-radio-button label="7">最近7天</el-radio-button>
            <el-radio-button label="30">最近30天</el-radio-button>
            <el-radio-button label="90">最近90天</el-radio-button>
          </el-radio-group>
        </div>

        <div class="overview-cards">
          <el-card class="overview-card">
            <div class="card-content">
              <div class="score-display">
                <div class="score">{{ statistics.avg_emotion_score || '0.50' }}</div>
                <div class="score-label">平均情感得分</div>
              </div>
              <div class="status-info">
                <div class="status">{{ summary.status || '未知' }}</div>
                <div class="suggestion">{{ summary.suggestion || '暂无建议' }}</div>
              </div>
            </div>
          </el-card>
        </div>

        <div class="charts-section">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-card>
                <template #header>
                  <span>情感趋势</span>
                </template>
                <div class="chart-container">
                  <v-chart
                    v-if="trendChartData.series.length > 0"
                    :option="trendChartOption"
                    :autoresize="true"
                    style="height: 300px;"
                  />
                  <div v-else class="no-data">暂无数据</div>
                </div>
              </el-card>
            </el-col>
            <el-col :span="12">
              <el-card>
                <template #header>
                  <span>情感分布</span>
                </template>
                <div class="chart-container">
                  <v-chart
                    v-if="distributionChartData.series.length > 0"
                    :option="distributionChartOption"
                    :autoresize="true"
                    style="height: 300px;"
                  />
                  <div v-else class="no-data">暂无数据</div>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </div>

        <div class="keywords-section" v-if="statistics.keywords_cloud.length > 0">
          <el-card>
            <template #header>
              <span>关键词分析</span>
            </template>
            <div class="keywords-cloud">
              <el-tag
                v-for="keyword in statistics.keywords_cloud"
                :key="keyword.text"
                :type="getKeywordType(keyword.value)"
                class="keyword-tag"
              >
                {{ keyword.text }} ({{ keyword.value }})
              </el-tag>
            </div>
          </el-card>
        </div>

        <div class="records-section">
          <el-card>
            <template #header>
              <span>分析记录</span>
            </template>
            <div class="records-list">
              <div
                v-for="record in emotionRecords"
                :key="record.id"
                class="record-item"
                :class="record.emotion_type"
              >
                <div class="record-header">
                  <el-tag
                    :type="getEmotionTagType(record.emotion_type)"
                    size="small"
                  >
                    {{ getEmotionLabel(record.emotion_type) }}
                  </el-tag>
                  <span class="record-time">{{ formatRecordTime(record.created_at) }}</span>
                </div>
                <div class="keywords">
                  <el-tag
                    v-for="keyword in record.keywords"
                    :key="keyword"
                    type="info"
                    size="small"
                  >
                    #{{ keyword }}
                  </el-tag>
                </div>
                <div class="score-info">
                  <span>情感得分: {{ record.emotion_score }}</span>
                  <span>置信度: {{ (record.confidence * 100).toFixed(1) }}%</span>
                </div>
              </div>
            </div>
            <div v-if="emotionRecords.length === 0" class="no-records">
              暂无情感分析记录
            </div>
          </el-card>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, PieChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components'
import VChart from 'vue-echarts'
import { getEmotionHistory, getEmotionStatistics, getEmotionTrends } from '@/api/emotion'
import { ElMessage } from 'element-plus'
import MainLayout from '@/components/layout/MainLayout.vue'

use([
  CanvasRenderer,
  LineChart,
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
])

const activePeriod = ref('7')
const emotionRecords = ref([])
const statistics = ref({
  total_messages: 0,
  emotion_distribution: { positive: 0, negative: 0, neutral: 0 },
  avg_emotion_score: 0,
  trend: 'stable',
  keywords_cloud: []
})
const summary = ref({})
const trendsData = ref([])

const trendChartData = computed(() => {
  return {
    dates: trendsData.value.map(t => t.date),
    series: [{
      name: '情感得分',
      data: trendsData.value.map(t => t.avg_score)
    }]
  }
})

const distributionChartData = computed(() => {
  const dist = statistics.value.emotion_distribution
  return {
    series: [{
      data: [
        { name: '积极', value: dist.positive },
        { name: '中性', value: dist.neutral },
        { name: '消极', value: dist.negative }
      ]
    }]
  }
})

const trendChartOption = computed(() => {
  return {
    tooltip: {
      trigger: 'axis',
      formatter: (params) => {
        const data = params[0]
        return `${data.name}<br/>情感得分: ${data.value}`
      }
    },
    xAxis: {
      type: 'category',
      data: trendChartData.value.dates
    },
    yAxis: {
      type: 'value',
      min: 0,
      max: 1,
      axisLabel: {
        formatter: (value) => value.toFixed(1)
      }
    },
    series: [{
      name: '情感得分',
      type: 'line',
      data: trendChartData.value.series[0].data,
      smooth: true,
      itemStyle: {
        color: '#3B82F6'
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [{
            offset: 0,
            color: 'rgba(59, 130, 246, 0.3)'
          }, {
            offset: 1,
            color: 'rgba(59, 130, 246, 0.1)'
          }]
        }
      }
    }],
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    }
  }
})

const distributionChartOption = computed(() => {
  return {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [{
      name: '情感分布',
      type: 'pie',
      radius: '50%',
      data: distributionChartData.value.series[0].data,
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      },
      itemStyle: {
        color: (params) => {
          const colors = {
            '积极': '#10B981',
            '中性': '#3B82F6',
            '消极': '#F59E0B'
          }
          return colors[params.name] || '#999'
        }
      }
    }]
  }
})

const getEmotionLabel = (type) => {
  const labels = {
    'positive': '积极',
    'negative': '消极',
    'neutral': '中性'
  }
  return labels[type] || type
}

const getEmotionTagType = (type) => {
  const types = {
    'positive': 'success',
    'negative': 'warning',
    'neutral': 'info'
  }
  return types[type] || 'info'
}

const getKeywordType = (value) => {
  if (value > 5) return 'danger'
  if (value > 2) return 'warning'
  return 'info'
}

const formatRecordTime = (timeStr) => {
  const date = new Date(timeStr)
  return `${date.getMonth() + 1}/${date.getDate()} ${date.getHours()}:${date.getMinutes().toString().padStart(2, '0')}`
}

const loadEmotionData = async () => {
  try {
    const [historyRes, statsRes, trendsRes] = await Promise.all([
      getEmotionHistory({ days: parseInt(activePeriod.value) }),
      getEmotionStatistics(),
      getEmotionTrends({ days: parseInt(activePeriod.value) })
    ])

    if (historyRes.success) {
      emotionRecords.value = historyRes.records
      summary.value = historyRes.summary
    }

    if (statsRes.success) {
      statistics.value = statsRes.statistics
    }

    if (trendsRes.success) {
      trendsData.value = trendsRes.trends
    }
  } catch (error) {
    ElMessage.error('加载情感数据失败')
    console.error('加载情感数据失败:', error)
  }
}

onMounted(() => {
  loadEmotionData()
})
</script>

<style scoped lang="scss">
.emotion-container {
  height: 100%;
  overflow-y: auto;
}

.emotion-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}

.analysis-header {
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

.time-filter {
  display: flex;
  justify-content: center;
  margin-bottom: 32px;
}

.overview-cards {
  margin-bottom: 32px;
}

.overview-card {
  .card-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px;
  }
}

.score-display {
  text-align: center;
  
  .score {
    font-size: 48px;
    font-weight: bold;
    color: var(--primary-color);
    line-height: 1;
  }
  
  .score-label {
    color: var(--text-secondary);
    font-size: 14px;
    margin-top: 8px;
  }
}

.status-info {
  flex: 1;
  margin-left: 32px;
  
  .status {
    font-size: 20px;
    font-weight: bold;
    color: var(--text-primary);
    margin-bottom: 8px;
  }
  
  .suggestion {
    color: var(--text-secondary);
    line-height: 1.5;
  }
}

.charts-section {
  margin-bottom: 32px;
}

.chart-container {
  position: relative;
}

.no-data {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 300px;
  color: var(--text-light);
  font-size: 16px;
}

.keywords-section {
  margin-bottom: 32px;
}

.keywords-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.keyword-tag {
  margin: 4px;
}

.records-section {
  margin-bottom: 32px;
}

.records-list {
  max-height: 400px;
  overflow-y: auto;
}

.record-item {
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 12px;
  border-left: 4px solid var(--border-color);
  
  &.positive {
    border-left-color: var(--success-color);
    background-color: rgba(16, 185, 129, 0.05);
  }
  
  &.negative {
    border-left-color: var(--warning-color);
    background-color: rgba(245, 158, 11, 0.05);
  }
  
  &.neutral {
    border-left-color: var(--primary-color);
    background-color: rgba(59, 130, 246, 0.05);
  }
}

.record-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.record-time {
  color: var(--text-light);
  font-size: 12px;
}

.keywords {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 8px;
}

.score-info {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: var(--text-secondary);
}

.no-records {
  text-align: center;
  padding: 40px;
  color: var(--text-light);
  font-size: 16px;
}

@media (max-width: 768px) {
  .emotion-content {
    padding: 16px;
  }
  
  .card-content {
    flex-direction: column;
    text-align: center;
  }
  
  .status-info {
    margin-left: 0;
    margin-top: 16px;
  }
  
  .charts-section {
    .el-col {
      margin-bottom: 16px;
    }
  }
}
</style>