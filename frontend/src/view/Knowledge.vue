<template>
  <MainLayout>
    <div class="knowledge-container">
      <div class="knowledge-content">
        <div class="knowledge-header">
          <h2>心理健康知识库</h2>
          <p>专业心理健康知识和实用技巧</p>
        </div>

        <div class="search-section">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索文章..."
            :prefix-icon="Search"
            clearable
            @input="handleSearch"
          />
        </div>

        <div class="categories-section">
          <el-radio-group v-model="activeCategory" @change="filterArticles">
            <el-radio-button label="">全部</el-radio-button>
            <el-radio-button label="焦虑应对">焦虑应对</el-radio-button>
            <el-radio-button label="情绪管理">情绪管理</el-radio-button>
            <el-radio-button label="压力管理">压力管理</el-radio-button>
            <el-radio-button label="人际关系">人际关系</el-radio-button>
          </el-radio-group>
        </div>

        <div class="articles-grid">
          <el-card
            v-for="article in filteredArticles"
            :key="article.id"
            class="article-card"
            shadow="hover"
          >
            <div class="article-header">
              <div class="article-category">
                <el-tag :type="getCategoryType(article.category)" size="small">
                  {{ article.category }}
                </el-tag>
              </div>
              <div class="article-date">
                {{ formatDate(article.created_at) }}
              </div>
            </div>
            
            <h3 class="article-title">{{ article.title }}</h3>
            
            <p class="article-excerpt">{{ article.excerpt }}</p>
            
            <div class="article-footer">
              <div class="article-author">
                <el-icon><User /></el-icon>
                <span>{{ article.author }}</span>
              </div>
              <el-button type="primary" text @click="viewArticle(article)">
                阅读全文
                <el-icon><ArrowRight /></el-icon>
              </el-button>
            </div>
          </el-card>
        </div>

        <div v-if="filteredArticles.length === 0" class="no-articles">
          <el-empty description="暂无相关文章" />
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Search, User, ArrowRight } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import MainLayout from '@/components/layout/MainLayout.vue'

const searchKeyword = ref('')
const activeCategory = ref('')
const articles = ref([])

const mockArticles = [
  {
    id: 1,
    title: '如何有效应对学习焦虑',
    excerpt: '学习焦虑是学生常见的心理问题，本文介绍几种实用的方法帮助你缓解焦虑情绪，提高学习效率。',
    category: '焦虑应对',
    author: '心理咨询中心',
    created_at: '2023-07-10',
    content: '详细内容...'
  },
  {
    id: 2,
    title: '情绪管理的五个关键步骤',
    excerpt: '掌握情绪管理技巧对维护心理健康至关重要。本文将介绍五个实用步骤，帮助你更好地管理自己的情绪。',
    category: '情绪管理',
    author: '心理健康专家',
    created_at: '2023-07-05',
    content: '详细内容...'
  },
  {
    id: 3,
    title: '如何建立健康的人际关系',
    excerpt: '良好的人际关系是心理健康的重要组成部分。本文将分享一些建立和维护健康人际关系的实用建议。',
    category: '人际关系',
    author: '心理咨询师',
    created_at: '2023-06-28',
    content: '详细内容...'
  },
  {
    id: 4,
    title: '高效学习与压力平衡的艺术',
    excerpt: '如何在保持高效学习的同时，避免过度压力对身心健康的影响？本文提供实用的时间管理和压力调节技巧。',
    category: '压力管理',
    author: '学业指导老师',
    created_at: '2023-06-20',
    content: '详细内容...'
  },
  {
    id: 5,
    title: '正念冥想缓解焦虑',
    excerpt: '正念冥想是一种有效的焦虑缓解方法。学习如何通过正念练习来平静心灵，减少焦虑感。',
    category: '焦虑应对',
    author: '冥想导师',
    created_at: '2023-06-15',
    content: '详细内容...'
  },
  {
    id: 6,
    title: '改善睡眠质量的实用技巧',
    excerpt: '良好的睡眠对心理健康至关重要。了解如何改善睡眠质量，提升白天的精力和情绪状态。',
    category: '情绪管理',
    author: '睡眠专家',
    created_at: '2023-06-10',
    content: '详细内容...'
  }
]

const filteredArticles = computed(() => {
  let filtered = articles.value

  if (activeCategory.value) {
    filtered = filtered.filter(article => article.category === activeCategory.value)
  }

  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    filtered = filtered.filter(article => 
      article.title.toLowerCase().includes(keyword) ||
      article.excerpt.toLowerCase().includes(keyword) ||
      article.content.toLowerCase().includes(keyword)
    )
  }

  return filtered
})

const getCategoryType = (category) => {
  const types = {
    '焦虑应对': 'warning',
    '情绪管理': 'success',
    '压力管理': 'danger',
    '人际关系': 'primary'
  }
  return types[category] || 'info'
}

const formatDate = (dateStr) => {
  return dateStr
}

const handleSearch = () => {
  // 搜索逻辑已在 computed 中处理
}

const filterArticles = () => {
  // 分类筛选逻辑已在 computed 中处理
}

const viewArticle = (article) => {
  ElMessage.info(`查看文章: ${article.title}`)
  // 在实际应用中，这里可以跳转到文章详情页
}

onMounted(() => {
  articles.value = mockArticles
})
</script>

<style scoped lang="scss">
.knowledge-container {
  height: 100%;
  overflow-y: auto;
}

.knowledge-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}

.knowledge-header {
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

.search-section {
  max-width: 400px;
  margin: 0 auto 32px;
}

.categories-section {
  display: flex;
  justify-content: center;
  margin-bottom: 32px;
}

.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.article-card {
  height: 100%;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-4px);
  }
}

.article-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.article-date {
  color: var(--text-light);
  font-size: 12px;
}

.article-title {
  font-size: 18px;
  font-weight: bold;
  color: var(--text-primary);
  margin-bottom: 12px;
  line-height: 1.4;
}

.article-excerpt {
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 16px;
}

.article-author {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--text-light);
  font-size: 12px;
}

.no-articles {
  text-align: center;
  padding: 40px 0;
}

@media (max-width: 768px) {
  .knowledge-content {
    padding: 16px;
  }
  
  .articles-grid {
    grid-template-columns: 1fr;
  }
  
  .categories-section {
    overflow-x: auto;
    justify-content: flex-start;
    padding-bottom: 8px;
  }
}
</style>