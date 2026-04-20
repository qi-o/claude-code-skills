/**
 * macos_window.jsx — macOS window chrome component
 *
 * Usage (load after React + Babel):
 *   <script type="text/babel" src="device_frames/macos_window.jsx"></script>
 *
 *   <MacOSWindow title="My App">
 *     <YourContent />
 *   </MacOSWindow>
 *
 * Features: traffic lights, optional title, 12px corners, drop shadow
 */

const macosWindowStyles = {
  window: {
    display: 'inline-flex',
    flexDirection: 'column',
    borderRadius: '12px',
    overflow: 'hidden',
    boxShadow: `
      0 0 0 0.5px rgba(0,0,0,0.25),
      0 2px 4px rgba(0,0,0,0.12),
      0 8px 24px rgba(0,0,0,0.15),
      0 20px 56px rgba(0,0,0,0.12)
    `,
    minWidth: '480px',
    background: '#fff',
  },
  titleBar: {
    display: 'flex',
    alignItems: 'center',
    height: '44px',
    padding: '0 16px',
    background: 'linear-gradient(180deg, #f6f6f6 0%, #ebebeb 100%)',
    borderBottom: '1px solid rgba(0,0,0,0.12)',
    position: 'relative',
    flexShrink: 0,
    userSelect: 'none',
  },
  titleBarDark: {
    background: 'linear-gradient(180deg, #3a3a3c 0%, #2c2c2e 100%)',
    borderBottom: '1px solid rgba(0,0,0,0.4)',
  },
  trafficLights: {
    display: 'flex',
    gap: '8px',
    alignItems: 'center',
    zIndex: 1,
  },
  dot: {
    width: '13px',
    height: '13px',
    borderRadius: '50%',
    boxShadow: 'inset 0 0 0 0.5px rgba(0,0,0,0.15)',
    flexShrink: 0,
  },
  titleText: {
    position: 'absolute',
    left: '50%',
    transform: 'translateX(-50%)',
    fontSize: '13px',
    fontWeight: '500',
    fontFamily: "-apple-system, 'SF Pro Text', sans-serif",
    letterSpacing: '-0.1px',
  },
  content: {
    flex: 1,
    overflow: 'auto',
  },
};

const TRAFFIC_LIGHTS = [
  { color: '#ff5f57', label: 'close' },
  { color: '#ffbd2e', label: 'minimize' },
  { color: '#28c840', label: 'maximize' },
];

function MacOSWindow({ title, children, darkMode = false, width, height, style }) {
  const barStyle = darkMode
    ? { ...macosWindowStyles.titleBar, ...macosWindowStyles.titleBarDark }
    : macosWindowStyles.titleBar;

  const titleColor = darkMode ? 'rgba(255,255,255,0.75)' : 'rgba(0,0,0,0.65)';

  return (
    <div
      style={{
        ...macosWindowStyles.window,
        background: darkMode ? '#1e1e1e' : '#fff',
        color: darkMode ? '#e8e6e3' : '#1a1a1a',
        ...(width ? { width } : {}),
        ...(height ? { height } : {}),
        ...style,
      }}
    >
      {/* Title bar */}
      <div style={barStyle}>
        <div style={macosWindowStyles.trafficLights}>
          {TRAFFIC_LIGHTS.map(({ color, label }) => (
            <div
              key={label}
              style={{ ...macosWindowStyles.dot, background: color }}
              aria-label={label}
            />
          ))}
        </div>
        {title && (
          <span style={{ ...macosWindowStyles.titleText, color: titleColor }}>
            {title}
          </span>
        )}
      </div>

      {/* Content area */}
      <div style={{ ...macosWindowStyles.content, ...(height ? { height: `calc(${height} - 44px)` } : {}) }}>
        {children}
      </div>
    </div>
  );
}

Object.assign(window, { MacOSWindow });
