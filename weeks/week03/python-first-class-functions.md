# Python First-Class Functions — Syntax & Term Reference

> A condensed summary of *Python 一級函式修煉手冊* (adapted from Luciano Ramalho's
> *Fluent Python*), organized around the **correct Python syntax names** for each concept.

**Contents**

1. [Functions as Objects](#1--functions-as-objects)
2. [Type Hints in Functions](#2--type-hints-in-functions)
3. [Decorators & Closures](#3--decorators--closures)
4. [Design Patterns with First-Class Functions](#4--design-patterns-with-first-class-functions)

---

## Quick Reference — the 6 most common function syntaxes

| # | Syntax | Name | One-liner |
|---|--------|------|-----------|
| 1 | `def f(...)` | function definition | Defines a named first-class function object. |
| 2 | `lambda x: ...` | anonymous function | A single-expression function, usually passed to a higher-order function. |
| 3 | `*args` | var-positional parameter | Collects extra positional args into a **tuple**. |
| 4 | `**kwargs` | var-keyword parameter | Collects extra keyword args into a **dict**. |
| 5 | `f(*it)` / `f(**d)` | iterable / dictionary unpacking | Spreads an iterable / dict into arguments at the **call site**. |
| 6 | `@decorator` | decorator | Sugar for `f = decorator(f)`; wraps or replaces a function. |

---

## 1 · Functions as Objects

### 1.1 First-class object
A function is a **first-class object**: it can be created at runtime, assigned to a
variable, passed as an argument, and returned from another function — just like `int`,
`str`, or `dict`. Every function is an instance of the `function` class.

```python
fact = factorial      # bind the function object to a new name (no call)
fact(5)               # 120 — the () is the call operator
```

### 1.2 Higher-order function
Takes a function as an argument **or** returns one — e.g. `sorted(..., key=len)`, `map`,
`filter`, `reduce`, `apply`.

| Built-in | Modern Pythonic replacement |
|----------|-----------------------------|
| `map` / `filter` (lazy iterators) | **list comprehension** |
| `reduce` (now in `functools`) | built-in `sum` for addition |
| `all` / `any` | reduce a sequence to one boolean (no replacement needed) |

### 1.3 Anonymous function (`lambda`)
Creates an **anonymous function** whose body must be a single **expression** (no
statements like `while`, `try`, or `=`). Best used as an argument to a higher-order
function. If a `lambda` gets hard to read, give it a name with `def`.

### 1.4 Callables — the call operator `()`
A **callable** is anything that works with the `()` **call operator**; test with the
built-in `callable(obj)`. Python 3.9 lists **nine** callable types:

| # | Callable type | Example |
|---|---------------|---------|
| 1 | User-defined function | `def` / `lambda` |
| 2 | Built-in function | `len` (implemented in C) |
| 3 | Built-in method | `dict.get` |
| 4 | Method | function defined in a class body |
| 5 | Class | calling it runs `__new__` then `__init__` |
| 6 | Class instance with `__call__` | see §1.5 |
| 7 | Generator function | uses `yield` → returns a generator |
| 8 | Native coroutine function | `async def` |
| 9 | Async generator function | `async def` + `yield` |

### 1.5 User-defined callable — `__call__`
Implement **`__call__`** so an instance can be invoked like a function — useful for
objects that must keep **state between calls**.

### 1.6 Parameter kinds in a signature
```python
def tag(name, /, *content, class_=None, **attrs): ...
```

| Token | Name |
|-------|------|
| `name` | positional parameter |
| `/` | marks everything to its left as **positional-only** (Python 3.8+) |
| `*content` | **var-positional** — extra positional args → *tuple* |
| `class_=None` | **keyword-only** (it follows `*content`) |
| `**attrs` | **var-keyword** — extra keyword args → *dict* |
| bare `*` | marks the start of **keyword-only parameters** |

### 1.7 Unpacking at the call site
At a **call**, `*` is **iterable unpacking** and `**` is **dictionary unpacking**:

```python
tag(**my_tag)         # expand dict into keyword arguments
```

### 1.8 The `operator` module
Replaces single-purpose lambdas with ready-made function versions of operators:

| Tool | Equivalent lambda | Notes |
|------|-------------------|-------|
| `mul`, `add`, … | `lambda a, b: a * b` | arithmetic / comparison operators |
| `itemgetter(1)` | `lambda x: x[1]` | uses `[]` / `__getitem__` |
| `attrgetter('a.b')` | `lambda x: x.a.b` | follows dotted paths into nested objects |
| `methodcaller('m', arg)` | `lambda x: x.m(arg)` | calls a named method, can bind args |

### 1.9 `functools.partial`
**Partial application**: freeze some arguments of a callable to produce a new callable
with fewer parameters. Exposes `.func`, `.args`, `.keywords`.

```python
triple = partial(mul, 3)     # triple(7) -> 21
```

---

## 2 · Type Hints in Functions

### 2.1 Gradual typing
**Type hints** (PEP 484) are **optional**, **not enforced at runtime**, and **don't make
code faster**. Checked statically by tools like **Mypy**, one function at a time.

> Useful Mypy flags: `--disallow-untyped-defs`, `--disallow-incomplete-defs`.

### 2.2 A type is defined by supported operations
The practical definition of a type = "the set of operations it supports."

| Concept | Meaning |
|---------|---------|
| **Duck typing** (Smalltalk/Python/Ruby) | values have types, variables don't; checked at runtime when an operation is attempted |
| **Nominal typing** (C++/Java, annotated Python) | variables *and* values have types; the static checker reads declared types, catching errors *before* runtime |
| **LSP** (Liskov Substitution Principle) / *behavioral subtyping* | `T2` is a subtype of `T1` if a `T2` can replace a `T1` everywhere |

### 2.3 Types usable in annotations

| Type | Notes |
|------|-------|
| **`Any`** | the *dynamic type*; consistent-with every type, top *and* bottom of the hierarchy. The more general a type, the fewer operations it supports. |
| simple types & classes | `int`, `float`, `str`, `bytes`, custom classes |
| **`Optional[str]`** | ≡ `Union[str, None]` (requires a `= None` default) |
| **`Union[...]`** | multiple incompatible types; avoid as a *return* type when possible |
| **generic collections** (PEP 585) | `list[str]`, `dict[str, set[str]]` (Python 3.9+); older code uses `typing.List` + `from __future__ import annotations` |
| **`tuple`** | record `tuple[str, float, str]`; named record `typing.NamedTuple`; unbounded `tuple[int, ...]` |
| **ABCs** | prefer `abc.Mapping`/`abc.Sequence`/`abc.Iterable` for *parameters* (Postel's Law: be liberal in what you accept); use concrete types for *returns* |

> **Consistent-with** (gradual) vs **is-subtype-of** (nominal) — two distinct relations.
> `Iterable` is best for *parameters*; `Iterator` for *returns*.

### 2.4 Parameterized generics & `TypeVar`
A **`TypeVar`** (type variable) ties the result type to the parameter type:

```python
T = TypeVar('T')
def sample(population: Sequence[T], size: int) -> list[T]: ...
```

| Form | Example | Meaning |
|------|---------|---------|
| Restricted | `TypeVar('T', float, Decimal, Fraction)` | must be one of the listed types |
| Bounded | `TypeVar('T', bound=Hashable)` | the inferred type, bounded above |
| Predefined | `AnyStr = TypeVar('AnyStr', bytes, str)` | ships with `typing` |

### 2.5 Static protocols (`typing.Protocol`)
**`Protocol`** (PEP 544) = *static duck typing*. A type is consistent-with a protocol if
it implements the declared methods — **no inheritance or registration needed**.

```python
class SupportsLessThan(Protocol):
    def __lt__(self, other: Any) -> bool: ...

LT = TypeVar('LT', bound=SupportsLessThan)
```

> Helpers: `typing.TYPE_CHECKING` (False at runtime, True for the checker),
> `reveal_type()` (Mypy-only debug helper).

### 2.6 `Callable` and variance
- **`Callable[[ParamType1, ParamType2], ReturnType]`** annotates callback / returned
  callables; `Callable[..., ReturnType]` for a flexible signature.
- **Variance**: `Callable` is **covariant** in its return type, **contravariant** in its
  parameter types.

### 2.7 `NoReturn`
Return annotation for functions that **never return** (e.g. `sys.exit()`).

### 2.8 Limits
Type hints **can't** express constraints like "positive int" or "6–12 ASCII chars," and
can break Pythonic features (`config(**settings)`, properties, metaclasses). Treat the
static checker as one CI tool among many — not the final word on correctness.

---

## 3 · Decorators & Closures

### 3.1 Decorator basics
A **decorator** is a callable that takes the **decorated function** as its argument and
may replace it. `@decorate` above `def target` is **syntactic sugar** for:

```python
target = decorate(target)
```

### 3.2 When Python runs decorators

| Phase | What happens |
|-------|--------------|
| **import time** | the decorator runs (when the module loads / the function is *defined*) |
| **runtime** | the decorated function runs (when *called*) |

This split is the basis of **registration decorators** / plugin systems.

### 3.3 Variable scope rules

| Rule | Meaning |
|------|---------|
| **local variable** | any name assigned to (or a parameter) in the body — decided by the **compiler**, regardless of statement order (else `UnboundLocalError`) |
| **`global x`** | `x` belongs to the module **global scope** |
| **`nonlocal x`** | `x` belongs to an enclosing function's scope (the closure) |

Lookup order: explicit `global`/`nonlocal` → local (assigned/param) → enclosing (nonlocal)
scope → module global → `__builtins__`.

> Inspect compiled bytecode with the `dis` module (`LOAD_GLOBAL` vs `LOAD_FAST`).

### 3.4 Closure
A **closure** is a function that retains bindings to **free variables** — names used in
its body that are defined in an *enclosing* (non-global) function's scope.

```python
func.__code__.co_freevars        # names of the free variables
func.__closure__[i].cell_contents # their retained values
```

### 3.5 `nonlocal`
Required when you must **rebind** (assign to) a free variable of **immutable** type inside
a nested function. (Mutating a mutable object like a list in place does *not* need it.)

### 3.6 A well-behaved decorator
- Use **`*args, **kwargs`** in the inner wrapper so any call signature passes through.
- Apply **`@functools.wraps(func)`** to copy `__name__`, `__doc__`, etc. from the wrapped
  function to the wrapper.

### 3.7 Standard-library decorators

| Decorator | Purpose |
|-----------|---------|
| `property`, `classmethod`, `staticmethod` | method decorators |
| **`functools.cache`** / **`functools.lru_cache`** | **memoization** (args must be *hashable*); `lru_cache(maxsize=128, typed=False)`, LRU = Least Recently Used |
| **`functools.singledispatch`** | **single-dispatch generic function** — dispatch on the type of the *first argument*; register impls with `@base.register`; prefer ABCs over concrete types (dispatch on multiple args = *multiple dispatch*) |

### 3.8 Parameterized decorators
A **decorator factory** takes arguments and returns the actual decorator — **three nested
layers**: factory → decorator → wrapper. The inner layers read the factory's arguments as
free variables (closure).

> `@register()` always needs the parentheses. Can also be implemented as a class with
> `__call__` (factory = `__init__`, decorator = `__call__`).

---

## 4 · Design Patterns with First-Class Functions

### 4.1 Design patterns are language-dependent
Per Peter Norvig, **16 of the 23 GoF patterns** become "invisible or much simpler" in
dynamic languages. With first-class functions, several patterns collapse.

### 4.2 Strategy pattern — classic version

| Role | In the e-commerce example |
|------|---------------------------|
| **Context** | `Order` — delegates an interchangeable algorithm |
| **Strategy** | abstract base class `Promotion(ABC)` with `@abstractmethod discount` |
| **Concrete strategies** | `FidelityPromo`, `BulkItemPromo`, `LargeOrderPromo` |

### 4.3 Function-oriented Strategy
Each concrete strategy is a single, **stateless** method — so replace it with a plain
**function**. Drop the ABC entirely; annotate the field as
`Optional[Callable[['Order'], Decimal]]` and call `self.promotion(self)` directly. Pass
the function itself (`fidelity_promo`, **not** `FidelityPromo()`).

> A module-level function is created once at import → it's already a shared object, so the
> **Flyweight** pattern (recommended by GoF to share strategy instances) is unnecessary.

### 4.4 Choosing the best strategy
```python
promos = [fidelity_promo, bulk_item_promo, large_order_promo]   # list of functions
def best_promo(order): return max(promo(order) for promo in promos)
```

### 4.5 Finding strategies automatically (introspection)

| Tool | Use |
|------|-----|
| `globals()` | dict of the current module's global symbol table; filter names ending in `_promo` |
| `inspect.getmembers(module, inspect.isfunction)` | collect functions from a dedicated module |

### 4.6 Decorator-enhanced Strategy (registration decorator)
Let each promotion "register itself" so the list never goes stale:

```python
Promotion = Callable[[Order], Decimal]   # type alias for readability
promos: list[Promotion] = []

def promotion(promo: Promotion) -> Promotion:
    promos.append(promo)                 # register
    return promo                         # return unchanged

@promotion
def fidelity(order: Order) -> Decimal: ...
```

Strategy functions can have any name and live in any module — applying `@promotion`
auto-registers them. A higher-level variant hides the list inside a `PromoRegistry`
object instead of a module-global.

---

*Source: 《Python 一級函式修煉手冊》 — adapted from Luciano Ramalho, "Fluent Python."*
