// LRU cache built on a doubly linked list + hash map.
// Mirrors LeetCode 146; head = most-recently-used, tail = least-recently-used.

export class Node {
  constructor(key, value) {
    this.key = key;
    this.value = value;
    this.prev = null;
    this.next = null;
  }
}

export class LRUCache {
  constructor(capacity) {
    if (!Number.isInteger(capacity) || capacity < 1) {
      throw new Error("LRUCache capacity must be a positive integer");
    }
    this.capacity = capacity;
    this.map = new Map();
    // Sentinel head/tail simplifies edge cases (no null checks on insert/remove).
    this.head = new Node(null, null);
    this.tail = new Node(null, null);
    this.head.next = this.tail;
    this.tail.prev = this.head;
  }

  get size() {
    return this.map.size;
  }

  has(key) {
    return this.map.has(key);
  }

  // Returns { hit, value, evicted }. evicted = the key dropped (or null).
  // touch=true means a hit also reorders to MRU (standard LRU).
  get(key) {
    const node = this.map.get(key);
    if (!node) return { hit: false, value: null };
    this._moveToFront(node);
    return { hit: true, value: node.value };
  }

  // put: insert new key, or refresh existing.
  // Returns the key that was evicted (or null).
  put(key, value) {
    let evicted = null;
    if (this.map.has(key)) {
      const node = this.map.get(key);
      node.value = value;
      this._moveToFront(node);
      return evicted;
    }
    if (this.map.size >= this.capacity) {
      const lru = this.tail.prev;
      this._remove(lru);
      this.map.delete(lru.key);
      evicted = lru.key;
    }
    const node = new Node(key, value);
    this._addFront(node);
    this.map.set(key, node);
    return evicted;
  }

  // Snapshot of slots from MRU → LRU. Pure read; doesn't mutate order.
  toArray() {
    const out = [];
    for (let n = this.head.next; n !== this.tail; n = n.next) {
      out.push({ key: n.key, value: n.value });
    }
    return out;
  }

  // ----- internal -----
  _remove(node) {
    node.prev.next = node.next;
    node.next.prev = node.prev;
    node.prev = null;
    node.next = null;
  }

  _addFront(node) {
    node.next = this.head.next;
    node.prev = this.head;
    this.head.next.prev = node;
    this.head.next = node;
  }

  _moveToFront(node) {
    this._remove(node);
    this._addFront(node);
  }
}
