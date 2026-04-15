#!/usr/bin/env python3
"""阶段二：聚合237个分析报告，提取高频模式，构建认知模型 - 使用LLM"""

import os
import json
import requests

BASE = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE, "analysis/individual")
OUTPUT_PATTERNS = os.path.join(BASE, "analysis/aggregated_patterns.md")
OUTPUT_COGNITIVE = os.path.join(BASE, "references/understanding/cognitive_model.md")
API_URL = "YOUR_API_ENDPOINT_HERE"
API_KEY = "YOUR_API_KEY_HERE"
MODEL = "YOUR_MODEL_HERE"

AGGREGATE_PROMPT = """你是首席研究员，已完成234个直播文本的深度分析。现在请综合所有分析报告。

【任务一：语言规律总结】
1. 高频模式识别
   - 哪些语言模式出现在50%以上的文本中？
   - 哪些模式出现在10-50%的文本中？
   - 罕见但典型的模式有哪些？

2. 模式变体归纳
   - 每个高频模式有哪些变体？
   - 给出典型例子（至少3-5个）

3. 扩充语法系统
   - 现有8条语法系统规则：
     1. 自相矛盾（30秒内反转）
     2. 答非所问（问A答B）
     3. 疯狂重复（口头禅轰炸）
     4. 逻辑崩坏（左脑右脑打架）
     5. 思维跳跃（话题瞬移）
     6. 常熟方言 + 错别字
     7. 语气词轰炸
     8. 突然破防（零帧起手）
   - 新增10-20条更细致的规则
   - 每条规则包含：
     * 规则描述
     * 出现频率（高/中/低）
     * 典型例子（3-5个，从分析报告中提取真实例子）
     * 认知机制解释（为什么会这样说话）

【任务二：认知模型构建】
1. 工作记忆模型
   - 容量估计（能记住多少前文）
   - 遗忘速度
   - 对语言生成的影响
   - 证据汇总

2. 注意力模型
   - 持续时间
   - 转移触发条件
   - 对话题跳跃的影响
   - 证据汇总

3. 逻辑推理模型
   - 因果理解能力
   - 悖论识别能力
   - 对答非所问的影响
   - 证据汇总

4. 情绪触发模型
   - 触发词列表（从分析报告中汇总）
   - 触发阈值
   - 情绪持续时间
   - 情绪转换模式
   - 证据汇总

5. 社交认知模型
   - 他人视角理解能力
   - 社交暗示敏感度
   - 自我认知准确度
   - 证据汇总

6. 语言生成机制
   - 生成策略（流式？规划？）
   - 联想链活跃度
   - 语义理解深度
   - 自我监控能力
   - 证据汇总

【任务三：合理化解释】
对于常人看来"不合理"的表达，给出基于认知模型的合理解释：
- 为什么会自相矛盾？（工作记忆容量不足？注意力转移？）
- 为什么会答非所问？（语义理解浅层？抓错关键词？）
- 为什么会思维跳跃？（联想链过度活跃？注意力易分散？）
- 为什么会突然破防？（情绪触发阈值低？情绪调节能力弱？）

请深入、系统、有洞察力。输出两个部分：

## 第一部分：扩充的语言规律（Markdown格式）
标题：# 常熟阿诺语言规律（20-30条）

每条规律格式：
### N. 规律名称
- **频率**：高/中/低
- **描述**：...
- **例子**：
  1. ...
  2. ...
  3. ...
- **认知机制**：...

## 第二部分：认知模型（Markdown格式）
标题：# 常熟阿诺认知模型

包含6个子模型，每个子模型格式：
## 1. 工作记忆模型
- **容量估计**：...
- **遗忘速度**：...
- **对语言的影响**：...
- **证据**：
  - ...
  - ...

最后加上：
## 7. 综合解释：为什么阿诺会这样说话
- 自相矛盾的原因：...
- 答非所问的原因：...
- 思维跳跃的原因：...
- 突然破防的原因：...

---
以下是234个分析报告的汇总：

"""

def load_all_analyses():
    """读取所有JSON分析报告"""
    analyses = []
    files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith('.json')])

    print(f"读取 {len(files)} 个分析报告...")

    for filename in files:
        filepath = os.path.join(INPUT_DIR, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                analyses.append(data)
        except Exception as e:
            print(f"警告: 无法读取 {filename}: {e}")

    print(f"成功读取 {len(analyses)} 个报告")
    return analyses

def summarize_analyses(analyses):
    """汇总分析报告为紧凑格式"""
    summary = []

    for i, analysis in enumerate(analyses[:50], 1):  # 先取前50个作为样本
        file = analysis.get('file', f'file_{i}')
        lang = analysis.get('language_patterns', {})
        cog = analysis.get('cognitive_features', {})

        # 提取关键信息
        catchphrases = lang.get('catchphrases', [])
        contradictions = lang.get('contradictions', [])

        summary.append(f"\n## 文件{i}: {file}")

        if catchphrases:
            summary.append(f"口头禅: {', '.join([c.get('phrase', '') for c in catchphrases[:5]])}")

        if contradictions:
            summary.append(f"矛盾: {contradictions[0].get('example', '')[:100] if contradictions else ''}")

        # 认知特征
        wm = cog.get('working_memory', {})
        if wm:
            summary.append(f"工作记忆: {wm.get('capacity', '')}")

    return '\n'.join(summary)

def call_claude(prompt):
    """调用LLM API"""
    print("调用LLM API进行聚合分析...")
    print(f"Prompt长度: {len(prompt)} 字符")

    resp = requests.post(
        API_URL,
        headers={
            'x-api-key': API_KEY,
            'anthropic-version': '2023-06-01',
            'content-type': 'application/json'
        },
        json={
            'model': MODEL,
            'max_tokens': 16000,
            'messages': [{'role': 'user', 'content': prompt}]
        },
        timeout=600
    )

    data = resp.json()
    if 'content' in data and len(data['content']) > 0:
        return data['content'][0]['text'].strip()
    else:
        raise Exception(f"API error: {data}")

def split_output(text):
    """分割输出为两个文件"""
    # 查找第二部分的开始
    parts = text.split('# 常熟阿诺认知模型')

    if len(parts) == 2:
        patterns = parts[0].strip()
        cognitive = '# 常熟阿诺认知模型' + parts[1].strip()
        return patterns, cognitive
    else:
        # 如果没有明确分割，尝试其他方式
        lines = text.split('\n')
        split_idx = -1
        for i, line in enumerate(lines):
            if '认知模型' in line and line.startswith('#'):
                split_idx = i
                break

        if split_idx > 0:
            patterns = '\n'.join(lines[:split_idx]).strip()
            cognitive = '\n'.join(lines[split_idx:]).strip()
            return patterns, cognitive
        else:
            # 无法分割，全部作为patterns
            return text, ""

def main():
    print("=== 阶段二：聚合分析与认知模型构建 ===")
    print(f"使用模型: {MODEL}")
    print()

    # 读取所有分析报告
    analyses = load_all_analyses()

    if len(analyses) == 0:
        print("错误: 没有找到分析报告")
        return

    # 汇总为紧凑格式
    print("汇总分析报告...")
    summary = summarize_analyses(analyses)

    # 构建完整prompt
    full_prompt = AGGREGATE_PROMPT + summary
    full_prompt += f"\n\n[注：以上是前50个文件的样本，实际共有{len(analyses)}个文件的分析]\n"
    full_prompt += "\n请基于这些样本，进行深度聚合分析。"

    # 调用API
    try:
        result = call_claude(full_prompt)
        print(f"\n✓ API调用成功，返回 {len(result)} 字符")

        # 分割输出
        patterns, cognitive = split_output(result)

        # 保存语言规律
        with open(OUTPUT_PATTERNS, 'w', encoding='utf-8') as f:
            f.write(patterns)
        print(f"✓ 语言规律已保存: {OUTPUT_PATTERNS}")

        # 保存认知模型
        if cognitive:
            os.makedirs(os.path.dirname(OUTPUT_COGNITIVE), exist_ok=True)
            with open(OUTPUT_COGNITIVE, 'w', encoding='utf-8') as f:
                f.write(cognitive)
            print(f"✓ 认知模型已保存: {OUTPUT_COGNITIVE}")
        else:
            print("警告: 未能提取认知模型部分")

        print("\n=== 阶段二完成 ===")
        print(f"下一步: 运行 integrate_portrait.py 进行阶段三整合分析")

    except Exception as e:
        print(f"\n✗ 错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
