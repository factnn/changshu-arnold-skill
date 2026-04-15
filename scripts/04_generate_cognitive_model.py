#!/usr/bin/env python3
"""单独生成认知模型 - 使用LLM"""

import os
import json
import requests

BASE = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE, "analysis/individual")
OUTPUT_COGNITIVE = os.path.join(BASE, "references/understanding/cognitive_model.md")
API_URL = "YOUR_API_ENDPOINT_HERE"
API_KEY = "YOUR_API_KEY_HERE"
MODEL = "YOUR_MODEL_HERE"

COGNITIVE_PROMPT = """你是认知心理学家，已经分析了234个常熟阿诺的直播文本。现在请构建他的完整认知模型。

【任务：构建6个子模型 + 综合解释】

## 1. 工作记忆模型
- **容量估计**：能记住多少前文？（估计字数/句数）
- **遗忘速度**：多快会忘记前面说过的话？
- **对语言的影响**：如何导致自相矛盾？
- **证据**：从分析报告中提取的真实例子（至少5个）

## 2. 注意力模型
- **持续时间**：能在一个话题上保持多久？
- **转移触发条件**：什么会让他跳到新话题？
- **对话题跳跃的影响**：为什么会A→B→C→D？
- **证据**：真实例子（至少5个）

## 3. 逻辑推理模型
- **因果理解能力**：能否理解"如果A则B"？
- **悖论识别能力**：能否发现"空腹吃饭"是悖论？
- **对答非所问的影响**：为什么问A答B？
- **证据**：真实例子（至少5个）

## 4. 情绪触发模型
- **触发词列表**：哪些词会让他破防？（从分析报告中汇总）
- **触发阈值**：多容易被激怒？
- **情绪持续时间**：破防后多久恢复？
- **情绪转换模式**：如何从平静到暴怒？
- **证据**：真实例子（至少5个）

## 5. 社交认知模型
- **他人视角理解能力**：能否理解别人的想法？
- **社交暗示敏感度**：能否理解讽刺、暗示？
- **自我认知准确度**：对自己的认知是否准确？
- **证据**：真实例子（至少5个）

## 6. 语言生成机制
- **生成策略**：是流式输出还是有规划？
- **联想链活跃度**：联想是否过度活跃？
- **语义理解深度**：是浅层关键词还是深层语义？
- **自我监控能力**：说完话会检查吗？
- **证据**：真实例子（至少5个）

## 7. 综合解释：为什么阿诺会这样说话

基于以上6个模型，给出深刻的解释：

### 自相矛盾的原因
- 工作记忆容量不足？
- 注意力转移太快？
- 缺乏自我监控？
- 具体机制是什么？

### 答非所问的原因
- 语义理解停留在关键词层面？
- 联想链过度活跃？
- 注意力被某个词劫持？
- 具体机制是什么？

### 思维跳跃的原因
- 注意力持续时间短？
- 联想网络连接混乱？
- 工作记忆无法维持话题？
- 具体机制是什么？

### 突然破防的原因
- 情绪触发阈值极低？
- 情绪调节能力弱？
- 自我保护机制过敏？
- 具体机制是什么？

---

请深入、系统、有洞察力。输出完整的Markdown文档，标题为：# 常熟阿诺认知模型

以下是234个分析报告的认知特征汇总样本：

"""

def load_cognitive_features():
    """读取所有分析报告的认知特征部分"""
    features = []
    files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith('.json')])

    print(f"读取 {len(files)} 个分析报告的认知特征...")

    for filename in files[:100]:  # 取前100个作为样本
        filepath = os.path.join(INPUT_DIR, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                cog = data.get('cognitive_features', {})
                if cog:
                    features.append({
                        'file': data.get('file', filename),
                        'cognitive': cog
                    })
        except Exception as e:
            print(f"警告: 无法读取 {filename}: {e}")

    print(f"成功读取 {len(features)} 个报告的认知特征")
    return features

def summarize_cognitive(features):
    """汇总认知特征"""
    summary = []

    for i, item in enumerate(features[:50], 1):
        file = item['file']
        cog = item['cognitive']

        summary.append(f"\n## 文件{i}: {file}")

        # 工作记忆
        wm = cog.get('working_memory', {})
        if wm:
            summary.append(f"**工作记忆**: {wm.get('capacity', '')} | 证据: {', '.join(wm.get('evidence', [])[:2])}")

        # 注意力
        att = cog.get('attention', {})
        if att:
            summary.append(f"**注意力**: 持续{att.get('duration', '')} | 触发: {', '.join(att.get('triggers', [])[:2])}")

        # 逻辑
        logic = cog.get('logic', {})
        if logic:
            summary.append(f"**逻辑**: {logic.get('causal_understanding', '')}")

        # 情绪
        emotion = cog.get('emotion', {})
        if emotion:
            triggers = emotion.get('triggers', [])
            summary.append(f"**情绪触发**: {', '.join(triggers[:3])}")

        # 社交认知
        social = cog.get('social_cognition', {})
        if social:
            summary.append(f"**社交认知**: {social.get('perspective_taking', '')}")

        # 语言生成
        lang_gen = cog.get('language_generation', {})
        if lang_gen:
            summary.append(f"**语言生成**: {lang_gen.get('strategy', '')}")

    return '\n'.join(summary)

def call_claude(prompt):
    """调用LLM API"""
    print("调用LLM API生成认知模型...")
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

def main():
    print("=== 生成认知模型 ===")
    print(f"使用模型: {MODEL}")
    print()

    # 读取认知特征
    features = load_cognitive_features()

    if len(features) == 0:
        print("错误: 没有找到认知特征数据")
        return

    # 汇总
    print("汇总认知特征...")
    summary = summarize_cognitive(features)

    # 构建完整prompt
    full_prompt = COGNITIVE_PROMPT + summary
    full_prompt += f"\n\n[注：以上是前50个文件的样本，实际共有{len(features)}个文件]\n"
    full_prompt += "\n请基于这些样本，构建完整的认知模型。"

    # 调用API
    try:
        result = call_claude(full_prompt)
        print(f"\n✓ API调用成功，返回 {len(result)} 字符")

        # 保存认知模型
        os.makedirs(os.path.dirname(OUTPUT_COGNITIVE), exist_ok=True)
        with open(OUTPUT_COGNITIVE, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"✓ 认知模型已保存: {OUTPUT_COGNITIVE}")

        print("\n=== 认知模型生成完成 ===")
        print(f"文件位置: {OUTPUT_COGNITIVE}")

    except Exception as e:
        print(f"\n✗ 失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
