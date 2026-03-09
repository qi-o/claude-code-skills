---
name: auto-install
version: 1.0.0
description: |
  鑷姩瀹夎缂哄け鍛戒护宸ュ叿銆傚綋妫€娴嬪埌 "command not found" 閿欒鏃讹紝鑷姩璇嗗埆鍛戒护骞堕€夋嫨鍚堥€傜殑鍖呯鐞嗗櫒瀹夎銆?
  鏀寔 Linux (apt-get/dnf/yum)銆乵acOS (brew)銆乄indows (winget/choco) 鍏ㄥ钩鍙般€?
  瑙﹀彂璇嶏細command not found銆佸畨瑁呭懡浠ゃ€乮nstall missing銆乤uto-install
github_url: https://github.com/anthropics/claude-code
github_hash: 53a5f3ee0703c2ab1b6d1dd18d8ab65187f9b8ad
license: MIT
allowed-tools: "Bash"
metadata:
  category: system-tools
---

# Auto Install

鑷姩瀹夎缂哄け鍛戒护宸ュ叿銆?

## 鏍稿績鍔熻兘

- 鑷姩妫€娴?"command not found" 閿欒
- 鏅鸿兘璇嗗埆鍛戒护骞堕€夋嫨鍚堥€傜殑鍖呯鐞嗗櫒
- 鏀寔澶氬钩鍙帮細Linux銆乵acOS銆乄indows
- 鏀寔澶氱鍖呯鐞嗗櫒锛歛pt-get銆乨nf銆亂um銆乥rew銆亀inget銆乧hoco銆乶pm銆乸ip

## 鑴氭湰鐩綍

鑴氭湰浣嶄簬 `scripts/` 瀛愮洰褰曘€傚皢 `${SKILL_DIR}` 鏇挎崲涓?SKILL.md 鎵€鍦ㄧ洰褰曡矾寰勩€?

| 鑴氭湰 | 鐢ㄩ€?|
|------|------|
| `scripts/auto-install.ts` | 鑷姩瀹夎 CLI |

## 鍛戒护璇硶

```bash
npx -y bun ${SKILL_DIR}/scripts/auto-install.ts <command>
```

## 鍙傛暟璇存槑

| 鍙傛暟 | 璇存槑 | 榛樿鍊?|
|------|------|--------|
| `<command>` | 瑕佸畨瑁呯殑鍛戒护鍚嶇О | 蹇呴渶 |
| `--package-manager` | 鎸囧畾鍖呯鐞嗗櫒 | 鑷姩妫€娴?|
| `--dry-run` | 妯℃嫙杩愯锛屼笉瀹為檯瀹夎 | false |
| `--json` | JSON 鏍煎紡杈撳嚭缁撴灉 | false |

## 浣跨敤绀轰緥

### 瀹夎缂哄け鍛戒护

```bash
/auto-install curl
```

### 鎸囧畾鍖呯鐞嗗櫒

```bash
/auto-install node --package-manager npm
```

### 妯℃嫙杩愯

```bash
/auto-install python --dry-run
```

### JSON 杈撳嚭

```bash
/auto-install git --json
```

杈撳嚭锛?

```json
{
  "command": "git",
  "packageManager": "winget",
  "installCommand": "winget install Git.Git",
  "success": true
}
```

## 鏀寔鐨勫寘绠＄悊鍣?

| 骞冲彴 | 鍖呯鐞嗗櫒 | 鍛戒护绀轰緥 |
|------|----------|----------|
| Linux (Debian/Ubuntu) | apt-get | apt-get install curl |
| Linux (Fedora) | dnf | dnf install curl |
| Linux (CentOS/RHEL) | yum | yum install curl |
| macOS | Homebrew | brew install curl |
| Windows | winget | winget install curl |
| Windows | Chocolatey | choco install curl |
| 璺ㄥ钩鍙?| npm | npm install -g curl |
| 璺ㄥ钩鍙?| pip | pip install curl |

## 鏀寔鐨勫懡浠ゅ垪琛?

璇﹁ `references/commands.md`

## 宸ヤ綔娴佺▼

1. 瑙ｆ瀽杈撳叆鐨勫懡浠ゅ悕绉?
2. 妫€娴嬪綋鍓嶅钩鍙板拰鍙敤鍖呯鐞嗗櫒
3. 鏌ユ壘鍛戒护瀵瑰簲鐨勫寘鍚?
4. 鐢熸垚瀹夎鍛戒护
5. 鎵ц瀹夎锛堥櫎闈炴寚瀹?--dry-run锛?
6. 楠岃瘉瀹夎缁撴灉

## 渚濊禆

- Node.js 18+
- Bun锛堥€氳繃 npx 鑷姩瀹夎锛?
- 骞冲彴瀵瑰簲鐨勫寘绠＄悊鍣?

---
