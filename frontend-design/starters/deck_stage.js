/**
 * deck_stage.js — Slide-deck shell Web Component
 *
 * Usage:
 *   <script src="deck_stage.js"></script>
 *   <deck-stage>
 *     <section><!-- Slide 1 content --></section>
 *     <section><!-- Slide 2 content --></section>
 *   </deck-stage>
 *
 * Features:
 *   - 1920×1080 canvas letterboxed via transform:scale into full viewport
 *   - Keyboard: ← → Home End Space
 *   - Touch swipe (60px threshold)
 *   - localStorage persistence ('deck_stage_index')
 *   - postMessage({slideIndexChanged: N}) to parent on every change
 *   - Auto data-screen-label on each <section>: "01 Title", "02 Agenda", …
 *   - Slide counter overlay "3/10" bottom-right
 *   - Optional speaker notes via <script type="application/json" id="speaker-notes">
 *   - Print-to-PDF: one page per section, no transform scaling
 */

(function () {
  'use strict';

  const SLIDE_W = 1920;
  const SLIDE_H = 1080;
  const STORAGE_KEY = 'deck_stage_index';
  const ANIM_MS = 500;

  const TEMPLATE = document.createElement('template');
  TEMPLATE.innerHTML = `
    <style>
      :host {
        display: block;
        width: 100vw;
        height: 100vh;
        background: #000;
        overflow: hidden;
        position: relative;
      }

      /* Outer centering stage */
      #stage {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
      }

      /* Fixed 1920×1080 canvas — JS applies scale */
      #canvas {
        position: relative;
        width: ${SLIDE_W}px;
        height: ${SLIDE_H}px;
        overflow: hidden;
        transform-origin: center center;
        flex-shrink: 0;
      }

      /* Each slide section */
      ::slotted(section) {
        position: absolute;
        inset: 0;
        opacity: 0;
        visibility: hidden;
        transition: opacity ${ANIM_MS}ms cubic-bezier(0.16, 1, 0.3, 1),
                    transform ${ANIM_MS}ms cubic-bezier(0.16, 1, 0.3, 1);
        transform: translateX(0);
        will-change: opacity, transform;
      }

      ::slotted(section.active) {
        opacity: 1;
        visibility: visible;
      }

      ::slotted(section.enter-right) {
        opacity: 0;
        transform: translateX(80px);
      }

      ::slotted(section.enter-left) {
        opacity: 0;
        transform: translateX(-80px);
      }

      /* Slide counter overlay */
      #counter {
        position: fixed;
        bottom: 20px;
        right: 28px;
        font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
        font-size: 14px;
        font-weight: 500;
        color: rgba(255,255,255,0.45);
        letter-spacing: 0.04em;
        font-variant-numeric: tabular-nums;
        z-index: 1000;
        pointer-events: none;
        user-select: none;
      }

      /* Print styles */
      @media print {
        :host {
          width: auto;
          height: auto;
          background: white;
          overflow: visible;
        }
        #stage {
          display: block;
          width: auto;
          height: auto;
        }
        #canvas {
          transform: none !important;
          width: 100%;
          height: auto;
          position: static;
        }
        ::slotted(section) {
          position: relative;
          opacity: 1 !important;
          visibility: visible !important;
          transform: none !important;
          page-break-after: always;
          width: 100%;
          height: auto;
          min-height: 100vh;
          display: block !important;
        }
        #counter {
          display: none;
        }
      }
    </style>

    <div id="stage">
      <div id="canvas">
        <slot></slot>
      </div>
    </div>
    <div id="counter"></div>
  `;

  class DeckStage extends HTMLElement {
    constructor() {
      super();
      this._root = this.attachShadow({ mode: 'open' });
      this._root.appendChild(TEMPLATE.content.cloneNode(true));

      this._canvas = this._root.getElementById('canvas');
      this._counter = this._root.getElementById('counter');
      this._slides = [];
      this._current = 0;
      this._animating = false;
      this._notes = [];

      this._onResize = this._onResize.bind(this);
      this._onKeydown = this._onKeydown.bind(this);
      this._onTouchStart = this._onTouchStart.bind(this);
      this._onTouchEnd = this._onTouchEnd.bind(this);
      this._touchStartX = 0;
      this._touchStartY = 0;
    }

    connectedCallback() {
      // Wait for slot to populate
      this._root.querySelector('slot').addEventListener('slotchange', () => {
        this._init();
      });
      // Also init immediately in case children are already present
      if (this.children.length > 0) this._init();

      window.addEventListener('resize', this._onResize);
      document.addEventListener('keydown', this._onKeydown);
      document.addEventListener('touchstart', this._onTouchStart, { passive: true });
      document.addEventListener('touchend', this._onTouchEnd, { passive: true });
    }

    disconnectedCallback() {
      window.removeEventListener('resize', this._onResize);
      document.removeEventListener('keydown', this._onKeydown);
      document.removeEventListener('touchstart', this._onTouchStart);
      document.removeEventListener('touchend', this._onTouchEnd);
    }

    _init() {
      this._slides = Array.from(this.querySelectorAll(':scope > section'));
      if (this._slides.length === 0) return;

      // Label every section 1-indexed: "01 Title", "02 Agenda", etc.
      this._slides.forEach((section, i) => {
        const num = String(i + 1).padStart(2, '0');
        // Use existing label if provided, else generic
        const existing = section.dataset.screenLabel;
        if (!existing) {
          const heading = section.querySelector('h1,h2,h3');
          const label = heading
            ? heading.textContent.trim().split('\n')[0].slice(0, 24)
            : ['Title', 'Agenda', 'Content', 'Summary', 'Close'][i] || 'Slide';
          section.dataset.screenLabel = `${num} ${label}`;
        }
      });

      // Load optional speaker notes
      const notesEl = document.getElementById('speaker-notes');
      if (notesEl && notesEl.type === 'application/json') {
        try {
          this._notes = JSON.parse(notesEl.textContent);
        } catch (e) {
          this._notes = [];
        }
      }

      // Restore saved index
      const saved = this._loadState();
      this._current = (saved >= 0 && saved < this._slides.length) ? saved : 0;

      this._updateCounter();
      this._scaleCanvas();
      this._goTo(this._current, false);
    }

    // ── Scaling ──────────────────────────────────────────────────
    _scaleCanvas() {
      const scaleX = window.innerWidth / SLIDE_W;
      const scaleY = window.innerHeight / SLIDE_H;
      const scale = Math.min(scaleX, scaleY);
      this._canvas.style.transform = `scale(${scale})`;
    }

    _onResize() {
      this._scaleCanvas();
    }

    // ── Navigation ───────────────────────────────────────────────
    _goTo(index, animate) {
      if (index < 0 || index >= this._slides.length) return;
      if (this._animating && animate) return;

      const prev = this._current;
      const dir = index > prev ? 'right' : 'left';

      if (animate && prev !== index) {
        this._animating = true;
        const incoming = this._slides[index];
        const outgoing = this._slides[prev];

        // Position incoming off-screen
        incoming.classList.add(dir === 'right' ? 'enter-right' : 'enter-left');
        incoming.classList.add('active');

        // Force reflow so transition fires
        void incoming.offsetWidth;
        incoming.classList.remove('enter-right', 'enter-left');

        // Slide out current
        outgoing.style.transform = dir === 'right' ? 'translateX(-80px)' : 'translateX(80px)';
        outgoing.style.opacity = '0';
        outgoing.style.transition = `opacity ${ANIM_MS}ms cubic-bezier(0.16,1,0.3,1), transform ${ANIM_MS}ms cubic-bezier(0.16,1,0.3,1)`;

        setTimeout(() => {
          outgoing.classList.remove('active');
          outgoing.style.transform = '';
          outgoing.style.opacity = '';
          outgoing.style.transition = '';
          this._animating = false;
        }, ANIM_MS);
      } else {
        this._slides.forEach((s, i) => {
          s.classList.toggle('active', i === index);
        });
      }

      this._current = index;
      this._updateCounter();
      this._saveState();
      this._notify();
    }

    next() { this._goTo(this._current + 1, true); }
    prev() { this._goTo(this._current - 1, true); }
    goTo(n) { this._goTo(n, true); }

    // ── UI ───────────────────────────────────────────────────────
    _updateCounter() {
      this._counter.textContent = `${this._current + 1}\u2009/\u2009${this._slides.length}`;
    }

    // ── postMessage ──────────────────────────────────────────────
    _notify() {
      try {
        window.parent.postMessage({ slideIndexChanged: this._current }, '*');
      } catch (e) { /* cross-origin frame — silently skip */ }
    }

    // ── localStorage ─────────────────────────────────────────────
    _saveState() {
      try { localStorage.setItem(STORAGE_KEY, String(this._current)); } catch (e) {}
    }

    _loadState() {
      try {
        const v = localStorage.getItem(STORAGE_KEY);
        if (v !== null) { const n = parseInt(v, 10); if (!isNaN(n)) return n; }
      } catch (e) {}
      return 0;
    }

    // ── Keyboard ─────────────────────────────────────────────────
    _onKeydown(e) {
      switch (e.key) {
        case 'ArrowRight': case 'ArrowDown': case ' ':
          e.preventDefault(); this.next(); break;
        case 'ArrowLeft': case 'ArrowUp':
          e.preventDefault(); this.prev(); break;
        case 'Home':
          e.preventDefault(); this._goTo(0, true); break;
        case 'End':
          e.preventDefault(); this._goTo(this._slides.length - 1, true); break;
      }
    }

    // ── Touch ────────────────────────────────────────────────────
    _onTouchStart(e) {
      this._touchStartX = e.touches[0].clientX;
      this._touchStartY = e.touches[0].clientY;
    }

    _onTouchEnd(e) {
      const dx = e.changedTouches[0].clientX - this._touchStartX;
      const dy = e.changedTouches[0].clientY - this._touchStartY;
      if (Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > 60) {
        dx < 0 ? this.next() : this.prev();
      }
    }
  }

  customElements.define('deck-stage', DeckStage);
})();
