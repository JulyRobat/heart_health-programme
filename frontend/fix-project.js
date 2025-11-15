const fs = require('fs')
const path = require('path')

// 创建缺失的目录
const dirs = [
  'src/pages/emotion',
  'src/pages/knowledge', 
  'src/pages/emergency',
  'src/pages/admin',
  'src/pages/register',
  'src/stores',
  'src/api',
  'src/utils'
]

dirs.forEach(dir => {
  const dirPath = path.join(__dirname, dir)
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true })
    console.log(`创建目录: ${dir}`)
  }
})

console.log('项目结构修复完成！')