# Obsidian 配置指南

## 插件安装

### 必需插件
1. **Zotero Integration** - 与Zotero文献管理集成
2. **Better BibTeX** - 增强BibTeX支持
3. **Zotfile** - 自动PDF注释提取
4. **Dataview** - 动态数据查询
5. **Templater** - 模板管理
6. **QuickAdd** - 快速添加内容

### 配置步骤

#### 1. Zotero Integration 配置
- 安装Zotero Integration插件
- 设置Zotero连接路径
- 配置文献导入格式

#### 2. Better BibTeX 配置
- 在Zotero中安装Better BibTeX插件
- 设置自动导出BibTeX文件
- 配置引用格式

#### 3. Zotfile 配置
- 设置PDF附件自动管理
- 配置注释提取规则
- 设置文件夹结构

## 笔记模板

### 文献笔记模板
```markdown
# {{title}}

**作者**: {{authors}}
**期刊**: {{publication}}
**年份**: {{year}}
**DOI**: {{doi}}

## 摘要
{{abstract}}

## 关键要点
- 

## 个人思考
- 

## 引用格式
```
citekey: {{citekey}}
```

## 相关文献
- 
```

### 项目笔记模板
```markdown
# {{title}}

## 项目描述
{{description}}

## 研究问题
1. 

## 研究方法
- 

## 预期成果
- 

## 进度跟踪
- [ ] 文献综述
- [ ] 数据收集
- [ ] 分析研究
- [ ] 论文写作

## 参考资料
- 
```

## 工作流程

1. **文献收集**: 使用Zotero收集文献
2. **PDF阅读**: 在Zotero中阅读PDF并添加注释
3. **笔记生成**: Zotfile自动提取注释到Obsidian
4. **知识整理**: 使用Obsidian整理和连接知识点
5. **论文写作**: 基于整理的笔记进行论文写作