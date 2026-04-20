/**
 * animations.jsx — Timeline animation engine
 *
 * Usage (load after React + Babel):
 *   <script type="text/babel" src="animations.jsx"></script>
 *
 *   <div id="root"></div>
 *   <script type="text/babel">
 *     function MyScene() {
 *       const t = useTime();
 *       return (
 *         <Stage totalDuration={6}>
 *           <Sprite start={0} end={2}>
 *             <div style={{ opacity: interpolate(useSprite(), Easing.easeOut, 0, 1) }}>
 *               Hello
 *             </div>
 *           </Sprite>
 *           <Sprite start={1.5} end={5}>
 *             <div>World</div>
 *           </Sprite>
 *         </Stage>
 *       );
 *     }
 *     ReactDOM.createRoot(document.getElementById('root')).render(<MyScene />);
 *   </script>
 */

// ── Context ──────────────────────────────────────────────────────────────────
const TimelineContext = React.createContext({ time: 0, duration: 1 });

// ── Easing library ───────────────────────────────────────────────────────────
const Easing = {
  linear: t => t,
  easeIn: t => t * t,
  easeOut: t => t * (2 - t),
  easeInOut: t => t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t,
  easeOutExpo: t => t === 1 ? 1 : 1 - Math.pow(2, -10 * t),
  easeOutBack: t => {
    const c1 = 1.70158;
    const c3 = c1 + 1;
    return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2);
  },
  easeOutElastic: t => {
    if (t === 0 || t === 1) return t;
    const c4 = (2 * Math.PI) / 3;
    return Math.pow(2, -10 * t) * Math.sin((t * 10 - 0.75) * c4) + 1;
  },
};

// ── interpolate ──────────────────────────────────────────────────────────────
/**
 * interpolate(progress, easingFn, from, to)
 * Maps a 0-1 progress through an easing function to [from, to].
 */
function interpolate(progress, easingFn, from, to) {
  const clamped = Math.max(0, Math.min(1, progress));
  const eased = (easingFn || Easing.linear)(clamped);
  return from + (to - from) * eased;
}

// ── useTime ──────────────────────────────────────────────────────────────────
/** Returns current global time in seconds from the nearest Stage. */
function useTime() {
  return React.useContext(TimelineContext).time;
}

// ── useSprite ────────────────────────────────────────────────────────────────
/** Returns 0-1 local progress within the nearest Sprite. */
const SpriteContext = React.createContext({ progress: 0 });
function useSprite() {
  return React.useContext(SpriteContext).progress;
}

// ── Stage ─────────────────────────────────────────────────────────────────────
const animStageStyles = {
  host: {
    position: 'relative',
    width: '100%',
    height: '100%',
    overflow: 'hidden',
  },
  scaler: {
    position: 'absolute',
    inset: 0,
    transformOrigin: 'top left',
  },
  controls: {
    position: 'fixed',
    bottom: '16px',
    left: '50%',
    transform: 'translateX(-50%)',
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    background: 'rgba(0,0,0,0.65)',
    backdropFilter: 'blur(12px)',
    borderRadius: '32px',
    padding: '8px 16px',
    zIndex: 9999,
    userSelect: 'none',
  },
  btn: {
    background: 'rgba(255,255,255,0.12)',
    border: 'none',
    borderRadius: '50%',
    width: '32px',
    height: '32px',
    cursor: 'pointer',
    color: '#fff',
    fontSize: '14px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  scrubber: {
    width: '160px',
    cursor: 'pointer',
    accentColor: '#c8a97e',
  },
  time: {
    color: 'rgba(255,255,255,0.5)',
    fontSize: '12px',
    fontVariantNumeric: 'tabular-nums',
    fontFamily: 'monospace',
    minWidth: '36px',
  },
};

/**
 * Stage — provides timeline context + auto-scale + play/pause scrubber.
 *
 * Props:
 *   totalDuration {number}  — seconds (default 5)
 *   autoPlay      {boolean} — start playing on mount (default true)
 *   loop          {boolean} — loop at end (default false)
 *   baseWidth     {number}  — design width for auto-scale (default 1920)
 *   baseHeight    {number}  — design height for auto-scale (default 1080)
 *   showControls  {boolean} — show scrubber UI (default true)
 */
function Stage({
  totalDuration = 5,
  autoPlay = true,
  loop = false,
  baseWidth = 1920,
  baseHeight = 1080,
  showControls = true,
  children,
}) {
  const [time, setTime] = React.useState(0);
  const [playing, setPlaying] = React.useState(autoPlay);
  const [scale, setScale] = React.useState(1);
  const rafRef = React.useRef(null);
  const lastRef = React.useRef(null);

  // RAF loop
  React.useEffect(() => {
    if (!playing) {
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
      return;
    }
    function tick(ts) {
      if (lastRef.current == null) lastRef.current = ts;
      const dt = (ts - lastRef.current) / 1000;
      lastRef.current = ts;
      setTime(prev => {
        const next = prev + dt;
        if (next >= totalDuration) {
          if (loop) return next % totalDuration;
          setPlaying(false);
          return totalDuration;
        }
        return next;
      });
      rafRef.current = requestAnimationFrame(tick);
    }
    lastRef.current = null;
    rafRef.current = requestAnimationFrame(tick);
    return () => { if (rafRef.current) cancelAnimationFrame(rafRef.current); };
  }, [playing, totalDuration, loop]);

  // Auto-scale
  React.useEffect(() => {
    function resize() {
      const sx = window.innerWidth / baseWidth;
      const sy = window.innerHeight / baseHeight;
      setScale(Math.min(sx, sy));
    }
    resize();
    window.addEventListener('resize', resize);
    return () => window.removeEventListener('resize', resize);
  }, [baseWidth, baseHeight]);

  const togglePlay = () => {
    if (!playing && time >= totalDuration) setTime(0);
    setPlaying(p => !p);
  };

  return (
    <TimelineContext.Provider value={{ time, duration: totalDuration }}>
      <div style={animStageStyles.host}>
        <div
          style={{
            ...animStageStyles.scaler,
            transform: `scale(${scale})`,
            width: baseWidth,
            height: baseHeight,
          }}
        >
          {children}
        </div>
        {showControls && (
          <div style={animStageStyles.controls}>
            <button style={animStageStyles.btn} onClick={togglePlay}>
              {playing ? '⏸' : '▶'}
            </button>
            <input
              type="range"
              min={0}
              max={totalDuration}
              step={0.01}
              value={time}
              style={animStageStyles.scrubber}
              onChange={e => {
                setPlaying(false);
                setTime(parseFloat(e.target.value));
              }}
            />
            <span style={animStageStyles.time}>{time.toFixed(2)}s</span>
          </div>
        )}
      </div>
    </TimelineContext.Provider>
  );
}

// ── Sprite ────────────────────────────────────────────────────────────────────
/**
 * Sprite — shows children only when global time is within [start, end].
 * Provides SpriteContext with local 0-1 progress to descendants.
 *
 * Props:
 *   start {number} — seconds when sprite becomes visible
 *   end   {number} — seconds when sprite becomes invisible
 */
function Sprite({ start, end, children }) {
  const { time } = React.useContext(TimelineContext);
  const duration = end - start;
  const local = duration > 0 ? Math.max(0, Math.min(1, (time - start) / duration)) : 0;
  const visible = time >= start && time <= end;

  if (!visible) return null;

  return (
    <SpriteContext.Provider value={{ progress: local }}>
      {children}
    </SpriteContext.Provider>
  );
}

// ── Exports ───────────────────────────────────────────────────────────────────
Object.assign(window, {
  Stage,
  Sprite,
  useTime,
  useSprite,
  Easing,
  interpolate,
  TimelineContext,
  SpriteContext,
});
