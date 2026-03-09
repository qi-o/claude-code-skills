# Error Rules Reference

閿欒妯″紡涓庝慨澶嶈鍒欏弬鑰冩枃妗ｏ紝瑕嗙洊 80%+ 甯歌閿欒銆?

## 鐩綍

1. [鏂囦欢鐩稿叧閿欒](#1-鏂囦欢鐩稿叧閿欒)
2. [鏉冮檺鐩稿叧閿欒](#2-鏉冮檺鐩稿叧閿欒)
3. [妯″潡/渚濊禆閿欒](#3-妯″潡渚濊禆閿欒)
4. [璇硶閿欒](#4-璇硶閿欒)
5. [绫诲瀷閿欒](#5-绫诲瀷閿欒)
6. [缃戠粶閿欒](#6-缃戠粶閿欒)
7. [杩涚▼/鐜閿欒](#7-杩涚▼鐜閿欒)
8. [骞跺彂/寮傛閿欒](#8-骞跺彂寮傛閿欒)

---

## 1. 鏂囦欢鐩稿叧閿欒

### 1.1 鏂囦欢涓嶅瓨鍦?(ENOENT)

**閿欒妯″紡**:
- `ENOENT: no such file or directory`
- `File does not exist`
- `No such file or directory: 'path'`
- `The system cannot find the file specified`

**鏍瑰洜鍒嗘瀽**:
- 鏂囦欢璺緞鎷煎啓閿欒
- 鏂囦欢灏氭湭鍒涘缓
- 宸ヤ綔鐩綍涓嶆纭?
- 鐩稿璺緞 vs 缁濆璺緞娣锋穯

**淇瑙勫垯**:
```
妫€鏌ユ楠?
1. 纭鏂囦欢璺緞鏄惁姝ｇ‘锛堝ぇ灏忓啓鏁忔劅锛?
2. 妫€鏌ュ綋鍓嶅伐浣滅洰褰?(pwd)
3. 浣跨敤缁濆璺緞灏濊瘯
4. 鍒楀嚭鐩綍鍐呭纭鏂囦欢瀛樺湪

鍛戒护寤鸿:
- ls -la <directory>  # 鍒楀嚭鏂囦欢
- realpath <path>      # 瑙ｆ瀽缁濆璺緞
```

### 1.2 鐩綍涓嶅瓨鍦?

**閿欒妯″紡**:
- `ENOENT: no such file or directory, mkdir`
- `Cannot create directory, path does not exist`

**淇瑙勫垯**:
```
淇鍛戒护:
- mkdir -p <path>  # 鍒涘缓鐩綍鍙婄埗鐩綍

妫€鏌ユ楠?
1. 纭鐖剁洰褰曟槸鍚﹀瓨鍦?
2. 妫€鏌ヨ矾寰勪腑鏄惁鏈夐潪娉曞瓧绗?
```

### 1.3 鏂囦欢宸插瓨鍦?

**閿欒妯″紡**:
- `EEXIST: file already exists`
- `File already exists`

**淇瑙勫垯**:
```
淇閫夐」:
1. 浣跨敤 --force 鎴?-f 瑕嗙洊
2. 鍏堝垹闄ゅ啀鍒涘缓
3. 浣跨敤鍞竴鏂囦欢鍚嶏紙娣诲姞鏃堕棿鎴筹級

鍛戒护寤鸿:
- rm <file> && <command>
- <command> --force
```

---

## 2. 鏉冮檺鐩稿叧閿欒

### 2.1 鏉冮檺琚嫆缁?(EACCES)

**閿欒妯″紡**:
- `EACCES: permission denied`
- `Permission denied: 'path'`
- `EACCES: permission denied, mkdir 'path'`

**鏍瑰洜鍒嗘瀽**:
- 褰撳墠鐢ㄦ埛鏃犺鍙?鍐欏叆/鎵ц鏉冮檺
- 鏂囦欢/鐩綍鐢卞叾浠栫敤鎴锋嫢鏈?
- Linux/macOS: 缂哄皯 execute 鏉冮檺鏃犳硶杩涘叆鐩綍
- Windows: 绠＄悊鍛樻潈闄愪笉瓒?

**淇瑙勫垯**:
```
Linux/macOS:
- chmod 755 <path>      # 鎵€鏈夎€?rwx, 缁?鍏朵粬 r-x
- chmod 644 <file>      # 鎵€鏈夎€?rw-, 缁?鍏朵粬 r--
- sudo chown -R $(whoami) <path>  # 鑾峰緱鎵€鏈夋潈

Windows:
- icacls <path> /grant Everyone:F  # 瀹屽叏鎺у埗锛堟祴璇曠幆澧冿級
- 浠ョ鐞嗗憳韬唤杩愯缁堢
```

### 2.2 鎿嶄綔涓嶈鍏佽 (EPERM)

**閿欒妯″紡**:
- `EPERM: operation not permitted`
- `Operation not permitted`

**淇瑙勫垯**:
```
鍙兘鍘熷洜:
1. 绯荤粺淇濇姢鐨勬枃浠讹紙濡傜郴缁熺洰褰曪級
2. 闃茬梾姣掕蒋浠堕樆姝?
3. 鏂囦欢琚叾浠栬繘绋嬮攣瀹?

瑙ｅ喅鏂规:
1. 鍏抽棴鍙兘閿佸畾鏂囦欢鐨勭▼搴?
2. 妫€鏌ラ槻鐥呮瘨璁剧疆
3. 浣跨敤绠＄悊鍛樻潈闄?
```

---

## 3. 妯″潡/渚濊禆閿欒

### 3.1 妯″潡鏈壘鍒?

**閿欒妯″紡**:
- `Cannot find module 'xxx'`
- `ERR_MODULE_NOT_FOUND`
- `Module not found: Error: Cannot resolve module`
- `Cannot find module './xxx'`

**鏍瑰洜鍒嗘瀽**:
- 妯″潡鏈畨瑁?
- 妯″潡璺緞閿欒锛堢己灏戞墿灞曞悕锛?
- node_modules 鐩綍闂
- TypeScript 璺緞鏄犲皠閿欒

**淇瑙勫垯**:
```
妫€鏌ユ楠?
1. 纭鏂囦欢鎵╁睍鍚?(.ts, .js, .tsx, .jsx)
2. 妫€鏌?package.json 鏄惁鍖呭惈璇ヤ緷璧?
3. 纭 index 鏂囦欢瀛樺湪锛坕ndex.ts/index.js锛?

瀹夎鍛戒护:
- npm install <module-name>
- bun install <module-name>
- pnpm install <module-name>

璺緞妫€鏌?
- 鐩稿璺緞浠庡綋鍓嶆枃浠朵綅缃嚭鍙?
- 浣跨敤缁濆璺緞鎴栬矾寰勫埆鍚?
```

### 3.2 渚濊禆鐗堟湰鍐茬獊

**閿欒妯″紡**:
- `ERR_PACKAGE_PATH_NOT_EXPORTED`
- `Invalid hook call`
- `Module has no default export`
- `Type ... is not assignable to type ...`

**淇瑙勫垯**:
```
瑙ｅ喅鏂规:
1. 妫€鏌?package.json 鐗堟湰鑼冨洿
2. 浣跨敤 npm ls <package> 鏌ョ湅渚濊禆鏍?
3. 鍒犻櫎 node_modules 鍜?package-lock.json 閲嶆柊瀹夎

鐗堟湰淇:
- npm install <package>@latest
- npm install <package>@<specific-version>
```

### 3.3 TypeScript 閰嶇疆閿欒

**閿欒妯″紡**:
- `Cannot find name 'xxx'`
- `Property 'xxx' does not exist on type`
- `Type 'xxx' is not assignable to type 'yyy'`

**淇瑙勫垯**:
```
妫€鏌?tsconfig.json:
1. 纭 "strict": true/false
2. 妫€鏌?"moduleResolution"
3. 纭 "paths" 鏄犲皠姝ｇ‘
4. 妫€鏌?"esModuleInterop": true

绫诲瀷瀹夎:
- npm install -D @types/<package-name>
```

---

## 4. 璇硶閿欒

### 4.1 甯歌 JavaScript/TypeScript 璇硶閿欒

**閿欒妯″紡**:
- `SyntaxError: Unexpected token`
- `SyntaxError: Unexpected string`
- `SyntaxError: Unexpected number`
- `SyntaxError: Bad escape sequence`

**鏍瑰洜鍒嗘瀽**:
- 鎷彿/寮曞彿涓嶅尮閰?
- 缂哄皯鍒嗗彿鎴栭€楀彿
- 閿欒鐨勮浆涔夊瓧绗?
- JSX 璇硶閿欒

**淇瑙勫垯**:
```
甯歌閿欒涓庝慨澶?

1. 鎷彿涓嶅尮閰?
   閿欒: function foo() { return 1
   淇: function foo() { return 1 }

2. 寮曞彿涓嶅尮閰?
   閿欒: const str = 'hello"
   淇: const str = 'hello'

3. 缂哄皯閫楀彿
  閿欒: const obj = { a: 1 b: 2 }
   淇: const obj = { a: 1, b: 2 }

4. 绠ご鍑芥暟閿欒
   閿欒: const foo = x => { x * 2 }  // 缂哄皯 return
   淇: const foo = x => x * 2
   鎴?   const foo = x => { return x * 2 }

5. 瑙ｆ瀯璧嬪€奸敊璇?
   閿欒: const { a, b } = null
   淇: const { a, b } = obj || {}
```

### 4.2 JSON 璇硶閿欒

**閿欒妯″紡**:
- `JSON Parse Error: Unexpected token`
- `Unexpected end of JSON input`

**淇瑙勫垯**:
```
妫€鏌ヨ鐐?
1. 鏈熬涓嶈兘鏈夊浣欓€楀彿
2. 閿悕蹇呴』鐢ㄥ弻寮曞彿
3. 涓嶈兘鏈夊崟寮曞彿
4. 涓嶈兘鏈夋敞閲?
5. 涓嶈兘鏈夊熬闅忛€楀彿

楠岃瘉宸ュ叿:
- node -e "JSON.parse(fs.readFileSync('file.json'))"
- 鍦ㄧ嚎 JSON 楠岃瘉鍣?
```

---

## 5. 绫诲瀷閿欒

### 5.1 undefined/null 鐩稿叧

**閿欒妯″紡**:
- `TypeError: Cannot read property 'xxx' of undefined`
- `TypeError: Cannot read properties of undefined`
- `TypeError: Cannot set properties of undefined`
- `TypeError: Cannot read property 'xxx' of null`
- `undefined is not an object (evaluating 'xxx')`

**鏍瑰洜鍒嗘瀽**:
- 璁块棶浜?undefined/null 鐨勫睘鎬?
- 寮傛鎿嶄綔杩斿洖鍓嶅氨璁块棶
- 鍑芥暟杩斿洖鍊煎彲鑳戒负 undefined

**淇瑙勫垯**:
```
淇绛栫暐:

1. 鍙€夐摼 (?.):
   閿欒: obj.foo.bar
   淇: obj?.foo?.bar

2. 绌哄€煎悎骞?(??):
   閿欒: value || 'default'
   淇: value ?? 'default'

3. 绫诲瀷瀹堝崼:
   if (obj && obj.prop) { ... }

4. 榛樿鍙傛暟:
   function foo(arg = {}) { ... }

5. 鍒濆鍖栨鏌?
   const data = result?.data ?? []
```

### 5.2 鍑芥暟璋冪敤鐩稿叧

**閿欒妯″紡**:
- `TypeError: xxx is not a function`
- `TypeError: xxx is not a constructor`
- `TypeError: xxx is not iterable`

**鏍瑰洜鍒嗘瀽**:
- 鍙橀噺璧嬪€奸敊璇?
- 瀵煎叆鏂瑰紡閿欒锛坉efault vs named锛?
- 瀵硅薄鏂规硶鏈粦瀹?this

**淇瑙勫垯**:
```
淇绛栫暐:

1. 瀵煎叆閿欒:
   閿欒: import { foo } from 'module'  // foo 鏄?default export
   淇: import foo from 'module'

2. this 缁戝畾:
   閿欒: const handler = obj.method
   淇: const handler = obj.method.bind(obj)
   鎴?  const handler = () => obj.method()

3. 鏋勯€犲嚱鏁伴敊璇?
   閿欒: new something  // something 涓嶆槸鏋勯€犲嚱鏁?
   淇: 妫€鏌ユ瀯閫犲嚱鏁版槸鍚︽纭鍑?
```

---

## 6. 缃戠粶閿欒

### 6.1 杩炴帴鎷掔粷/瓒呮椂

**閿欒妯″紡**:
- `ECONNREFUSED`
- `ETIMEDOUT`
- `Connection timed out`
- `Connection refused`

**鏍瑰洜鍒嗘瀽**:
- 鏈嶅姟鍣ㄦ湭杩愯
- 绔彛閿欒
- 闃茬伀澧欓樆姝?
- 缃戠粶闂

**淇瑙勫垯**:
```
妫€鏌ユ楠?
1. 纭鏈嶅姟鍣ㄦ槸鍚﹁繍琛?
2. 妫€鏌ョ鍙ｅ彿鏄惁姝ｇ‘
3. 妫€鏌ラ槻鐏璁剧疆
4. 浣跨敤 telnet/netcat 娴嬭瘯杩炴帴

娴嬭瘯鍛戒护:
- curl -v <url>
- nc -zv <host> <port>
- telnet <host> <port>

閲嶈瘯鏈哄埗:
- 浣跨敤 http-retry 搴?
- 瀹炵幇鎸囨暟閫€閬块噸璇?
```

### 6.2 DNS/涓绘満鏈壘鍒?

**閿欒妯″紡**:
- `ENOTFOUND`
- `getaddrinfo EAI_AGAIN`
- `DNS lookup failed`

**鏍瑰洜鍒嗘瀽**:
- URL 鎷煎啓閿欒
- DNS 閰嶇疆闂
- 缃戠粶鏈繛鎺?

**淇瑙勫垯**:
```
妫€鏌ユ楠?
1. 纭 URL 鎷煎啓姝ｇ‘
2. ping <host> 娴嬭瘯缃戠粶
3. nslookup <host> 妫€鏌?DNS

淇鍛戒护:
- 鍒锋柊 DNS: ipconfig /flushdns (Windows)
-               sudo killall -HUP mDNSResponder (macOS)
```

### 6.3 璇锋眰澶辫触

**閿欒妯″紡**:
- `fetch failed`
- `Request failed with status code 4xx`
- `Request failed with status code 5xx`
- `Network request failed`

**淇瑙勫垯**:
```
HTTP 閿欒鐮佸鐞?

4xx 瀹㈡埛绔敊璇?
- 400: 璇锋眰鏍煎紡閿欒
- 401: 闇€瑕佽璇?
- 403: 鏉冮檺涓嶈冻
- 404: 璧勬簮涓嶅瓨鍦?

5xx 鏈嶅姟鍣ㄩ敊璇?
- 500: 鏈嶅姟鍣ㄥ唴閮ㄩ敊璇?
- 502: 缃戝叧閿欒
- 503: 鏈嶅姟涓嶅彲鐢?
- 504: 缃戝叧瓒呮椂

寤鸿:
- 妫€鏌ヨ姹?URL銆乭eaders銆乥ody
- 娣诲姞閿欒澶勭悊鍜岄噸璇曢€昏緫
- 鏌ョ湅鏈嶅姟鍣ㄦ棩蹇?
```

---

## 7. 杩涚▼/鐜閿欒

### 7.1 杩涚▼琚粓姝?

**閿欒妯″紡**:
- `SIGTERM`
- `SIGKILL`
- `Process exited with code 137` (OOM)
- `Process killed`

**鏍瑰洜鍒嗘瀽**:
- 鍐呭瓨涓嶈冻 (OOM Killer)
- 瓒呮椂琚粓姝?
- 鎵嬪姩缁堟杩涚▼

**淇瑙勫垯**:
```
鍐呭瓨闂:
1. 妫€鏌ヤ唬鐮佹槸鍚︽湁鍐呭瓨娉勬紡
2. 澧炲姞鍐呭瓨闄愬埗: node --max-old-space-size=4096
3. 鍒嗘壒澶勭悊澶ф暟鎹?
4. 浣跨敤娴佸鐞?

瓒呮椂闂:
1. 澧炲姞瓒呮椂鏃堕棿
2. 妫€鏌ユ槸鍚︽湁姝诲惊鐜?
3. 浣跨敤鏂偣缁紶
```

### 7.2 鐜鍙橀噺闂

**閿欒妯″紡**:
- `undefined is not a function` (env missing)
- `process.env.XXX is undefined`

**淇瑙勫垯**:
```
妫€鏌ユ楠?
1. 纭 .env 鏂囦欢瀛樺湪
2. 纭 .env 鍦?.gitignore 涓?
3. 閲嶅惎搴旂敤鍔犺浇鏂扮幆澧冨彉閲?

淇:
- 鍦ㄧ粓绔缃? export VAR=value
- 鎴栦娇鐢?dotenv: require('dotenv').config()
```

---

## 8. 骞跺彂/寮傛閿欒

### 8.1 Promise 鏈鐞?

**閿欒妯″紡**:
- `UnhandledPromiseRejection`
- `Promise rejection`

**鏍瑰洜鍒嗘瀽**:
- async 鍑芥暟鏈?await
- Promise 鏈?.catch()

**淇瑙勫垯**:
```
淇绛栫暐:

1. 娣诲姞 .catch():
   promise
     .then(result => ...)
     .catch(error => console.error(error))

2. 浣跨敤 try-catch:
   try {
     const result = await promise
   } catch (error) {
     console.error(error)
   }

3. 鍏ㄥ眬澶勭悊:
   process.on('unhandledRejection', handler)
```

### 8.2 绔炴€佹潯浠?

**閿欒妯″紡**:
- 鏁版嵁涓嶄竴鑷?
- 鐘舵€侀敊璇?
- 閲嶅鎿嶄綔

**淇瑙勫垯**:
```
淇绛栫暐:

1. 浣跨敤閿?闃熷垪
2. async/await 纭繚椤哄簭
3. 鐘舵€佺鐞嗕娇鐢ㄥ師瀛愭搷浣?
4. 娣诲姞璇锋眰 ID 鍘婚噸
```

---

## 閿欒妯″紡鍖归厤浼樺厛绾?

1. **浼樺厛绾ф渶楂?*: 鍏蜂綋閿欒鐮?(ENOENT, EACCES)
2. **娆′紭鍏堢骇**: 閿欒绫诲瀷 (SyntaxError, TypeError)
3. **鏈€浣庝紭鍏堢骇**: 閿欒娑堟伅鍏抽敭璇?

## 鑷姩淇鑳藉姏鐭╅樀

| 閿欒绫诲瀷 | 鑷姩淇 | 闇€鎵嬪姩 | 涓嶅彲淇 |
|----------|----------|--------|----------|
| 鏂囦欢涓嶅瓨鍦?| 鉁?寤鸿鍒涘缓 | | |
| 鏉冮檺闂 | 鉁?鎻愪緵鍛戒护 | | |
| 妯″潡鏈畨瑁?| 鉁?鎻愪緵瀹夎鍛戒护 | | |
| 璇硶閿欒 | | 鉁?鎻愪緵浣嶇疆 | |
| 绫诲瀷閿欒 | | 鉁?鎻愪緵鍒嗘瀽 | |
| 缃戠粶閿欒 | 鉁?鎻愪緵閲嶈瘯 | | |
| 杩涚▼宕╂簝 | | 鉁?鎻愪緵鍒嗘瀽 | 鉁?闇€绯荤粺绾т慨澶?|

---

*鏈枃妗ｈ鐩栫害 80%+ 甯歌寮€鍙戦敊璇紝鎸佺画鏇存柊涓€?
