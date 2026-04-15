# 脚本说明

本目录包含用于从原始视频到最终Skill的完整蒸馏流程脚本。

## 使用前准备

1. **配置API密钥**：在每个脚本中设置你的API密钥
2. **准备数据**：将原始转写文本放在对应目录
3. **安装依赖**：`pip install requests`

## 脚本列表

### 01_clean_transcripts.py
**功能**：批量清洗Whisper转写文本

**输入**：`raw_transcripts/` 目录下的txt文件

**输出**：`cleaned_transcripts/` 目录下的清洗后文本

**模型**：LLM-M2.5（或其他便宜的模型）

**并发**：4 workers

**用法**：
```bash
python 01_clean_transcripts.py
```

**配置项**：
- `API_URL`：API端点
- `API_KEY`：你的API密钥
- `MODEL`：模型名称
- `MAX_WORKERS`：并发数

---

### 02_analyze_transcripts.py
**功能**：深度分析每个直播文本的语言规律和认知特征

**输入**：`cleaned_transcripts/` 目录下的清洗后文本

**输出**：`analysis/individual/` 目录下的JSON分析报告

**模型**：LLM（或其他强推理模型）

**并发**：20 workers

**用法**：
```bash
python 02_analyze_transcripts.py
```

**输出格式**：
```json
{
  "file": "文件名.txt",
  "language_patterns": {
    "catchphrases": [...],
    "contradictions": [...],
    "irrelevant_answers": [...],
    "topic_jumps": [...],
    "interjections": [...],
    "new_patterns": [...]
  },
  "cognitive_features": {
    "working_memory": {...},
    "attention": {...},
    "logic": {...},
    "emotion": {...},
    "social_cognition": {...},
    "language_generation": {...}
  }
}
```

---

### 03_aggregate_analysis.py
**功能**：聚合234个分析报告，提取高频模式

**输入**：`analysis/individual/` 目录下的所有JSON

**输出**：
- `analysis/aggregated_patterns.md`：语言规律总结
- `analysis/aggregated_cognitive.md`：认知模型初稿

**模型**：LLM（或最强模型）

**用法**：
```bash
python 03_aggregate_analysis.py
```

---

### 04_generate_cognitive_model.py
**功能**：基于聚合结果，生成完整的6维认知模型

**输入**：`analysis/aggregated_cognitive.md`

**输出**：`references/understanding/cognitive_model.md`

**模型**：LLM

**用法**：
```bash
python 04_generate_cognitive_model.py
```

---

### 05_generate_evil_stupid.py
**功能**：基于"蠢限制了坏"理论，分析深层结构

**输入**：
- `references/understanding/cognitive_model.md`
- `references/understanding/language_patterns.md`
- 所有清洗后的文本

**输出**：`references/understanding/evil_and_stupid.md`

**模型**：LLM

**用法**：
```bash
python 05_generate_evil_stupid.py
```

---

## 完整流程

```bash
# 1. 清洗文本（234个直播）
python 01_clean_transcripts.py

# 2. 深度分析（生成234个JSON）
python 02_analyze_transcripts.py

# 3. 聚合模式
python 03_aggregate_analysis.py

# 4. 生成认知模型
python 04_generate_cognitive_model.py

# 5. 生成深层结构分析
python 05_generate_evil_stupid.py
```

## 注意事项

1. **API成本**：整个流程约需$200（取决于你的API定价）
2. **时间**：总计约4-5小时
3. **并发限制**：根据你的API限制调整`MAX_WORKERS`
4. **错误重试**：所有脚本都有重试机制
5. **断点续传**：脚本会跳过已处理的文件

## 数据隐私

- 原始视频和文本**不包含在本仓库**
- 脚本中的API密钥已移除
- 仅提供方法论和工具

## 自定义

你可以修改以下内容来适配其他角色：

1. **清洗规则**：修改`01_clean_transcripts.py`中的`PROMPT_TEMPLATE`
2. **分析维度**：修改`02_analyze_transcripts.py`中的分析prompt
3. **聚合逻辑**：修改`03_aggregate_analysis.py`中的聚合prompt

## 许可

这些脚本遵循MIT许可证，可自由使用和修改。
