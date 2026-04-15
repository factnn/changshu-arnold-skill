#!/usr/bin/env python3
"""阶段一：对237个直播文本进行语言学+心理学深度分析 - 使用LLM API"""

import os
import json
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE, "cleaned_transcripts")
OUTPUT_DIR = os.path.join(BASE, "analysis/individual")
API_URL = "YOUR_API_ENDPOINT_HERE"
API_KEY = "YOUR_API_KEY_HERE"
MODEL = "YOUR_MODEL_HERE"
MAX_WORKERS = 20
MAX_RETRIES = 3

ANALYSIS_PROMPT_PART1 = """你是一位语言学家。请深度分析以下直播文本的语言规律。

【任务：语言规律提取】
1. 口头禅使用模式
   - 识别所有口头禅（"那我问你"、"对吧"、"是吧"、"说实话"、"怎么说呢"、"我操"等）
   - 统计出现频率和位置（句首/句中/句尾）
   - 分析口头禅的功能（填充停顿？话题转换？情绪表达？）

2. 自相矛盾模式
   - 找出所有前后矛盾的表述
   - 标注矛盾发生的时间间隔（字数/句数）
   - 分类矛盾类型：完全反转型、渐进矛盾型、循环矛盾型

3. 答非所问模式
   - 提取问答对（如果有）
   - 分析问题类型 vs 答案类型的错位规律

4. 思维跳跃模式
   - 标注话题跳跃点
   - 分析跳跃的触发词和连接词

5. 语气词使用
   - 统计"啊"、"呃"、"哎"、"哎呀"、"我操"等的密度

6. 新发现的语言特征

输出JSON格式：
{
  "catchphrases": [{"phrase": "那我问你", "count": 15, "positions": ["句首"], "function": "填充"}],
  "contradictions": [{"example": "例子", "interval": "30字", "type": "反转型"}],
  "irrelevant_answers": [{"question": "问", "answer": "答"}],
  "topic_jumps": [{"from": "A", "to": "B", "trigger": "词"}],
  "interjections": [{"word": "啊", "density": "高"}],
  "new_patterns": ["描述"]
}

直接输出JSON，不要其他文字。

文本：
"""

ANALYSIS_PROMPT_PART2 = """你是认知心理学家。基于以下直播文本，推断说话者的认知特征。

【任务：认知特征推断】
1. 工作记忆 - 能记住多少前文？自相矛盾是否因为忘了？给出证据
2. 注意力 - 持续时间？什么触发转移？给出证据
3. 逻辑推理 - 能否理解因果？能否理解悖论？给出证据
4. 情绪模式 - 破防触发词？情绪持续时间？给出证据
5. 社交认知 - 能否理解他人视角？自我认知准确吗？给出证据
6. 语言生成 - 流式输出？联想链活跃？语义理解深度？给出证据

输出JSON格式：
{
  "working_memory": {"capacity": "估计", "evidence": ["例子"]},
  "attention": {"duration": "估计", "triggers": ["触发"], "evidence": ["例子"]},
  "logic": {"causal_understanding": "弱", "evidence": ["例子"]},
  "emotion": {"triggers": ["词"], "duration": "短", "evidence": ["例子"]},
  "social_cognition": {"perspective_taking": "弱", "evidence": ["例子"]},
  "language_generation": {"strategy": "流式", "evidence": ["例子"]}
}

直接输出JSON，不要其他文字。

文本：
"""

def call_claude(prompt, text, retry=0):
    """调用LLM API进行分析"""
    try:
        resp = requests.post(
            API_URL,
            headers={
                'x-api-key': API_KEY,
                'anthropic-version': '2023-06-01',
                'content-type': 'application/json'
            },
            json={
                'model': MODEL,
                'max_tokens': 4096,
                'messages': [{'role': 'user', 'content': prompt + text}]
            },
            timeout=60
        )
        data = resp.json()
        if 'content' in data and len(data['content']) > 0:
            content = data['content'][0]['text'].strip()
            # 尝试提取JSON
            if content.startswith('```json'):
                content = content[7:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()
            # 验证是否为有效JSON
            json.loads(content)
            return content
        else:
            raise Exception(f"API error: {data}")
    except Exception as e:
        if retry < MAX_RETRIES:
            time.sleep(2 * (retry + 1))
            return call_claude(prompt, text, retry + 1)
        else:
            raise e

def process_file(filepath):
    """处理单个文件 - 分两次调用API"""
    filename = os.path.basename(filepath)
    json_filename = filename.replace('.txt', '.json')
    outpath = os.path.join(OUTPUT_DIR, json_filename)

    # 跳过已处理的文件
    if os.path.exists(outpath):
        return f"SKIP: {filename}"

    # 读取文本
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read().strip()

    if not text:
        return f"EMPTY: {filename}"

    # 如果文本太长，截取前5000字
    if len(text) > 5000:
        text = text[:5000] + "\n\n[文本过长，已截取前5000字]"

    # 第一次调用：语言规律分析
    language_json = call_claude(ANALYSIS_PROMPT_PART1, text)
    language_data = json.loads(language_json)

    time.sleep(1)  # 避免API限流

    # 第二次调用：认知特征分析
    cognitive_json = call_claude(ANALYSIS_PROMPT_PART2, text)
    cognitive_data = json.loads(cognitive_json)

    # 合并结果
    result = {
        "file": filename,
        "language_patterns": language_data,
        "cognitive_features": cognitive_data
    }

    # 保存JSON结果
    with open(outpath, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    return f"DONE: {filename}"

def main():
    """主函数"""
    # 切换到BASE目录
    # os.chdir(BASE)  # 根据需要取消注释
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 获取所有待处理文件
    files = []
    for f in sorted(os.listdir(INPUT_DIR)):
        if f.endswith('.txt'):
            filepath = os.path.join(INPUT_DIR, f)
            json_filename = f.replace('.txt', '.json')
            outpath = os.path.join(OUTPUT_DIR, json_filename)
            if not os.path.exists(outpath):
                files.append(filepath)

    total = len(files)
    print(f"=== 阶段一：单文本深度分析 ===")
    print(f"待处理: {total} 个文件")
    print(f"并发数: {MAX_WORKERS}")
    print(f"输出目录: {OUTPUT_DIR}")
    print(f"预计耗时: 2-3小时")
    print(f"开始时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    done = 0
    failed = []
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_file = {executor.submit(process_file, f): f for f in files}
        for future in as_completed(future_to_file):
            filepath = future_to_file[future]
            filename = os.path.basename(filepath)
            try:
                result = future.result()
                done += 1
                elapsed = time.time() - start_time
                avg_time = elapsed / done
                eta = avg_time * (total - done)
                print(f"[{done}/{total}] {result} | 已用时: {elapsed/60:.1f}分 | 预计剩余: {eta/60:.1f}分")
            except Exception as e:
                done += 1
                failed.append(filename)
                print(f"[{done}/{total}] FAIL: {filename} - {e}")

    total_time = time.time() - start_time
    print(f"\n=== 阶段一完成 ===")
    print(f"总耗时: {total_time/60:.1f}分钟")
    print(f"成功: {total - len(failed)}, 失败: {len(failed)}")

    if failed:
        print("\n失败文件:")
        for f in failed:
            print(f"  - {f}")

    print(f"\n分析结果已保存到: {OUTPUT_DIR}")
    print(f"下一步: 运行 aggregate_analysis.py 进行阶段二聚合分析")

if __name__ == '__main__':
    main()
