#!/usr/bin/env python3
"""批量清洗阿诺直播转写稿 - LLM API 并发处理"""

import os
import re
import json
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# === 配置 ===
INPUT_DIR = "raw_transcripts"
OUTPUT_DIR = "cleaned_transcripts"
API_URL = "YOUR_API_ENDPOINT_HERE"
API_KEY = "YOUR_API_KEY_HERE"
MODEL = "YOUR_MODEL_HERE"
MAX_CHUNK_SIZE = 2000  # 字符
MAX_WORKERS = 4        # 并发数
MAX_RETRIES = 3        # 重试次数

PROMPT_TEMPLATE = """## 背景
我们正在从常熟阿诺（盛亦陶，中国健美网红）的直播录像中蒸馏他的说话方式。你现在读的是阿诺直播的语音转写稿（由Whisper转写，可能有大量错误）。

阿诺是江苏常熟人，人称"诺神"、"诺哥"，粉丝叫他"诺哥"不是"洛哥"。他说话有以下特征：
- 口头禅：那我问你、再说我申气了
- 特色用词（这些是阿诺本人的错误用法，必须保留）：申气（生气）、屌利（犀利）、煞门（厦门）、闰蜜（闺蜜）、脆下（跪下）、痦帅（痞帅）、低儿能（低能儿）、仰郁症（抑郁症）
- 经常自称"我阿诺"、"阿诺"
- 说话重复、语气词多、逻辑混乱，这些都是他的风格
- 他最爱玩的游戏叫"英雄萨姆"（Serious Sam），不是"英雄三母"、"英雄三不"等
- AD钙奶（不是"ad干奶奶"）

## 目标
清洗后的文字稿要一看就是阿诺说的话——保留他的语言特色，只修正语音识别的错误转写。

## 处理规则
1. 繁体中文全部转为简体中文
2. 修正明显的语音识别错别字（如"洛哥"→"诺哥"、"英雄三母"→"英雄萨姆"）
3. 保留阿诺本人的特色错误用词（申气、屌利、煞门等），不要纠正这些
4. 去除时间戳
5. 保持阿诺原始的说话风格和语序，不要修改成书面语
6. 保留所有语气词、重复、口头禅，这些是阿诺的说话特征
7. 分段整理，使内容可读

直接输出处理后的文字，不要加任何说明。

---
以下是转写稿：

"""


def split_text(text, max_size=MAX_CHUNK_SIZE):
    """按行切块，不超过 max_size 字符"""
    lines = text.split('\n')
    chunks = []
    current = []
    current_len = 0

    for line in lines:
        line_len = len(line) + 1  # +1 for newline
        if current_len + line_len > max_size and current:
            chunks.append('\n'.join(current))
            current = [line]
            current_len = line_len
        else:
            current.append(line)
            current_len += line_len

    if current:
        chunks.append('\n'.join(current))
    return chunks


def call_minimax(text, retry=0):
    """调用 LLM API 清洗一段文字"""
    try:
        resp = requests.post(
            API_URL,
            headers={
                'Authorization': f'Bearer {API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': MODEL,
                'messages': [{'role': 'user', 'content': PROMPT_TEMPLATE + text}],
                'max_tokens': 4096
            },
            timeout=180
        )
        data = resp.json()
        if 'choices' in data:
            content = data['choices'][0]['message']['content']
            content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()
            return content
        else:
            raise Exception(f"API error: {data}")
    except Exception as e:
        if retry < MAX_RETRIES:
            time.sleep(5 * (retry + 1))
            return call_minimax(text, retry + 1)
        else:
            raise e


def process_file(filepath):
    """处理单个文件：读取 → 切块 → 调API → 拼接 → 写入"""
    filename = os.path.basename(filepath)
    outpath = os.path.join(OUTPUT_DIR, filename)

    # 跳过已处理的
    if os.path.exists(outpath):
        return f"SKIP: {filename}"

    with open(filepath, 'r', encoding='utf-8') as f:
        raw = f.read().strip()

    if not raw:
        return f"EMPTY: {filename}"

    # 切块
    if len(raw) <= MAX_CHUNK_SIZE:
        chunks = [raw]
    else:
        chunks = split_text(raw)

    # 逐块调用API（同一文件内串行）
    results = []
    for i, chunk in enumerate(chunks):
        cleaned = call_minimax(chunk)
        results.append(cleaned)
        if len(chunks) > 1:
            time.sleep(1)  # 多块之间稍等

    # 拼接写入
    final = '\n\n'.join(results)
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(final)

    return f"DONE ({len(chunks)} chunks): {filename}"


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 收集所有待处理的txt（排除人物志的已处理稿）
    files = []
    for f in sorted(os.listdir(INPUT_DIR)):
        if f.endswith('.txt'):
            filepath = os.path.join(INPUT_DIR, f)
            outpath = os.path.join(OUTPUT_DIR, f)
            if not os.path.exists(outpath):
                files.append(filepath)

    total = len(files)
    print(f"待处理: {total} 个文件, 并发: {MAX_WORKERS}")

    done = 0
    failed = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_file = {executor.submit(process_file, f): f for f in files}
        for future in as_completed(future_to_file):
            filepath = future_to_file[future]
            filename = os.path.basename(filepath)
            try:
                result = future.result()
                done += 1
                print(f"[{done}/{total}] {result}")
            except Exception as e:
                done += 1
                failed.append(filename)
                print(f"[{done}/{total}] FAIL: {filename} - {e}")

    print(f"\n=== 完成 ===")
    print(f"成功: {total - len(failed)}, 失败: {len(failed)}")
    if failed:
        print("失败文件:")
        for f in failed:
            print(f"  - {f}")


if __name__ == '__main__':
    main()
