// Cache Crash — LRU-cache reaction game.
// The cache slots ARE the playfield. Hit a slot when the request matches its emoji.

import { LRUCache } from "./lru.js";

const EMOJI_POOL = [
  "🍎", "🍌", "🍇", "🍓", "🍒", "🍍",
  "🥑", "🥕", "🌽", "🍔", "🍕", "🍩",
  "🐶", "🐱", "🦊", "🐼", "🐸", "🦁",
];

const CAPACITY = 5;
const ROUND_SECONDS = 60;
const HIT_POINTS = 10;
const MISS_POINTS = -5;
const REQUEST_INTERVAL_MS = 1500;
// Probability the next request is a key currently in the cache (pre-bias toward hits early on).
const HIT_BIAS_INITIAL = 0.5;
const HIT_BIAS_FLOOR = 0.25;

const els = {
  slots: document.getElementById("slots"),
  request: document.getElementById("request-emoji"),
  score: document.getElementById("score"),
  hits: document.getElementById("hits"),
  misses: document.getElementById("misses"),
  timer: document.getElementById("timer"),
  startBtn: document.getElementById("start-btn"),
  message: document.getElementById("message"),
};

class Game {
  constructor() {
    this.cache = new LRUCache(CAPACITY);
    this.score = 0;
    this.hits = 0;
    this.misses = 0;
    this.currentRequest = null;
    this.running = false;
    this.timeLeft = ROUND_SECONDS;
    this.requestTimer = null;
    this.tickTimer = null;
  }

  start() {
    this.cache = new LRUCache(CAPACITY);
    this.score = 0;
    this.hits = 0;
    this.misses = 0;
    this.timeLeft = ROUND_SECONDS;
    this.running = true;
    els.message.textContent = "";
    els.startBtn.textContent = "Restart";

    // Pre-fill cache with random distinct emojis so the first request can hit.
    const shuffled = [...EMOJI_POOL].sort(() => Math.random() - 0.5);
    for (let i = 0; i < CAPACITY; i++) {
      this.cache.put(shuffled[i], shuffled[i]);
    }

    this.nextRequest();
    this.render();

    this.requestTimer = setInterval(() => this.handleTimeout(), REQUEST_INTERVAL_MS);
    this.tickTimer = setInterval(() => this.tick(), 1000);
  }

  stop() {
    this.running = false;
    clearInterval(this.requestTimer);
    clearInterval(this.tickTimer);
    const totalAttempts = this.hits + this.misses;
    const rate = totalAttempts > 0 ? Math.round((this.hits / totalAttempts) * 100) : 0;
    els.message.textContent = `Game over. Score ${this.score} · hit rate ${rate}%`;
    els.startBtn.textContent = "Play again";
    this.currentRequest = null;
    els.request.textContent = "—";
  }

  tick() {
    this.timeLeft -= 1;
    if (this.timeLeft <= 0) {
      this.stop();
    }
    this.render();
  }

  nextRequest() {
    const slots = this.cache.toArray();
    const hitBias = Math.max(
      HIT_BIAS_FLOOR,
      HIT_BIAS_INITIAL - (ROUND_SECONDS - this.timeLeft) / ROUND_SECONDS * 0.3,
    );
    if (slots.length > 0 && Math.random() < hitBias) {
      this.currentRequest = slots[Math.floor(Math.random() * slots.length)].key;
    } else {
      // pick a random emoji NOT currently in the cache to force a miss option.
      const inCache = new Set(slots.map(s => s.key));
      const available = EMOJI_POOL.filter(e => !inCache.has(e));
      this.currentRequest = available.length > 0
        ? available[Math.floor(Math.random() * available.length)]
        : EMOJI_POOL[Math.floor(Math.random() * EMOJI_POOL.length)];
    }
    this.render();
  }

  // Player clicked a slot. If it matches the request → hit. Otherwise → wrong click penalty.
  handleSlotClick(emoji) {
    if (!this.running || !this.currentRequest) return;
    if (emoji === this.currentRequest) {
      this.cache.get(emoji);
      this.score += HIT_POINTS;
      this.hits += 1;
      this.flash("hit");
      this.nextRequest();
    } else {
      this.score += MISS_POINTS;
      this.misses += 1;
      this.flash("miss");
    }
    this.render();
  }

  // Player ran out of time on a request → auto-miss + LRU evicted, request takes its place.
  handleTimeout() {
    if (!this.running || !this.currentRequest) return;
    if (!this.cache.has(this.currentRequest)) {
      this.cache.put(this.currentRequest, this.currentRequest);
      this.misses += 1;
      this.score += MISS_POINTS;
      this.flash("miss");
    }
    this.nextRequest();
    this.render();
  }

  flash(kind) {
    els.request.classList.remove("hit-flash", "miss-flash");
    void els.request.offsetWidth; // restart animation
    els.request.classList.add(kind === "hit" ? "hit-flash" : "miss-flash");
  }

  render() {
    const slots = this.cache.toArray();
    els.slots.innerHTML = "";
    slots.forEach((slot, idx) => {
      const btn = document.createElement("button");
      btn.className = "slot";
      if (idx === slots.length - 1) btn.classList.add("lru");
      if (idx === 0) btn.classList.add("mru");
      btn.textContent = slot.value;
      btn.title = `${idx === 0 ? "MRU" : idx === slots.length - 1 ? "LRU (next to evict)" : `position ${idx}`}`;
      btn.addEventListener("click", () => this.handleSlotClick(slot.key));
      els.slots.appendChild(btn);
    });

    els.request.textContent = this.currentRequest ?? "—";
    els.score.textContent = String(this.score);
    els.hits.textContent = String(this.hits);
    els.misses.textContent = String(this.misses);
    els.timer.textContent = String(this.timeLeft);
  }
}

const game = new Game();
els.startBtn.addEventListener("click", () => game.start());
