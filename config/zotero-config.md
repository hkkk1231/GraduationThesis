# Zotero 配置指南

## 必需插件

### 1. Better BibTeX
- **用途**: 提供更好的BibTeX支持
- **安装**: 在Zotero中通过工具 → 附加组件安装
- **配置**:
  - 启用自动导出
  - 设置键生成格式为 `[auth:lower][year]`
  - 配置引用样式

### 2. Zotfile
- **用途**: 自动管理PDF附件和提取注释
- **安装**: 通过Zotero附加组件安装
- **配置**:
  - 设置附件文件夹路径
  - 启用注释提取功能
  - 配置移动规则

### 3. PDF注释提取
- **用途**: 提取PDF中的高亮和注释
- **配置**:
  - 设置提取格式
  - 配置输出到Obsidian的规则

## 设置步骤

### 1. 基础设置
```
编辑 → 首选项 → 常规
- 设置语言为中文
- 启用自动同步
- 配置数据目录
```

### 2. 同步设置
```
编辑 → 首选项 → 同步
- 输入Zotero账号信息
- 启用文件同步
- 设置同步方式（WebDAV推荐）
```

### 3. 导出设置
```
编辑 → 首选项 → 导出
- 设置默认导出格式为BibTeX
- 配置Better BibTeX选项
```

## 文献管理最佳实践

### 1. 文献分类
- 按研究主题创建集合
- 使用标签进行细分类
- 建立相关文献的关联

### 2. PDF管理
- 使用Zotfile自动重命名PDF
- 设置统一的文件夹结构
- 定期清理重复文件

### 3. 注释规范
- 使用统一的高亮颜色
- 添加有意义的注释
- 提取关键观点和引用

### 4. 引用管理
- 统一引用格式
- 定期检查引用完整性
- 备份引用数据库

## CLI命令行管理

### 1. 统一CLI工具 (zotero_cli.bat)

#### 基本操作
```cmd
# 查看帮助
E:\仓库\毕业论文\zotero_cli.bat --help

# 搜索文献
E:\仓库\毕业论文\zotero_cli.bat search "关键词" --limit 10

# 创建新文献
E:\仓库\毕业论文\zotero_cli.bat create "文献标题" --type journalArticle

# 列出所有分类
E:\仓库\毕业论文\zotero_cli.bat collections

# 添加文献到分类
E:\仓库\毕业论文\zotero_cli.bat addto "文献Key" "分类名称"

# 导入PDF文件
E:\仓库\毕业论文\zotero_cli.bat import "PDF文件路径"
```

#### 文献类型选项
- `book` - 图书
- `journalArticle` - 期刊文章
- `conferencePaper` - 会议论文
- `thesis` - 学位论文
- `report` - 报告

### 2. 批量管理工具 (zotero_batch.bat)

#### 批量操作
```cmd
# 批量导入PDF文件
E:\仓库\毕业论文\zotero_batch.bat batch-import "PDF目录路径" --collection "目标分类"

# 创建分类结构
E:\仓库\毕业论文\zotero_batch.bat create-structure "E:\仓库\毕业论文\collection_structure.json"

# 根据关键词自动分类
E:\仓库\毕业论文\zotero_batch.bat auto-classify "E:\仓库\毕业论文\keywords_mapping.json"

# 导出文献库摘要
E:\仓库\毕业论文\zotero_batch.bat export-summary "输出文件路径.json"
```

#### 配置文件说明

**分类结构配置** (`collection_structure.json`)：
```json
{
  "教育学": {
    "英语教学": {},
    "数学教学": {},
    "语文教学": {}
  },
  "计算机科学": {
    "人工智能": {
      "机器学习": {},
      "深度学习": {}
    }
  }
}
```

**关键词映射配置** (`keywords_mapping.json`)：
```json
{
  "英语教学": ["英语", "English", "语言", "Language"],
  "人工智能": ["AI", "人工智能", "机器学习", "深度学习"]
}
```

### 3. 使用场景

#### 场景1：批量导入新文献
```cmd
# 1. 将PDF文件放入指定目录
# 2. 批量导入
E:\仓库\毕业论文\zotero_batch.bat batch-import "E:\仓库\毕业论文\zotero\知网文献"

# 3. 自动分类
E:\仓库\毕业论文\zotero_batch.bat auto-classify "E:\仓库\毕业论文\keywords_mapping.json"
```

#### 场景2：创建研究项目分类结构
```cmd
# 1. 编辑分类结构配置文件
# 2. 创建分类结构
E:\仓库\毕业论文\zotero_batch.bat create-structure "E:\仓库\毕业论文\collection_structure.json"
```

#### 场景3：查找和整理文献
```cmd
# 1. 搜索相关文献
E:\仓库\毕业论文\zotero_cli.bat search "人工智能" --limit 20

# 2. 查看当前分类
E:\仓库\毕业论文\zotero_cli.bat collections

# 3. 手动添加到分类
E:\仓库\毕业论文\zotero_cli.bat addto "ABC123" "教育学"
```

### 4. 故障排除

#### 常见问题
1. **API连接失败**：检查API密钥和库ID配置
2. **文件路径错误**：使用绝对路径避免路径问题
3. **权限问题**：确保有读写Zotero目录的权限

#### 配置检查
```cmd
# 检查配置文件
python E:\仓库\毕业论文\zotero_cli_config.py

# 测试连接
E:\仓库\毕业论文\zotero_cli.bat collections
```

## 与Obsidian集成

### 1. 自动工作流
1. 在Zotero中添加文献
2. 阅读PDF并添加注释
3. Zotfile自动提取注释
4. 在Obsidian中生成笔记
5. 建立知识关联

### 2. 手动同步
```
Zotero → 右键文献 → Export Notes
选择Obsidian格式并导出
```

### 3. 引用链接
```
在Obsidian中使用 [[Zotero文献标题]] 引用文献
自动生成文献卡片和引用信息
```