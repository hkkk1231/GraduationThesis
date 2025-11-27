# Zotero CLI 操作经验总结

## 问题背景
尝试通过CLI向Zotero数据库添加笔记，但创建的笔记无法在GUI界面中显示，而手动创建的笔记可以正常显示。

## 关键发现

### 1. HTML结构要求
**正确的笔记HTML结构**：
```html
<div class="zotero-note znv1"><div data-schema-version="9">笔记内容</div></div>
```

**错误的结构**（缺少schema属性）：
```html
<div class="zotero-note znv1">笔记内容</div>
```

### 2. 数据库操作前提
- **必须完全关闭Zotero**才能操作SQLite数据库
- ItemTypeID 28 对应笔记类型
- 数据库路径：`C:\Users\用户名\Zotero\zotero.sqlite`

### 3. 父文献Key的重要性
- 不同的文献条目有不同的Key
- 确保为正确的父文献创建笔记，否则会添加到错误的文献下
- 需要通过数据库查询确认正确的父文献Key

## 调试流程

### 系统化排查步骤
1. **确认父文献Key**：查询数据库确保操作的是正确的文献条目
2. **对比数据结构**：分析手动创建和代码创建的笔记差异
3. **检查HTML格式**：验证必需的属性和结构
4. **验证数据库存储**：确认数据正确写入数据库
5. **重启验证**：重启Zotero检查显示效果

### 常用查询语句
```sql
-- 查找父文献下的所有笔记
SELECT i.key, i.dateAdded, n.note
FROM items i
LEFT JOIN itemNotes n ON i.itemID = n.itemID
WHERE i.itemID IN (
    SELECT itemID FROM itemNotes WHERE parentItemID = ?
)
ORDER BY i.dateAdded DESC

-- 检查笔记HTML结构
SELECT note FROM itemNotes WHERE itemID = ?
```

## 解决方案

### 创建笔记的正确代码结构
```python
# 生成正确的HTML结构
formatted_note = f"""<div class="zotero-note znv1"><div data-schema-version="9">{note_content}</div></div>"""

# 插入笔记条目
cursor.execute("""
    INSERT INTO items (libraryID, key, itemTypeID, dateAdded, dateModified, clientDateModified)
    VALUES (1, ?, 28, datetime('now'), datetime('now'), datetime('now'))
""", (note_key,))

# 设置父子关系和内容
cursor.execute("""
    INSERT INTO itemNotes (itemID, parentItemID, note)
    VALUES (?, ?, ?)
""", (note_id, parent_id, formatted_note))
```

## 经验总结

### 关键要点
1. **data-schema-version="9"** 是Zotero识别笔记格式的关键属性
2. **父文献Key确认** 是确保笔记添加到正确位置的前提
3. **数据库锁定** 问题会导致操作失败，必须完全关闭Zotero
4. **对比分析** 是解决显示问题的有效方法

### 避免的坑
- 不要假设某个Key就是正确的父文献
- 不要忽略HTML结构的细微差异
- 不要在Zotero运行时操作数据库
- 不要跳过验证步骤直接提交

## 工具脚本
项目中创建的相关脚本：
- `compare_notes.py` - 对比笔记数据结构
- `find_correct_parent.py` - 查找正确的父文献
- `fix_note_structure.py` - 修复笔记结构
- `create_note_correct_parent.py` - 在正确父文献下创建笔记

## 应用场景
- 批量导入文献时自动创建笔记
- 通过CLI管理Zotero文献库
- 自动化文献整理和分类
- 与其他工具集成时的数据同步

---
*记录时间：2025-11-27*
*适用版本：Zotero 7*