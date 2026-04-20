/**
 * android_frame.jsx — Pixel-style Android bezel component
 *
 * Usage (load after React + Babel):
 *   <script type="text/babel" src="device_frames/android_frame.jsx"></script>
 *
 *   <AndroidFrame>
 *     <YourScreen />
 *   </AndroidFrame>
 *
 * Viewport: 412×915   Corners: 40px   Camera: punch-hole center-top
 */

const androidFrameStyles = {
  outer: {
    display: 'inline-flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  bezel: {
    position: 'relative',
    width: '452px',
    height: '975px',
    borderRadius: '48px',
    padding: '10px',
    background: 'linear-gradient(160deg, #1c1c1e 0%, #111 60%, #0a0a0b 100%)',
    boxShadow: `
      0 0 0 1px rgba(255,255,255,0.10),
      0 0 0 2px rgba(0,0,0,0.85),
      0 28px 90px rgba(0,0,0,0.65),
      inset 0 0 0 1px rgba(255,255,255,0.04)
    `,
  },
  screen: {
    position: 'relative',
    width: '100%',
    height: '100%',
    borderRadius: '40px',
    overflow: 'hidden',
    display: 'flex',
    flexDirection: 'column',
    background: '#fff',
  },
  statusBar: {
    position: 'relative',
    width: '100%',
    height: '36px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '0 20px',
    flexShrink: 0,
    zIndex: 10,
  },
  punchHole: {
    position: 'absolute',
    top: '8px',
    left: '50%',
    transform: 'translateX(-50%)',
    width: '12px',
    height: '12px',
    borderRadius: '50%',
    background: '#000',
    zIndex: 20,
  },
  statusTime: {
    fontSize: '12px',
    fontWeight: '700',
    fontFamily: "'Roboto', sans-serif",
    letterSpacing: '0.01em',
  },
  statusRight: {
    display: 'flex',
    alignItems: 'center',
    gap: '5px',
  },
  content: {
    flex: 1,
    overflow: 'hidden',
    display: 'flex',
    flexDirection: 'column',
  },
  navBar: {
    width: '100%',
    height: '48px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-evenly',
    padding: '0 32px',
    flexShrink: 0,
    borderTop: '1px solid rgba(0,0,0,0.06)',
  },
  navBtn: {
    opacity: 0.5,
    fontSize: '18px',
    lineHeight: 1,
    cursor: 'default',
  },
};

function AndroidStatusIcons({ dark }) {
  const c = dark ? '#fff' : '#000';
  return (
    <div style={androidFrameStyles.statusRight}>
      {/* Signal */}
      <svg width="14" height="11" viewBox="0 0 14 11" fill={c}>
        <rect x="0" y="7" width="2.5" height="4" rx="0.8"/>
        <rect x="3.8" y="4.5" width="2.5" height="6.5" rx="0.8"/>
        <rect x="7.6" y="2" width="2.5" height="9" rx="0.8"/>
        <rect x="11.4" y="0" width="2.5" height="11" rx="0.8" opacity="0.3"/>
      </svg>
      {/* Wifi */}
      <svg width="14" height="11" viewBox="0 0 14 11" fill="none" stroke={c} strokeWidth="1.4" strokeLinecap="round">
        <path d="M1 3.5 C3 1.5 5.5 0.5 7 0.5 C8.5 0.5 11 1.5 13 3.5" opacity="0.3"/>
        <path d="M3 6 C4.2 4.5 5.6 3.8 7 3.8 C8.4 3.8 9.8 4.5 11 6" opacity="0.7"/>
        <path d="M5 8.5 C5.7 7.6 6.3 7.2 7 7.2 C7.7 7.2 8.3 7.6 9 8.5"/>
        <circle cx="7" cy="10.5" r="0.8" fill={c} stroke="none"/>
      </svg>
      {/* Battery */}
      <svg width="22" height="11" viewBox="0 0 22 11" fill="none">
        <rect x="0.5" y="0.5" width="18" height="10" rx="2.5" stroke={c} strokeOpacity="0.4"/>
        <rect x="19" y="3" width="2.5" height="5" rx="1.5" fill={c} fillOpacity="0.4"/>
        <rect x="2" y="2" width="14" height="7" rx="1.5" fill={c}/>
      </svg>
    </div>
  );
}

function AndroidFrame({ children, darkMode = false }) {
  const bg = darkMode ? '#121212' : '#fff';
  const fg = darkMode ? '#fff' : '#000';

  return (
    <div style={androidFrameStyles.outer}>
      <div style={androidFrameStyles.bezel}>
        <div style={{ ...androidFrameStyles.screen, background: bg, color: fg }}>
          {/* Punch-hole camera */}
          <div style={androidFrameStyles.punchHole} />

          {/* Status bar */}
          <div style={{ ...androidFrameStyles.statusBar, color: fg }}>
            <span style={androidFrameStyles.statusTime}>9:41</span>
            <AndroidStatusIcons dark={darkMode} />
          </div>

          {/* App content */}
          <div style={androidFrameStyles.content}>{children}</div>

          {/* 3-button nav bar */}
          <div style={{ ...androidFrameStyles.navBar, borderTopColor: darkMode ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)' }}>
            <span style={{ ...androidFrameStyles.navBtn, color: fg, fontSize: '14px' }}>◁</span>
            <span style={{ ...androidFrameStyles.navBtn, color: fg, fontSize: '20px' }}>○</span>
            <span style={{ ...androidFrameStyles.navBtn, color: fg, fontSize: '16px' }}>□</span>
          </div>
        </div>
      </div>
    </div>
  );
}

Object.assign(window, { AndroidFrame });
