<template>
  <view class="knowledge-container">
    <view class="search-section">
      <view class="search-box">
        <input 
          v-model="searchKeyword" 
          class="search-input" 
          placeholder="搜索心理健康知识..." 
          @input="handleSearch"
        />
        <text class="search-icon">🔍</text>
      </view>
    </view>
    
    <view class="category-tabs">
      <scroll-view class="category-scroll" scroll-x>
        <view 
          v-for="category in categories" 
          :key="category.id"
          :class="['category-tab', { active: activeCategory === category.id }]"
          @click="setActiveCategory(category.id)"
        >
          <text class="category-icon">{{ category.icon }}</text>
          <text class="category-name">{{ category.name }}</text>
        </view>
      </scroll-view>
    </view>
    
    <view class="featured-articles" v-if="activeCategory === 'all' && !searchKeyword">
      <view class="section-header">
        <text class="section-title">精选推荐</text>
      </view>
      
      <scroll-view class="featured-scroll" scroll-x>
        <view 
          v-for="article in featuredArticles" 
          :key="article.id"
          class="featured-card"
          @click="viewArticle(article)"
        >
          <view class="featured-badge">推荐</view>
          <view class="featured-content">
            <text class="featured-title">{{ article.title }}</text>
            <text class="featured-desc">{{ article.description }}</text>
            <view class="featured-meta">
              <text class="meta-item">{{ article.read_time }}分钟阅读</text>
              <text class="meta-item">{{ article.category }}</text>
            </view>
          </view>
        </view>
      </scroll-view>
    </view>
    
    <view class="articles-section">
      <view class="section-header" v-if="activeCategory !== 'all' || searchKeyword">
        <text class="section-title">
          {{ activeCategory !== 'all' ? getCategoryName(activeCategory) : '搜索结果' }}
        </text>
        <text class="article-count">{{ filteredArticles.length }}篇文章</text>
      </view>
      
      <scroll-view class="articles-list" scroll-y>
        <view 
          v-for="article in filteredArticles" 
          :key="article.id"
          class="article-card"
          @click="viewArticle(article)"
        >
          <view class="article-header">
            <text class="article-title">{{ article.title }}</text>
            <view class="article-category">{{ article.category }}</view>
          </view>
          
          <text class="article-summary">{{ article.summary }}</text>
          
          <view class="article-footer">
            <view class="article-meta">
              <text class="meta-author">{{ article.author }}</text>
              <text class="meta-date">{{ formatDate(article.created_at) }}</text>
              <text class="meta-read">{{ article.read_count }}人阅读</text>
            </view>
            <view class="article-actions">
              <text class="action-icon" @click.stop="toggleLike(article)">
                {{ article.liked ? '❤️' : '🤍' }}
              </text>
              <text class="action-icon">📖</text>
            </view>
          </view>
          
          <view class="article-tags" v-if="article.tags && article.tags.length">
            <text 
              v-for="tag in article.tags" 
              :key="tag"
              class="article-tag"
            >
              {{ tag }}
            </text>
          </view>
        </view>
        
        <view v-if="filteredArticles.length === 0" class="empty-articles">
          <text class="empty-icon">📚</text>
          <text class="empty-text">暂无相关文章</text>
          <text class="empty-desc">换个关键词试试看</text>
        </view>
      </scroll-view>
    </view>
    
    <view class="quick-help">
      <view class="help-header">
        <text class="help-title">快速帮助</text>
      </view>
      <view class="help-buttons">
        <button class="help-btn" @click="contactSupport">
          <text class="btn-icon">💬</text>
          <text class="btn-text">在线咨询</text>
        </button>
        <button class="help-btn" @click="viewHotline">
          <text class="btn-icon">📞</text>
          <text class="btn-text">心理热线</text>
        </button>
        <button class="help-btn" @click="takeTest">
          <text class="btn-icon">📝</text>
          <text class="btn-text">心理测评</text>
        </button>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const searchKeyword = ref('')
const activeCategory = ref('all')
const articles = ref([])
const featuredArticles = ref([])

const categories = ref([
  { id: 'all', name: '全部', icon: '📚' },
  { id: 'stress', name: '压力管理', icon: '😰' },
  { id: 'anxiety', name: '焦虑应对', icon: '😥' },
  { id: 'depression', name: '抑郁情绪', icon: '😔' },
  { id: 'sleep', name: '睡眠健康', icon: '😴' },
  { id: 'relationship', name: '人际关系', icon: '👥' },
  { id: 'study', name: '学习压力', icon: '📖' },
  { id: 'emotion', name: '情绪管理', icon: '😊' }
])

const loadArticles = () => {
  // 模拟文章数据
  articles.value = [
    {
      id: 1,
      title: '如何有效应对学习压力',
      summary: '学习压力是学生常见的问题，本文介绍了多种有效的压力管理技巧，包括时间管理、放松训练和认知调整等方法。',
      description: '详细讲解学习压力的成因和应对策略',
      category: '压力管理',
      author: '心理咨询中心',
      created_at: '2024-11-10',
      read_count: 1245,
      read_time: 8,
      liked: false,
      tags: ['学习', '压力', '时间管理']
    },
    {
      id: 2,
      title: '改善睡眠质量的10个方法',
      summary: '良好的睡眠对心理健康至关重要，本文提供了10个实用的改善睡眠质量的建议，帮助您获得更好的休息。',
      description: '提升睡眠质量的实用技巧',
      category: '睡眠健康',
      author: '心理咨询中心',
      created_at: '2024-11-08',
      read_count: 892,
      read_time: 6,
      liked: true,
      tags: ['睡眠', '健康', '作息']
    },
    {
      id: 3,
      title: '焦虑情绪的自我调节技巧',
      summary: '当感到焦虑时，可以尝试这些简单有效的自我调节技巧，帮助您平静心情，恢复内心平衡。',
      description: '焦虑情绪的实用应对方法',
      category: '焦虑应对',
      author: '心理咨询中心',
      created_at: '2024-11-05',
      read_count: 1567,
      read_time: 5,
      liked: false,
      tags: ['焦虑', '调节', '放松']
    },
    {
      id: 4,
      title: '建立健康人际关系的要点',
      summary: '良好的人际关系是心理健康的重要保障，本文介绍了建立和维护健康人际关系的几个关键要点。',
      description: '人际关系的建立和维护技巧',
      category: '人际关系',
      author: '心理咨询中心',
      created_at: '2024-11-01',
      read_count: 734,
      read_time: 7,
      liked: false,
      tags: ['人际关系', '沟通', '社交']
    },
    {
      id: 5,
      title: '认识抑郁情绪的常见表现',
      summary: '了解抑郁情绪的常见表现有助于早期识别和干预，本文详细介绍了抑郁情绪的各种表现特征。',
      description: '抑郁情绪的识别和认识',
      category: '抑郁情绪',
      author: '心理咨询中心',
      created_at: '2024-10-28',
      read_count: 1983,
      read_time: 10,
      liked: true,
      tags: ['抑郁', '情绪', '识别']
    }
  ]
  
  // 精选文章
  featuredArticles.value = [
    articles.value[0],
    articles.value[1],
    articles.value[2]
  ]
}

const filteredArticles = computed(() => {
  let result = articles.value
  
  // 按分类过滤
  if (activeCategory.value !== 'all') {
    const categoryName = categories.value.find(cat => cat.id === activeCategory.value)?.name
    result = result.filter(article => article.category === categoryName)
  }
  
  // 按关键词搜索
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    result = result.filter(article => 
      article.title.toLowerCase().includes(keyword) || 
      article.summary.toLowerCase().includes(keyword) ||
      article.tags.some(tag => tag.toLowerCase().includes(keyword))
    )
  }
  
  return result
})

const handleSearch = () => {
  // 搜索逻辑已在计算属性中处理
}

const setActiveCategory = (categoryId) => {
  activeCategory.value = categoryId
}

const getCategoryName = (categoryId) => {
  return categories.value.find(cat => cat.id === categoryId)?.name || ''
}

const viewArticle = (article) => {
  uni.navigateTo({
    url: `/pages/knowledge/article?id=${article.id}`,
    success: () => {
      // 可以在这里传递文章数据
    }
  })
}

const toggleLike = (article) => {
  article.liked = !article.liked
  uni.showToast({
    title: article.liked ? '已收藏' : '已取消收藏',
    icon: 'success'
  })
}

const formatDate = (dateStr) => {
  return dateStr
}

const contactSupport = () => {
  uni.navigateTo({ url: '/pages/chat/chat' })
}

const viewHotline = () => {
  uni.navigateTo({ url: '/pages/emergency/emergency' })
}

const takeTest = () => {
  uni.showModal({
    title: '心理测评',
    content: '心理测评功能将在后续版本开放',
    showCancel: false
  })
}

onMounted(() => {
  loadArticles()
})
</script>

<style scoped>
.knowledge-container {
  padding: 40rpx;
  min-height: 100vh;
  background: #f5f7fa;
}

.search-section {
  margin-bottom: 40rpx;
}

.search-box {
  position: relative;
  background: white;
  border-radius: 25rpx;
  padding: 20rpx 30rpx;
  box-shadow: 0 4rpx 20rpx rgba(0,0,0,0.06);
}

.search-input {
  font-size: 28rpx;
  padding-right: 60rpx;
}

.search-icon {
  position: absolute;
  right: 30rpx;
  top: 50%;
  transform: translateY(-50%);
  font-size: 28rpx;
  color: #999;
}

.category-tabs {
  margin-bottom: 40rpx;
}

.category-scroll {
  white-space: nowrap;
}

.category-tab {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  padding: 20rpx 25rpx;
  background: white;
  border-radius: 20rpx;
  margin-right: 20rpx;
  min-width: 120rpx;
  box-shadow: 0 2rpx 10rpx rgba(0,0,0,0.06);
}

.category-tab.active {
  background: #667eea;
  color: white;
}

.category-icon {
  font-size: 36rpx;
  margin-bottom: 10rpx;
}

.category-name {
  font-size: 22rpx;
}

.featured-articles {
  margin-bottom: 40rpx;
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

.article-count {
  font-size: 24rpx;
  color: #999;
}

.featured-scroll {
  white-space: nowrap;
}

.featured-card {
  display: inline-block;
  width: 400rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20rpx;
  padding: 40rpx;
  margin-right: 25rpx;
  color: white;
  position: relative;
}

.featured-badge {
  position: absolute;
  top: 20rpx;
  right: 20rpx;
  background: rgba(255,255,255,0.2);
  padding: 8rpx 16rpx;
  border-radius: 12rpx;
  font-size: 20rpx;
}

.featured-content {
  height: 180rpx;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.featured-title {
  font-size: 28rpx;
  font-weight: bold;
  margin-bottom: 15rpx;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.featured-desc {
  font-size: 22rpx;
  opacity: 0.9;
  margin-bottom: 15rpx;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.featured-meta {
  display: flex;
  gap: 20rpx;
  font-size: 20rpx;
  opacity: 0.8;
}

.articles-section {
  flex: 1;
}

.articles-list {
  height: calc(100vh - 600rpx);
}

.article-card {
  background: white;
  border-radius: 20rpx;
  padding: 40rpx;
  margin-bottom: 30rpx;
  box-shadow: 0 4rpx 20rpx rgba(0,0,0,0.06);
}

.article-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20rpx;
}

.article-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  flex: 1;
  margin-right: 20rpx;
  line-height: 1.4;
}

.article-category {
  background: #667eea;
  color: white;
  padding: 8rpx 16rpx;
  border-radius: 12rpx;
  font-size: 22rpx;
  flex-shrink: 0;
}

.article-summary {
  font-size: 26rpx;
  color: #666;
  line-height: 1.5;
  margin-bottom: 25rpx;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.article-meta {
  display: flex;
  gap: 20rpx;
  font-size: 22rpx;
  color: #999;
}

.article-actions {
  display: flex;
  gap: 20rpx;
}

.action-icon {
  font-size: 28rpx;
  padding: 8rpx;
}

.article-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 15rpx;
}

.article-tag {
  background: #f0f2f5;
  color: #666;
  padding: 8rpx 16rpx;
  border-radius: 15rpx;
  font-size: 22rpx;
}

.empty-articles {
  text-align: center;
  padding: 100rpx 40rpx;
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

.quick-help {
  background: white;
  border-radius: 20rpx;
  padding: 40rpx;
  margin-top: 40rpx;
  box-shadow: 0 4rpx 20rpx rgba(0,0,0,0.06);
}

.help-header {
  margin-bottom: 30rpx;
}

.help-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
}

.help-buttons {
  display: flex;
  justify-content: space-between;
}

.help-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #f8f9fa;
  border: none;
  border-radius: 15rpx;
  padding: 25rpx 20rpx;
  flex: 1;
  margin: 0 10rpx;
}

.btn-icon {
  font-size: 40rpx;
  margin-bottom: 10rpx;
}

.btn-text {
  font-size: 24rpx;
  color: #333;
}
</style>