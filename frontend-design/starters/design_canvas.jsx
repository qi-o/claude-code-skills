/**
 * design_canvas.jsx — Multi-option design comparison grid
 *
 * Usage (load after React + Babel):
 *   <script type="text/babel" src="design_canvas.jsx"></script>
 *
 *   <div id="root"></div>
 *   <script type="text/babel">
 *     ReactDOM.createRoot(document.getElementById('root')).render(
 *       <DesignCanvas>
 *         <CanvasCell label="Option A"><YourComponentA /></CanvasCell>
 *         <CanvasCell label="Option B"><YourComponentB /></CanvasCell>
 *         <CanvasCell label="Option C"><YourComponentC /></CanvasCell>
 *       </DesignCanvas>
 *     );
 *   </script>
 *
 * Layout rules:
 *   1 cell  → full width
 *   2 cells → 50/50 side by side
 *   3+ cells → responsive auto-fill (minmax 360px, 1fr)
 */

const designCanvasStyles = {
  root: {
    minHeight: '100vh',
    background: '#0f0f10',
    padding: '48px 40px',
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Inter', sans-serif",
    boxSizing: 'border-box',
  },
  grid1: {
    display: 'grid',
    gridTemplateColumns: '1fr',
    gap: '32px',
  },
  grid2: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '32px',
  },
  gridN: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))',
    gap: '32px',
  },
  cell: {
    position: 'relative',
    border: '1.5px dashed rgba(255,255,255,0.15)',
    borderRadius: '12px',
    overflow: 'hidden',
    background: 'rgba(255,255,255,0.02)',
    minHeight: '240px',
  },
  labelPill: {
    position: 'absolute',
    top: '12px',
    left: '12px',
    zIndex: 10,
    background: 'rgba(255,255,255,0.08)',
    border: '1px solid rgba(255,255,255,0.14)',
    borderRadius: '20px',
    padding: '4px 12px',
    fontSize: '11px',
    fontWeight: '600',
    letterSpacing: '0.08em',
    textTransform: 'uppercase',
    color: 'rgba(255,255,255,0.55)',
    backdropFilter: 'blur(8px)',
    WebkitBackdropFilter: 'blur(8px)',
    userSelect: 'none',
    pointerEvents: 'none',
  },
  cellContent: {
    width: '100%',
    height: '100%',
    display: 'flex',
    flexDirection: 'column',
  },
};

function DesignCanvas({ children, style }) {
  const childCount = React.Children.count(children);
  const gridStyle =
    childCount === 1
      ? designCanvasStyles.grid1
      : childCount === 2
      ? designCanvasStyles.grid2
      : designCanvasStyles.gridN;

  return (
    <div style={{ ...designCanvasStyles.root, ...style }}>
      <div style={gridStyle}>{children}</div>
    </div>
  );
}

function CanvasCell({ label, children, style }) {
  return (
    <div style={{ ...designCanvasStyles.cell, ...style }}>
      {label && <div style={designCanvasStyles.labelPill}>{label}</div>}
      <div style={designCanvasStyles.cellContent}>{children}</div>
    </div>
  );
}

// Export to window so other <script type="text/babel"> blocks can use these
Object.assign(window, { DesignCanvas, CanvasCell });
