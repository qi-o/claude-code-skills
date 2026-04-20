/**
 * ios_frame.jsx — iPhone 15 Pro bezel component
 *
 * Usage (load after React + Babel):
 *   <script type="text/babel" src="device_frames/ios_frame.jsx"></script>
 *
 *   <IOSFrame darkMode>
 *     <YourScreen />
 *   </IOSFrame>
 *
 * Viewport: 390×844   Corners: 55px   Notch: Dynamic Island
 */

const iosFrameStyles = {
  outer: {
    display: 'inline-flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  bezel: {
    position: 'relative',
    width: '430px',
    height: '932px',
    borderRadius: '55px',
    padding: '10px',
    background: 'linear-gradient(145deg, #2a2a2a 0%, #1a1a1a 50%, #111 100%)',
    boxShadow: `
      0 0 0 1px rgba(255,255,255,0.12),
      0 0 0 2px rgba(0,0,0,0.8),
      0 24px 80px rgba(0,0,0,0.7),
      inset 0 0 0 1px rgba(255,255,255,0.05)
    `,
  },
  screen: {
    position: 'relative',
    width: '100%',
    height: '100%',
    borderRadius: '47px',
    overflow: 'hidden',
    display: 'flex',
    flexDirection: 'column',
  },
  statusBar: {
    position: 'relative',
    width: '100%',
    height: '54px',
    display: 'flex',
    alignItems: 'flex-end',
    justifyContent: 'space-between',
    padding: '0 28px 10px',
    flexShrink: 0,
    zIndex: 10,
  },
  dynamicIsland: {
    position: 'absolute',
    top: '12px',
    left: '50%',
    transform: 'translateX(-50%)',
    width: '126px',
    height: '36px',
    borderRadius: '20px',
    background: '#000',
    zIndex: 20,
  },
  time: {
    fontSize: '15px',
    fontWeight: '600',
    fontFamily: "-apple-system, 'SF Pro Display', sans-serif",
    letterSpacing: '-0.3px',
  },
  icons: {
    display: 'flex',
    alignItems: 'center',
    gap: '6px',
  },
  content: {
    flex: 1,
    overflow: 'hidden',
    display: 'flex',
    flexDirection: 'column',
  },
  homeBar: {
    width: '134px',
    height: '5px',
    borderRadius: '3px',
    background: 'currentColor',
    opacity: 0.3,
    margin: '8px auto 10px',
    flexShrink: 0,
  },
};

function IOSStatusIcons({ dark }) {
  const c = dark ? '#fff' : '#000';
  return (
    <div style={iosFrameStyles.icons}>
      {/* Signal bars */}
      <svg width="17" height="12" viewBox="0 0 17 12" fill={c}>
        <rect x="0" y="7" width="3" height="5" rx="1" opacity="1"/>
        <rect x="4.5" y="4.5" width="3" height="7.5" rx="1" opacity="1"/>
        <rect x="9" y="2" width="3" height="10" rx="1" opacity="1"/>
        <rect x="13.5" y="0" width="3" height="12" rx="1" opacity="0.3"/>
      </svg>
      {/* Wifi */}
      <svg width="16" height="12" viewBox="0 0 16 12" fill="none" stroke={c} strokeWidth="1.6" strokeLinecap="round">
        <path d="M1 4.5 C3.5 2 5.8 1 8 1 C10.2 1 12.5 2 15 4.5" opacity="0.3"/>
        <path d="M3 7 C4.5 5.2 6.2 4.3 8 4.3 C9.8 4.3 11.5 5.2 13 7" opacity="0.7"/>
        <path d="M5.5 9.5 C6.3 8.5 7.1 8 8 8 C8.9 8 9.7 8.5 10.5 9.5"/>
        <circle cx="8" cy="11.5" r="0.8" fill={c} stroke="none"/>
      </svg>
      {/* Battery */}
      <svg width="25" height="12" viewBox="0 0 25 12" fill="none">
        <rect x="0.5" y="0.5" width="21" height="11" rx="3.5" stroke={c} strokeOpacity="0.35"/>
        <rect x="22" y="3.5" width="2.5" height="5" rx="1.5" fill={c} fillOpacity="0.4"/>
        <rect x="2" y="2" width="16" height="8" rx="2" fill={c}/>
      </svg>
    </div>
  );
}

function IOSFrame({ children, darkMode = false }) {
  const bg = darkMode ? '#000' : '#fff';
  const fg = darkMode ? '#fff' : '#000';

  return (
    <div style={iosFrameStyles.outer}>
      <div style={iosFrameStyles.bezel}>
        <div style={{ ...iosFrameStyles.screen, background: bg, color: fg }}>
          {/* Dynamic Island */}
          <div style={iosFrameStyles.dynamicIsland} />

          {/* Status bar */}
          <div style={{ ...iosFrameStyles.statusBar, color: fg }}>
            <span style={iosFrameStyles.time}>9:41</span>
            <IOSStatusIcons dark={darkMode} />
          </div>

          {/* App content */}
          <div style={iosFrameStyles.content}>{children}</div>

          {/* Home indicator */}
          <div style={{ ...iosFrameStyles.homeBar, color: fg }} />
        </div>
      </div>
    </div>
  );
}

Object.assign(window, { IOSFrame });
