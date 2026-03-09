---
name: react-best-practices
description: |
  React/Next.js 鎬ц兘浼樺寲鏈€浣冲疄璺点€傚寘鍚?57 鏉¤鍒欙紝瑕嗙洊寮傛浼樺寲銆丅undle 浼樺寲銆佹湇鍔＄鎬ц兘銆佸鎴风鏁版嵁鑾峰彇銆侀噸娓叉煋浼樺寲绛?8 澶х被鍒€?
  瑙﹀彂璇嶏細React 浼樺寲銆丯ext.js 鎬ц兘銆佷唬鐮佸鏌ャ€佹€ц兘浼樺寲銆乥undle 浼樺寲銆侀噸娓叉煋
github_url: https://github.com/vercel-labs/agent-skills
github_hash: 64bee5b7ea30702448e2aed774eb361914029944
version: 1.1.0
source: https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices
author: Vercel
tags: [react, nextjs, performance, optimization, best-practices]
license: MIT
metadata:
  category: code-quality
---

# Vercel React Best Practices

React 鍜?Next.js 搴旂敤鎬ц兘浼樺寲鎸囧崡锛屾潵鑷?Vercel 宸ョ▼鍥㈤槦銆傚寘鍚?57 鏉¤鍒欙紝鎸変紭鍏堢骇鍒嗕负 8 澶х被鍒€?

## 瑙﹀彂鏉′欢

褰撶敤鎴疯繘琛屼互涓嬫搷浣滄椂浣跨敤姝?skill锛?
- 缂栧啓鏂扮殑 React 缁勪欢鎴?Next.js 椤甸潰
- 瀹炵幇鏁版嵁鑾峰彇锛堝鎴风鎴栨湇鍔＄锛?
- 瀹℃煡浠ｇ爜鎬ц兘闂
- 閲嶆瀯鐜版湁 React/Next.js 浠ｇ爜
- 浼樺寲 bundle 澶у皬鎴栧姞杞芥椂闂?

## 瑙勫垯绫诲埆锛堟寜浼樺厛绾ф帓搴忥級

### 1. 娑堥櫎鐎戝竷娴?(CRITICAL) - `async-` 鍓嶇紑

| 瑙勫垯 | 璇存槑 |
|------|------|
| `async-defer-await` | 灏?await 绉诲埌瀹為檯浣跨敤鍊肩殑鍒嗘敮涓?|
| `async-parallel` | 瀵圭嫭绔嬪紓姝ユ搷浣滀娇鐢?`Promise.all()` |
| `async-dependencies` | 瀵归儴鍒嗕緷璧栫殑鎿嶄綔浣跨敤 better-all |
| `async-api-routes` | API 璺敱涓敖鏃╁惎鍔?promise锛屽欢杩?await |
| `async-suspense-boundaries` | 浣跨敤 Suspense 杈圭晫娴佸紡浼犺緭鍐呭 |

**绀轰緥锛?*
```typescript
// 鉂?閿欒锛氫覆琛岃姹?
const user = await getUser(id);
const posts = await getPosts(id);

// 鉁?姝ｇ‘锛氬苟琛岃姹?
const [user, posts] = await Promise.all([
  getUser(id),
  getPosts(id)
]);
```

### 2. Bundle 澶у皬浼樺寲 (CRITICAL) - `bundle-` 鍓嶇紑

| 瑙勫垯 | 璇存槑 |
|------|------|
| `bundle-barrel-imports` | 鐩存帴浠庢簮鏂囦欢瀵煎叆锛岄伩鍏?barrel 鏂囦欢 |
| `bundle-dynamic-imports` | 瀵归噸鍨嬬粍浠朵娇鐢?`next/dynamic` |
| `bundle-defer-third-party` | 鍦?hydration 鍚庡姞杞藉垎鏋?鏃ュ織 |
| `bundle-conditional` | 浠呭湪鍔熻兘婵€娲绘椂鍔犺浇妯″潡 |
| `bundle-preload` | 鍦?hover/focus 鏃堕鍔犺浇璧勬簮 |

**绀轰緥锛?*
```typescript
// 鉂?閿欒锛氫粠 barrel 鏂囦欢瀵煎叆
import { Button } from '@/components';

// 鉁?姝ｇ‘锛氱洿鎺ュ鍏?
import { Button } from '@/components/Button';

// 鉁?鍔ㄦ€佸鍏ラ噸鍨嬬粍浠?
const HeavyChart = dynamic(() => import('./HeavyChart'), {
  loading: () => <Skeleton />,
  ssr: false
});
```

### 3. 鏈嶅姟绔€ц兘 (HIGH) - `server-` 鍓嶇紑

| 瑙勫垯 | 璇存槑 |
|------|------|
| `server-auth-actions` | 鍍?API 璺敱涓€鏍烽獙璇?server actions |
| `server-cache-react` | 浣跨敤 `React.cache()` 杩涜璇锋眰鍐呭幓閲?|
| `server-cache-lru` | 浣跨敤 LRU 缂撳瓨杩涜璺ㄨ姹傜紦瀛?|
| `server-dedup-props` | 閬垮厤 RSC props 涓殑閲嶅搴忓垪鍖?|
| `server-serialization` | 鏈€灏忓寲浼犻€掔粰瀹㈡埛绔粍浠剁殑鏁版嵁 |
| `server-parallel-fetching` | 閲嶆瀯缁勪欢浠ュ苟琛屽寲鑾峰彇 |
| `server-after-nonblocking` | 浣跨敤 `after()` 杩涜闈為樆濉炴搷浣?|

**绀轰緥锛?*
```typescript
// 鉁?浣跨敤 React.cache() 鍘婚噸
import { cache } from 'react';

const getUser = cache(async (id: string) => {
  return await db.user.findUnique({ where: { id } });
});
```

### 4. 瀹㈡埛绔暟鎹幏鍙?(MEDIUM-HIGH) - `client-` 鍓嶇紑

| 瑙勫垯 | 璇存槑 |
|------|------|
| `client-swr-dedup` | 浣跨敤 SWR 鑷姩璇锋眰鍘婚噸 |
| `client-event-listeners` | 鍘婚噸鍏ㄥ眬浜嬩欢鐩戝惉鍣?|
| `client-passive-event-listeners` | 瀵规粴鍔ㄤ簨浠朵娇鐢?passive 鐩戝惉鍣?|
| `client-localstorage-schema` | 鐗堟湰鍖栧苟鏈€灏忓寲 localStorage 鏁版嵁 |

**绀轰緥锛?*
```typescript
// 鉁?浣跨敤 SWR 鑷姩鍘婚噸鍜岀紦瀛?
import useSWR from 'swr';

function Profile() {
  const { data, error } = useSWR('/api/user', fetcher);
  // 澶氫釜缁勪欢璋冪敤鐩稿悓 key 鍙彂涓€娆¤姹?
}
```

### 5. 閲嶆覆鏌撲紭鍖?(MEDIUM) - `rerender-` 鍓嶇紑

| 瑙勫垯 | 璇存槑 |
|------|------|
| `rerender-defer-reads` | 涓嶈璁㈤槄浠呭湪鍥炶皟涓娇鐢ㄧ殑鐘舵€?|
| `rerender-memo` | 灏嗘槀璐靛伐浣滄彁鍙栧埌 memo 缁勪欢 |
| `rerender-memo-with-default-value` | 鎻愬崌榛樿闈炲師濮?props |
| `rerender-dependencies` | 鍦?effects 涓娇鐢ㄥ師濮嬩緷璧?|
| `rerender-derived-state` | 璁㈤槄娲剧敓甯冨皵鍊硷紝鑰岄潪鍘熷鍊?|
| `rerender-derived-state-no-effect` | 鍦ㄦ覆鏌撴湡闂存淳鐢熺姸鎬侊紝鑰岄潪 effects |
| `rerender-functional-setstate` | 浣跨敤鍑芥暟寮?setState 鑾峰緱绋冲畾鍥炶皟 |
| `rerender-lazy-state-init` | 瀵规槀璐靛€间紶閫掑嚱鏁扮粰 `useState` |
| `rerender-simple-expression-in-memo` | 閬垮厤瀵圭畝鍗曞師濮嬪€间娇鐢?memo |
| `rerender-move-effect-to-event` | 灏嗕氦浜掗€昏緫鏀惧湪浜嬩欢澶勭悊鍣ㄤ腑 |
| `rerender-transitions` | 瀵归潪绱ф€ユ洿鏂颁娇鐢?`startTransition` |
| `rerender-use-ref-transient-values` | 瀵归绻佸彉鍖栫殑鐬€佸€间娇鐢?refs |

**绀轰緥锛?*
```typescript
// 鉂?閿欒锛氭瘡娆℃覆鏌撳垱寤烘柊瀵硅薄
<Component style={{ color: 'red' }} />

// 鉁?姝ｇ‘锛氭彁鍗囧埌缁勪欢澶?
const style = { color: 'red' };
<Component style={style} />

// 鉁?浣跨敤 startTransition 澶勭悊闈炵揣鎬ユ洿鏂?
import { startTransition } from 'react';

function handleSearch(query: string) {
  startTransition(() => {
    setSearchResults(filterResults(query));
  });
}
```

### 6. 娓叉煋鎬ц兘 (MEDIUM) - `rendering-` 鍓嶇紑

| 瑙勫垯 | 璇存槑 |
|------|------|
| `rendering-animate-svg-wrapper` | 鍔ㄧ敾 div 鍖呰鍣紝鑰岄潪 SVG 鍏冪礌 |
| `rendering-content-visibility` | 瀵归暱鍒楄〃浣跨敤 content-visibility |
| `rendering-hoist-jsx` | 灏嗛潤鎬?JSX 鎻愬彇鍒扮粍浠跺 |
| `rendering-svg-precision` | 鍑忓皯 SVG 鍧愭爣绮惧害 |
| `rendering-hydration-no-flicker` | 浣跨敤鍐呰仈鑴氭湰澶勭悊浠呭鎴风鏁版嵁 |
| `rendering-hydration-suppress-warning` | 鎶戝埗棰勬湡鐨勪笉鍖归厤璀﹀憡 |
| `rendering-activity` | 浣跨敤 Activity 缁勪欢澶勭悊鏄剧ず/闅愯棌 |
| `rendering-conditional-render` | 浣跨敤涓夊厓杩愮畻绗︼紝鑰岄潪 && |
| `rendering-usetransition-loading` | 浼樺厛浣跨敤 useTransition 澶勭悊鍔犺浇鐘舵€?|

**绀轰緥锛?*
```css
/* 鉁?瀵归暱鍒楄〃浣跨敤 content-visibility */
.list-item {
  content-visibility: auto;
  contain-intrinsic-size: 0 50px;
}
```

### 7. JavaScript 鎬ц兘 (LOW-MEDIUM) - `js-` 鍓嶇紑

| 瑙勫垯 | 璇存槑 |
|------|------|
| `js-batch-dom-css` | 閫氳繃 classes 鎴?cssText 鎵归噺 CSS 鏇存敼 |
| `js-index-maps` | 涓洪噸澶嶆煡鎵炬瀯寤?Map |
| `js-cache-property-access` | 鍦ㄥ惊鐜腑缂撳瓨瀵硅薄灞炴€?|
| `js-cache-function-results` | 鍦ㄦā鍧楃骇 Map 涓紦瀛樺嚱鏁扮粨鏋?|
| `js-cache-storage` | 缂撳瓨 localStorage/sessionStorage 璇诲彇 |
| `js-combine-iterations` | 灏嗗涓?filter/map 鍚堝苟涓轰竴涓惊鐜?|
| `js-length-check-first` | 鍦ㄦ槀璐垫瘮杈冨墠鍏堟鏌ユ暟缁勯暱搴?|
| `js-early-exit` | 浠庡嚱鏁版彁鍓嶈繑鍥?|
| `js-hoist-regexp` | 灏?RegExp 鍒涘缓鎻愬崌鍒板惊鐜 |
| `js-min-max-loop` | 浣跨敤寰幆鑰岄潪 sort 鑾峰彇 min/max |
| `js-set-map-lookups` | 浣跨敤 Set/Map 杩涜 O(1) 鏌ユ壘 |
| `js-tosorted-immutable` | 浣跨敤 `toSorted()` 淇濇寔涓嶅彲鍙樻€?|

**绀轰緥锛?*
```typescript
// 鉂?閿欒锛氬娆￠亶鍘?
const filtered = items.filter(x => x.active);
const mapped = filtered.map(x => x.name);

// 鉁?姝ｇ‘锛氬崟娆￠亶鍘?
const result = [];
for (const item of items) {
  if (item.active) result.push(item.name);
}

// 鉁?浣跨敤 Set 杩涜 O(1) 鏌ユ壘
const activeIds = new Set(activeItems.map(x => x.id));
const isActive = activeIds.has(item.id);
```

### 8. 楂樼骇妯″紡 (LOW) - `advanced-` 鍓嶇紑

| 瑙勫垯 | 璇存槑 |
|------|------|
| `advanced-event-handler-refs` | 鍦?refs 涓瓨鍌ㄤ簨浠跺鐞嗗櫒 |
| `advanced-init-once` | 姣忎釜搴旂敤鍔犺浇鍙垵濮嬪寲涓€娆?|
| `advanced-use-latest` | useLatest 鐢ㄤ簬绋冲畾鍥炶皟寮曠敤 |

---

## 蹇€熷弬鑰?

```typescript
// 骞惰璇锋眰
const [a, b] = await Promise.all([fetchA(), fetchB()]);

// 鍔ㄦ€佸鍏?
const Heavy = dynamic(() => import('./Heavy'), { ssr: false });

// React.cache 鍘婚噸
const getData = cache(async (id) => fetch(`/api/${id}`));

// SWR 瀹㈡埛绔紦瀛?
const { data } = useSWR(key, fetcher);

// startTransition 闈炵揣鎬ユ洿鏂?
startTransition(() => setState(newValue));

// content-visibility 闀垮垪琛?
.item { content-visibility: auto; }
```

## 涓庡叾浠?Skills 閰嶅悎

| Skill | 閰嶅悎鏂瑰紡 |
|-------|----------|
| `frontend-design` | 璁捐 鈫?鏈?skill 浼樺寲瀹炵幇 |
| `web-design-guidelines` | 鏈?skill 鎬ц兘瑙勫垯 + 鍙闂€ц鍒?|

## 璧勬簮

- [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills)
- [React 瀹樻柟鏂囨。](https://react.dev)
- [Next.js 瀹樻柟鏂囨。](https://nextjs.org/docs)
