// Cache Crash — turn-based LRU sandbox.
// Click any key → see exactly what an LRU cache does:
//   - present in cache → cache.get(key) reorders it to MRU
//   - not in cache    → cache.put(key) inserts at MRU, evicting current LRU when full

import { LRUCache } from "./lru.js";

const KEYS = ["A", "B", "C", "D", "E", "F", "G", "H"];
const CAPACITY = 4;

const els = {
  keys: document.getElementById("keys"),
  slots: document.getElementById("slots"),
  hits: document.getElementById("hits"),
  misses: document.getElementById("misses"),
  rate: document.getElementById("rate"),
  resetBtn: document.getElementById("reset-btn"),
  message: document.getElementById("message"),
};

class Game {
  constructor() {
    this.reset();
  }

  reset() {
    this.cache = new LRUCache(CAPACITY);
    this.hits = 0;
    this.misses = 0;
    this.lastEvent = null;
    this.renderKeys();
    this.render();
  }

  request(key) {
    if (this.cache.has(key)) {
      this.cache.get(key);
      this.hits += 1;
      this.lastEvent = { kind: "hit", key };
    } else {
      const evicted = this.cache.put(key, key);
      this.misses += 1;
      this.lastEvent = { kind: "miss", key, evicted };
    }
    this.render();
  }

  renderKeys() {
    els.keys.innerHTML = "";
    KEYS.forEach((k) => {
      const btn = document.createElement("button");
      btn.className = "key";
      btn.textContent = k;
      btn.addEventListener("click", () => this.request(k));
      els.keys.appendChild(btn);
    });
  }

  render() {
    const slots = this.cache.toArray();

    els.slots.innerHTML = "";
    for (let i = 0; i < CAPACITY; i++) {
      const cell = document.createElement("div");
      cell.className = "slot";
      if (i < slots.length) {
        cell.textContent = slots[i].value;
        if (i === 0) cell.classList.add("mru");
        if (i === slots.length - 1 && slots.length > 1) cell.classList.add("lru");
      } else {
        cell.classList.add("empty");
        cell.textContent = "·";
      }
      els.slots.appendChild(cell);
    }

    // Reflect cache membership on key buttons (cached = highlighted).
    const cached = new Set(slots.map((s) => s.key));
    [...els.keys.children].forEach((btn) => {
      btn.classList.toggle("cached", cached.has(btn.textContent));
    });

    els.hits.textContent = String(this.hits);
    els.misses.textContent = String(this.misses);
    const total = this.hits + this.misses;
    els.rate.textContent = total > 0 ? `${Math.round((this.hits / total) * 100)}%` : "—";

    els.message.textContent = this.describeLastEvent();
    this.flash();
  }

  describeLastEvent() {
    const e = this.lastEvent;
    if (!e) return "Click any key to start.";
    if (e.kind === "hit") return `Hit: ${e.key} was already in the cache, moved to the front.`;
    if (e.evicted) return `Miss: added ${e.key} to the front, dropped ${e.evicted} (it was the oldest).`;
    return `Miss: added ${e.key} to the front.`;
  }

  flash() {
    const e = this.lastEvent;
    if (!e) return;
    const target = [...els.slots.children].find((s) => s.textContent === e.key);
    if (!target) return;
    target.classList.remove("hit-flash", "miss-flash");
    void target.offsetWidth; // restart animation
    target.classList.add(e.kind === "hit" ? "hit-flash" : "miss-flash");
  }
}

const game = new Game();
els.resetBtn.addEventListener("click", () => game.reset());
