# Dataview查询示例

## 最近添加的文献
```dataview
TABLE 
  authors as "作者",
  year as "年份",
  publication as "期刊",
  dateAdded as "添加日期"
FROM #文献笔记
SORT dateAdded DESC
LIMIT 10
```

## 按年份分组的文献
```dataview
TABLE rows.file.link as "文献"
FROM #文献笔记
GROUP BY year
SORT year DESC
```

## 特定研究领域的文献
```dataview
TABLE 
  authors as "作者",
  title as "标题",
  tags as "标签"
FROM #文献笔记
WHERE contains(this.tags, "教育学") OR contains(this.tags, "人工智能")
SORT year DESC
```

## 未阅读的文献
```dataview
LIST
FROM #文献笔记
WHERE !contains(this.tags, "已读")
SORT dateAdded DESC
```

## 带有特定标签的笔记
```dataview
LIST
FROM ""
WHERE contains(file.tags, "核心概念")
```

## 文献统计
```dataview
TABLE 
  length(rows) as "数量"
FROM #文献笔记
GROUP BY year
SORT year DESC
```

## 相关文献推荐
```dataview
LIST
FROM #文献笔记
WHERE contains(this.tags, this.tags)
SORT file.mtime DESC
LIMIT 5
```
