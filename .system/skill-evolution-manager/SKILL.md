---
name: skill-evolution-manager
description: 涓撻棬鐢ㄤ簬鍦ㄥ璇濈粨鏉熸椂锛屾牴鎹敤鎴峰弽棣堝拰瀵硅瘽鍐呭鎬荤粨浼樺寲骞惰凯浠ｇ幇鏈?Skills 鐨勬牳蹇冨伐鍏枫€傚畠閫氳繃鍚稿彇瀵硅瘽涓殑"绮惧崕"锛堝鎴愬姛鐨勮В鍐虫柟妗堛€佸け璐ョ殑鏁欒銆佺壒瀹氱殑浠ｇ爜瑙勮寖锛夋潵鎸佺画婕旇繘 Skills 搴撱€俇se when user says "澶嶇洏skill", "浼樺寲skill", "evolve", "璁板綍缁忛獙", "淇濆瓨鍒皊kill", or "skill杩涘寲".
license: MIT
github_url: https://github.com/KKKKhazix/Khazix-Skills
github_hash: fe15fea6cf7ac216027d11c2c64e87b462cc0427
version: 1.0.0
metadata:
  category: workflow-automation
---

# Skill Evolution Manager

杩欐槸鏁翠釜 AI 鎶€鑳界郴缁熺殑鈥滆繘鍖栦腑鏋⑩€濄€傚畠涓嶄粎璐熻矗浼樺寲鍗曚釜 Skill锛岃繕璐熻矗璺?Skill 鐨勭粡楠屽鐩樺拰娌夋穩銆?

## 鏍稿績鑱岃矗

1.  **澶嶇洏璇婃柇 (Session Review)**锛氬湪瀵硅瘽缁撴潫鏃讹紝鍒嗘瀽鎵€鏈夎璋冪敤鐨?Skill 鐨勮〃鐜般€?
2.  **缁忛獙鎻愬彇 (Experience Extraction)**锛氬皢闈炵粨鏋勫寲鐨勭敤鎴峰弽棣堣浆鍖栦负缁撴瀯鍖栫殑 JSON 鏁版嵁锛坄evolution.json`锛夈€?
3.  **鏅鸿兘缂濆悎 (Smart Stitching)**锛氬皢娌夋穩鐨勭粡楠岃嚜鍔ㄥ啓鍏?`SKILL.md`锛岀‘淇濇寔涔呭寲涓斾笉琚増鏈洿鏂拌鐩栥€?

## 浣跨敤鍦烘櫙

**Trigger**: 
- `/evolve`
- "澶嶇洏涓€涓嬪垰鎵嶇殑瀵硅瘽"
- "鎴戣寰楀垰鎵嶉偅涓伐鍏蜂笉澶ソ鐢紝璁板綍涓€涓?
- "鎶婅繖涓粡楠屼繚瀛樺埌 Skill 閲?

## 宸ヤ綔娴?(The Evolution Workflow)

### 1. 缁忛獙澶嶇洏 (Review & Extract)
褰撶敤鎴疯Е鍙戝鐩樻椂锛孉gent 蹇呴』鎵ц锛?
1.  **鎵弿涓婁笅鏂?*锛氭壘鍑虹敤鎴蜂笉婊℃剰鐨勭偣锛堟姤閿欍€侀鏍间笉瀵广€佸弬鏁伴敊璇級鎴栨弧鎰忕殑鐐癸紙鐗瑰畾 Prompt 鏁堟灉濂斤級銆?
2.  **瀹氫綅 Skill**锛氱‘瀹氭槸鍝釜 Skill 闇€瑕佽繘鍖栵紙渚嬪 `yt-dlp` 鎴?`baoyu-comic`锛夈€?
3.  **鐢熸垚 JSON**锛氬湪鍐呭瓨涓瀯寤哄涓?JSON 缁撴瀯锛?
    ```json
    {
      "preferences": ["鐢ㄦ埛甯屾湜涓嬭浇榛樿闈欓煶"],
      "fixes": ["Windows 涓?ffmpeg 璺緞闇€杞箟"],
      "custom_prompts": "鍦ㄦ墽琛屽墠鎬绘槸鍏堟墦鍗伴浼拌€楁椂"
    }
    ```

### 2. 缁忛獙鎸佷箙鍖?(Persist)
Agent 璋冪敤 `scripts/merge_evolution.py`锛屽皢涓婅堪 JSON 澧為噺鍐欏叆鐩爣 Skill 鐨?`evolution.json` 鏂囦欢涓€?
- **鍛戒护**: `python scripts/merge_evolution.py <skill_path> <json_string>`

### 3. 鏂囨。缂濆悎 (Stitch)
Agent 璋冪敤 `scripts/smart_stitch.py`锛屽皢 `evolution.json` 鐨勫唴瀹硅浆鍖栦负 Markdown 骞惰拷鍔犲埌 `SKILL.md` 鏈熬銆?
- **鍛戒护**: `python scripts/smart_stitch.py <skill_path>`

### 4. 璺ㄧ増鏈榻?(Align)
褰?`skill-manager` 鏇存柊浜嗘煇涓?Skill 鍚庯紝Agent 搴斾富鍔ㄨ繍琛?`smart_stitch.py`锛屽皢涔嬪墠淇濆瓨鐨勭粡楠屸€滈噸鏂扮紳鍚堚€濆埌鏂扮増鏂囨。涓€?

## 鏍稿績鑴氭湰

- `scripts/merge_evolution.py`: **澧為噺鍚堝苟宸ュ叿**銆傝礋璐ｈ鍙栨棫 JSON锛屽幓閲嶅悎骞舵柊 List锛屼繚瀛樸€?
- `scripts/smart_stitch.py`: **鏂囨。鐢熸垚宸ュ叿**銆傝礋璐ｈ鍙?JSON锛屽湪 `SKILL.md` 鏈熬鐢熸垚鎴栨洿鏂?`## User-Learned Best Practices & Constraints` 绔犺妭銆?
- `scripts/align_all.py`: **鍏ㄩ噺瀵归綈宸ュ叿**銆備竴閿亶鍘嗘墍鏈?Skill 鏂囦欢澶癸紝灏嗗瓨鍦ㄧ殑 `evolution.json` 缁忛獙閲嶆柊缂濆悎鍥炲搴旂殑 `SKILL.md`銆傚父鐢ㄤ簬 `skill-manager` 鎵归噺鏇存柊鍚庣殑缁忛獙杩樺師銆?

## 鏈€浣冲疄璺?

- **涓嶈鐩存帴淇敼 SKILL.md 鐨勬鏂?*锛氶櫎闈炴槸鏄庢樉鐨勬嫾鍐欓敊璇€傛墍鏈夌殑缁忛獙淇搴旈€氳繃 `evolution.json` 閫氶亾杩涜锛岃繖鏍峰彲浠ヤ繚璇佸湪 Skill 鍗囩骇鏃剁粡楠屼笉涓㈠け銆?
- **澶?Skill 鍗忓悓**锛氬鏋滀竴娆″璇濇秹鍙婂涓?Skill锛岃渚濇涓烘瘡涓?Skill 鎵ц涓婅堪娴佺▼銆?

## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### User Preferences
- Skill 系统优化应按 ROI 排序执行：description 优化 > 体积控制 > 元数据规范化 > 安全限制
- 验证步骤必须在所有修改完成后执行，使用独立 agent 进行全量检查
- Phase 1 实现：修改工具 description 比修改核心逻辑更安全有效
- description 级别的优化投入产出比最高

### Known Fixes & Workarounds
- SKILL.md 的 name 字段必须使用 kebab-case 格式，不能包含空格（如 skill-evolution-manager 而非 Skill Evolution Manager）
- name 字段应与文件夹名保持一致，否则 Claude Code 无法正确识别 skill
- 批量编辑 40+ SKILL.md 文件时，使用并行后台 agent 可显著提升效率，但必须配合验证 agent 确认结果
- 后台 agent 可能因 API 超时（524 错误）失败，主线程需要有手动兜底能力
- PowerShell 变量（如 /c/Users/ZDS/bash_completion.d/*.bash）在 bash 环境中会被错误解释为 glob 模式，应避免在 bash 中使用 PowerShell 变量语法
- 复制技能目录时需要排除 .git 和 .omc 等嵌套目录，否则 git add 会报错
- GitHub Token 权限不足时需要创建新 Token，确保勾选 repo 权限
- 外部 npm 包修改不可持续：dist 编译文件会在包更新时丢失，应优先考虑向上游提交 PR
- 独立 Agent 审查能发现自我审查遗漏的问题（如 uuid 依赖未使用）
- Phase 2 放弃原因：OMC 插件更新频繁，深度集成修改意义不大
- Windows bash 环境缺少 jq，配置写入应使用 node.js 而非 shell 命令
- 读取空 JSON 文件前需要检查文件是否存在或内容是否为空
- align_all.py 可批量将所有 skills 的 evolution.json 合并到对应的 SKILL.md
- skills 目录重组后，部分 evolution.json 存在于 .curated/ 或 .experimental/ 子目录中

### Custom Instruction Injection

对于复杂任务，实施前先用独立 Agent 验证计划，实施后用独立 Agent 审查代码。审查清单：(1) 功能正确性 (2) 代码质量 (3) 集成风险 (4) 边缘情况处理