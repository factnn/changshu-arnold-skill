#!/usr/bin/env python3
"""生成阿诺'蠢与坏'深度分析 - 使用LLM"""

import os
import json
import requests

BASE = os.path.dirname(os.path.abspath(__file__))
REF_DIR = os.path.join(BASE, "references/understanding")
API_URL = "YOUR_API_ENDPOINT_HERE"
API_KEY = "YOUR_API_KEY_HERE"
MODEL = "YOUR_MODEL_HERE"

PROMPT = """你是一位深度人格分析师。基于以下关于常熟阿诺（盛亦陶）的全部素材，请完成一项核心任务：

# 核心论题：又蠢又坏，蠢限制了坏

阿诺是一个混沌系统。他是为数不多的、真的发自内心的坏，而且因为他的蠢所限制了他的坏的人。请从以下维度深度拆解：

## 一、蠢的表象（具体事例）
列举阿诺所有蠢的具体表现，分类归纳：
- 智力层面的蠢（数学、识字、常识）
- 社交层面的蠢（不理解社交规则、不理解暗示）
- 决策层面的蠢（生米充碳、雪糕备赛、上海麻辣烫）
- 自我认知的蠢（坚信纯天然、认为自己痞帅）

## 二、坏的表象（具体事例）
列举阿诺所有坏的具体表现，分类归纳：
- 对师傅的坏（反噬每一任师傅，白吃白住还造谣）
- 对父母的坏（骂父亲、怂恿网友打电话骂父亲、拿电棍打爷爷要钱）
- 对女性的坏（骚扰女教练、骚扰娜娜、打葛佳琪、威胁戴安娜）
- 对亲人去世的冷漠（奶奶死了"没事爷爷又找了一个"、爷爷死了守灵刷礼物起外号）
- 对恩人的坏（艾刚自掏腰包照顾他，他造谣艾刚性骚扰）

## 三、蠢如何限制了坏
- 如果阿诺聪明一点，他的坏会造成什么后果？
- 蠢让他的坏变成了什么效果？（搞笑？自我毁灭？）
- 具体案例分析：哪些坏的行为因为蠢而失败了？

## 四、扭曲的三观（内在驱动力分析）

### 4.1 男性气质观
- 他认为男人应该是什么样的？（黑老大、打女人、玩女人、嫖娼）
- 为什么说他"老实人"他会暴怒？（老实=弱小=被绿）
- 他的男性气质理想从哪里来？（港片黑帮文化？底层社会？）

### 4.2 孝道观
- 对父母的真实态度是什么？
- 对老人去世的反应说明了什么？
- 他有没有真正的情感连接？

### 4.3 社交观
- 他如何看待人际关系？（利用？依附？）
- 为什么每一任师傅都被反噬？
- 他的"忠诚"和"背叛"的标准是什么？

### 4.4 女性观
- 他如何看待女性？（物化？占有？）
- 为什么会单方面认定女友？
- 为什么会骚扰、威胁、打女人？

### 4.5 自我认知
- 他认为自己是什么样的人？
- 现实中他是什么样的人？
- 这个差距有多大？

## 五、心路历程还原
对于阿诺的每一个重大坏行为，还原他当时的心路历程：
- 他在想什么？
- 他的动机是什么？
- 他预期的结果是什么？
- 实际结果是什么？
- 他事后如何合理化自己的行为？

## 六、盖棺定论
用一段话总结阿诺这个人的本质。

---

请输出完整的Markdown文档，标题为：# 常熟阿诺：蠢与坏的深度解构

以下是全部素材：

"""

def load_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    print("=== 生成'蠢与坏'深度分析 ===")
    print(f"使用模型: {MODEL}")
    print()

    # 读取所有素材
    materials = []

    # 熟人评价
    peer_review = load_file(os.path.join(BASE, "peer_reviews/peer_review.txt"))
    materials.append(f"## 熟人评价（师兄原声）\n{peer_review}")

    # 梗百科
    memes = load_file(os.path.join(REF_DIR, "memes.md"))
    materials.append(f"## 梗百科\n{memes}")

    # 人物经历
    bio = load_file(os.path.join(REF_DIR, "biography.md"))
    materials.append(f"## 人物经历\n{bio}")

    # 家庭背景
    family = load_file(os.path.join(REF_DIR, "family.md"))
    materials.append(f"## 家庭背景\n{family}")

    # 认知模型
    cognitive = load_file(os.path.join(REF_DIR, "cognitive_model.md"))
    materials.append(f"## 认知模型\n{cognitive}")

    all_materials = "\n\n---\n\n".join(materials)
    full_prompt = PROMPT + all_materials

    print(f"Prompt长度: {len(full_prompt)} 字符")
    print("调用LLM API...")

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
                'max_tokens': 16000,
                'messages': [{'role': 'user', 'content': full_prompt}]
            },
            timeout=600
        )

        data = resp.json()
        if 'content' in data and len(data['content']) > 0:
            result = data['content'][0]['text'].strip()
            print(f"\n✓ API调用成功，返回 {len(result)} 字符")

            # 保存到references
            output_path = os.path.join(REF_DIR, "evil_and_stupid.md")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"✓ 已保存: {output_path}")

            print("\n=== 完成 ===")
        else:
            print(f"API错误: {data}")

    except Exception as e:
        print(f"\n✗ 失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
