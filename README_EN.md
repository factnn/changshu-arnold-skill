# Changshu Arnold Claude Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude-Code-blue)](https://claude.ai)

> "The Last Line of Defense Against AI"

English | [简体中文](README.md)

## Introduction

What happens when AI meets "The Last Line of Defense Against AI"?
Will "Nuo Language" prevail, or will LLM maintain its dominance?
This is not a simple catchphrase imitation, but a cyber persona based on **systematic analysis of 269 video transcripts**. We extracted 30 language patterns, built a 6-dimensional cognitive model, and provided a complete material library.

**This project is for entertainment and educational purposes only. It does not represent any real person.**

> 💡 **Want to learn about the complete distillation process?** Check out [Methodology](METHODOLOGY.md)
> 📝 **Stories behind development** Check out [Dev Log](DEVLOG.md)

## ⚠️ Warning

**Summon Arnold with caution! Unless you have unlimited tokens!**

Arnold's responses typically:
- Answer irrelevantly, jump between topics
- Contradict himself 3+ times within 30 seconds
- Extremely high density of catchphrases ("right?" "isn't it?" "let me ask you")
- Turn one question into 5 unrelated topics
- Consume tokens at an alarming rate

## Quick Start

### Installation

#### Method 1: Claude Code (Recommended)

```bash
# Clone the repository to Claude Code's skills directory
cd ~/.claude/skills/
git clone https://github.com/factnn/changshu-arnold-skill.git changshu-arnold
```

#### Method 2: Manual Installation

1. Download this repository
2. Copy the entire directory to `~/.claude/skills/changshu-arnold/`
3. Restart Claude Code

### Trigger Words

In Claude Code, use any of the following trigger words to activate the skill:

- 常熟阿诺 (Changshu Arnold)
- 诺神 (God Nuo)
- 诺言诺语 (Nuo Language)
- 那我问你 (Let me ask you)
- 三卡车 (Three trucks)
- 生米冲碳 (Raw rice carb-loading)
- 申气 (Getting angry)
- 脑袋尖尖 (Pointy head)
- 无糖可乐 (Sugar-free cola)

Or use the command directly: `/changshu-arnold`

### Example Dialogue

**User**: Do you know operator generation?

**Arnold**: Aiya, let me ask you, operator generation right? Let me ask you, what kind of operator are you talking about, right?

To be honest, let me tell you, I Arnold know a lot of things, right. You say operator generation, let me ask you, is it that what, uh, that what thing, right?

Let me tell you honestly, I graduated from junior college, I'm an educated person, right...

## File Structure

```
changshu-arnold-skill/
├── README.md                    # Project description (Chinese)
├── README_EN.md                 # Project description (English)
├── METHODOLOGY.md               # Methodology documentation
├── DEVLOG.md                    # Development log
├── LICENSE                      # MIT License
├── SAFETY.md                    # Safety guidelines
├── SKILL.md                     # Main configuration file
├── scripts/                     # Distillation scripts
│   ├── 01_clean_transcripts.py
│   ├── 02_analyze_transcripts.py
│   ├── 03_aggregate_analysis.py
│   ├── 04_generate_cognitive_model.py
│   ├── 05_generate_evil_stupid.py
│   └── README.md
└── references/
    ├── understanding/           # Cognitive models (internal principles)
    │   ├── language_patterns.md    # 30 language patterns
    │   ├── cognitive_model.md      # 6-dimensional cognitive model
    │   └── evil_and_stupid.md      # Deep structure analysis
    └── output/                  # Output materials (material library)
        ├── typos.md                # Typo table
        ├── memes.md                # Meme encyclopedia
        ├── quotes.md               # Classic quotes
        ├── family.md               # Family background
        └── biography.md            # Biographical timeline
```
    └── output/                  # Output materials (material library)
        ├── typos.md                # Typo table
        ├── memes.md                # Meme encyclopedia
        ├── quotes.md               # Classic quotes
        ├── family.md               # Family background
        └── biography.md            # Biographical timeline
```

### Core Files

#### SKILL.md
Main configuration file containing:
- Identity definition
- Internal instructions (understanding/)
- Output material library (output/)
- Prohibited behaviors
- Output strategy (high/medium/low frequency layering, topic-driven)

#### understanding/ Directory
**Purpose**: Help the model understand Arnold's thinking patterns

- **language_patterns.md**: 30 language patterns
  - Confirmation bias catchphrase bombardment ("right?" "isn't it?")
  - 30-second self-destructive contradictions
  - Irrelevant answer semantic drift
  - Zero-frame instant meltdown
  - ...

- **cognitive_model.md**: 6-dimensional cognitive model
  - Working memory model
  - Attention model
  - Logical reasoning model
  - Emotion regulation model
  - Social cognition model
  - Language generation model

- **evil_and_stupid.md**: Deep structure analysis
  - Structural characteristics of stupidity
  - Instinctive characteristics of malice
  - How stupidity limits the range of malice

#### output/ Directory
**Purpose**: Material library for generating specific content

- **typos.md**: Typo table + generation rules (24 fixed + creation rule: similar shape + more common + different pronunciation)
- **memes.md**: 40 classic memes (雪qie, 数学, 靓旗店, 冰红茶...)
- **quotes.md**: 34 original voice quotes
- **family.md**: Family background (parents, grandparents, power structure)
- **biography.md**: Biographical timeline (25+ major events)

## Special Features

### Trigger-Driven Mode

No longer mechanically stacking features, but judging whether to trigger specific behavior patterns based on user input:

**Basic Rules**:
- Catchphrases, interjections, third-person self-reference, Changshu dialect, typos
- Default short responses (1-3 sentences)

**Trigger Condition Mechanism** (7 trigger conditions):
- **Zero-frame meltdown**: Sensitive words like head shape, tech, diabetes → Explosive mode
- **Pure natural contradiction loop**: Fitness, protein powder → Gradual self-contradiction
- **Victim-boasting oscillation**: Romance, female fans → First miserable then boastful
- **Irrelevant answer semantic drift**: Random trigger, keyword association
- **Food ecstasy reaction**: Food-related → Sudden excitement
- **Fabricated narrative/grandiose planning**: Future, plans → Fabrication or grandiosity
- **Temporary patriotic filler**: Nothing to say → Patriotic rescue

### Typo Generation System

Arnold's typos follow a pattern: **Similar shape replacement + more common + different pronunciation**

- Fixed typos: 申气, 脆下, 闰蜜, 煞门, 刷羊肉, etc. (24 total)
- Creative ability: Model can create new typos based on rules (e.g., 嫉妒→嫉炉, 沮丧→且丧)
- Usage frequency: Naturally appears once every 2-3 sentences

### Cognitive Modeling

Not just imitating "how to speak", but also explaining "why speak this way":

- Why 30-second self-contradictions? → Extremely low working memory capacity
- Why irrelevant answers? → Semantic processing stuck at keyword activation level
- Why zero-frame meltdown? → Emotion regulation system lacks buffer layer

## Disclaimer

- This project is for **entertainment and educational purposes**, exploring the charm of abstract literature
- **Does not represent the real person** Sheng Yitao/Changshu Arnold
- **Original data not disclosed** (copyright and privacy protection)
- Does not confirm or spread private information about real people
- Does not generate illegal, abusive, or cyberbullying content

See [SAFETY.md](SAFETY.md) for details

## Contributing

Contributions are welcome! You can:

### Add New Memes
1. Fork this repository
2. Add new memes to `references/output/memes.md`
3. Submit a Pull Request

### Report Issues
- Use [Issues](https://github.com/your-username/changshu-arnold-skill/issues) to report bugs
- Suggest improvements

### Improve Patterns
- If you discover new language patterns, feel free to discuss in Issues
- Provide specific examples and analysis

## Acknowledgments

Thanks to the following Bilibili creators for providing video materials:
- [@抽象健美大使](https://space.bilibili.com/18213126) - Arnold's chronicle
- [@一起活捉盛亦陶](https://space.bilibili.com/484942972) - Classic meme videos
- [@薄特特](https://space.bilibili.com/1953301228) - Livestream recordings

Thanks to all creators contributing to abstract literature.

## License

[MIT License](LICENSE)

---