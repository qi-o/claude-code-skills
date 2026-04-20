/**
 * browser_window.jsx — Browser chrome component
 *
 * Usage (load after React + Babel):
 *   <script type="text/babel" src="device_frames/browser_window.jsx"></script>
 *
 *   <BrowserWindow url="https://example.com">
 *     <YourContent />
 *   </BrowserWindow>
 *
 * Features: traffic lights, tab bar, URL field, back/forward/refresh buttons
 */

const browserWindowStyles = {
  window: {
    display: 'inline-flex',
    flexDirection: 'column',
    borderRadius: '10px',
    overflow: 'hidden',
    boxShadow: `
      0 0 0 0.5px rgba(0,0,0,0.22),
      0 2px 6px rgba(0,0,0,0.10),
      0 10px 30px rgba(0,0,0,0.14),
      0 24px 64px rgba(0,0,0,0.10)
    `,
    minWidth: '560px',
    background: '#fff',
  },
  chrome: {
    flexShrink: 0,
    userSelect: 'none',
  },
  tabBar: {
    display: 'flex',
    alignItems: 'flex-end',
    height: '36px',
    padding: '0 12px',
    gap: '0',
    background: '#dee1e6',
  },
  tabBarDark: {
    background: '#2a2a2c',
  },
  trafficRow: {
    display: 'flex',
    alignItems: 'center',
    gap: '6px',
    paddingRight: '16px',
    alignSelf: 'center',
  },
  dot: {
    width: '12px',
    height: '12px',
    borderRadius: '50%',
    boxShadow: 'inset 0 0 0 0.5px rgba(0,0,0,0.12)',
    flexShrink: 0,
  },
  tab: {
    height: '28px',
    padding: '0 16px',
    borderRadius: '8px 8px 0 0',
    background: '#f0f0f2',
    fontSize: '12px',
    fontWeight: '500',
    fontFamily: "-apple-system, 'Segoe UI', sans-serif",
    display: 'flex',
    alignItems: 'center',
    gap: '6px',
    color: '#333',
    maxWidth: '200px',
    overflow: 'hidden',
    whiteSpace: 'nowrap',
    textOverflow: 'ellipsis',
    borderBottom: '2px solid transparent',
    flexShrink: 0,
  },
  tabActive: {
    background: '#fff',
    borderBottom: '2px solid #fff',
  },
  tabDark: {
    background: '#3a3a3c',
    color: '#e8e6e3',
  },
  tabActiveDark: {
    background: '#1c1c1e',
    borderBottom: '2px solid #1c1c1e',
  },
  toolbar: {
    display: 'flex',
    alignItems: 'center',
    height: '44px',
    padding: '0 12px',
    gap: '8px',
    background: '#f0f0f2',
    borderBottom: '1px solid rgba(0,0,0,0.10)',
  },
  toolbarDark: {
    background: '#1c1c1e',
    borderBottom: '1px solid rgba(255,255,255,0.08)',
  },
  navBtn: {
    width: '28px',
    height: '28px',
    borderRadius: '6px',
    border: 'none',
    background: 'transparent',
    cursor: 'default',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '13px',
    color: 'inherit',
    opacity: 0.5,
    flexShrink: 0,
  },
  urlBar: {
    flex: 1,
    height: '28px',
    borderRadius: '6px',
    background: 'rgba(0,0,0,0.06)',
    display: 'flex',
    alignItems: 'center',
    padding: '0 10px',
    gap: '6px',
    overflow: 'hidden',
  },
  urlBarDark: {
    background: 'rgba(255,255,255,0.08)',
  },
  urlText: {
    fontSize: '12px',
    fontFamily: "-apple-system, 'Segoe UI', sans-serif",
    color: 'inherit',
    opacity: 0.65,
    overflow: 'hidden',
    whiteSpace: 'nowrap',
    textOverflow: 'ellipsis',
    flex: 1,
  },
  lockIcon: {
    opacity: 0.4,
    fontSize: '10px',
    flexShrink: 0,
  },
  content: {
    flex: 1,
    overflow: 'auto',
  },
};

const BROWSER_TRAFFIC = [
  { color: '#ff5f57' },
  { color: '#ffbd2e' },
  { color: '#28c840' },
];

function BrowserWindow({ url = 'example.com', title, children, darkMode = false, width, height, style }) {
  const displayUrl = url.replace(/^https?:\/\//, '');
  const isSecure = url.startsWith('https://') || !url.startsWith('http://');

  const tabStyle = darkMode
    ? { ...browserWindowStyles.tab, ...browserWindowStyles.tabDark, ...browserWindowStyles.tabActiveDark }
    : { ...browserWindowStyles.tab, ...browserWindowStyles.tabActive };

  const toolbarStyle = darkMode
    ? { ...browserWindowStyles.toolbar, ...browserWindowStyles.toolbarDark, color: '#e8e6e3' }
    : { ...browserWindowStyles.toolbar, color: '#1a1a1a' };

  const urlBarStyle = darkMode
    ? { ...browserWindowStyles.urlBar, ...browserWindowStyles.urlBarDark }
    : browserWindowStyles.urlBar;

  const tabBarStyle = darkMode
    ? { ...browserWindowStyles.tabBar, ...browserWindowStyles.tabBarDark }
    : browserWindowStyles.tabBar;

  return (
    <div
      style={{
        ...browserWindowStyles.window,
        background: darkMode ? '#1c1c1e' : '#fff',
        color: darkMode ? '#e8e6e3' : '#1a1a1a',
        ...(width ? { width } : {}),
        ...(height ? { height } : {}),
        ...style,
      }}
    >
      <div style={browserWindowStyles.chrome}>
        {/* Tab bar */}
        <div style={tabBarStyle}>
          <div style={browserWindowStyles.trafficRow}>
            {BROWSER_TRAFFIC.map(({ color }, i) => (
              <div key={i} style={{ ...browserWindowStyles.dot, background: color }} />
            ))}
          </div>
          <div style={tabStyle}>
            {/* Favicon placeholder */}
            <svg width="12" height="12" viewBox="0 0 12 12" fill="currentColor" opacity="0.4">
              <circle cx="6" cy="6" r="5" fill="none" stroke="currentColor" strokeWidth="1.5"/>
              <path d="M6 1 C4 3 4 9 6 11 M6 1 C8 3 8 9 6 11 M1.5 4.5 L10.5 4.5 M1.5 7.5 L10.5 7.5" stroke="currentColor" strokeWidth="1" fill="none"/>
            </svg>
            {title || displayUrl}
          </div>
        </div>

        {/* Toolbar */}
        <div style={toolbarStyle}>
          <button style={{ ...browserWindowStyles.navBtn, color: 'inherit' }}>‹</button>
          <button style={{ ...browserWindowStyles.navBtn, color: 'inherit' }}>›</button>
          <button style={{ ...browserWindowStyles.navBtn, color: 'inherit', fontSize: '11px' }}>↻</button>

          <div style={urlBarStyle}>
            {isSecure && <span style={browserWindowStyles.lockIcon}>🔒</span>}
            <span style={browserWindowStyles.urlText}>{displayUrl}</span>
          </div>
        </div>
      </div>

      {/* Content */}
      <div style={{ ...browserWindowStyles.content, ...(height ? { height: `calc(${height} - 80px)` } : {}) }}>
        {children}
      </div>
    </div>
  );
}

Object.assign(window, { BrowserWindow });
