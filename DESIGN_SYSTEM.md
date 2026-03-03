# 🎨 Food Security Intelligence - Design System

A complete style guide for extending and maintaining the premium Apple-inspired aesthetic of the Food Security Intelligence System.

## 1. Core Principles
- **Minimalist luxury:** Let the content breathe. Avoid visual clutter.
- **Purposeful interaction:** Use subtle, 60fps animations to guide the user's eye and reward interaction.
- **Data-driven storytelling:** Present complex agricultural data with stark simplicity.
- **Mobile-first:** Ensure all components scale effortlessly from 320px to 4K displays.

## 2. Color Palette (Design Tokens)

### Foundation Colors
* **Primary (Emerald Green):** `#10b981` — Represents growth, hope, and action.
* **Background (Deep Navy):** `#0f172a` — Premium, sophisticated dark canvas.
* **Surface (Lighter Navy):** `#1e293b` — Used for cards, panels, and elevated containers.
* **Text Main:** `#f1f5f9` — High-contrast off-white for maximum legibility.
* **Text Muted:** `#cbd5e1` — Secondary text and subtle borders.

### Risk System Colors
Consistent semantic coloring for threat levels across all dashboards:
* **Safe / Low Risk:** `#10b981` (Green)
* **Moderate Risk:** `#f59e0b` (Yellow)
* **High Risk:** `#f97316` (Orange)
* **Critical Risk:** `#dc2626` (Red)

## 3. Typography
We utilize system font stacks to eliminate loading times while retaining a stark, modern sans-serif aesthetic.

**Font Stack:** `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif`

* **Display (h1):** 4rem / 1.1 line-height / Bold (-1px letter spacing)
* **Heading (h2):** 2.5rem / 1.2 line-height / Semi-bold
* **Title (h3):** 1.5rem / 1.3 line-height / Medium
* **Body:** 1rem / 1.6 line-height / Regular
* **Muted / Small:** 0.875rem / 1.5 line-height / Regular 

## 4. Spacing System (8px Grid)
* `--spacing-xs`: 0.5rem (8px)
* `--spacing-sm`: 1rem (16px)
* `--spacing-md`: 1.5rem (24px)
* `--spacing-lg`: 2rem (32px)
* `--spacing-xl`: 4rem (64px)
* `--spacing-xxl`: 8rem (128px)

## 5. UI Components

### Elevated Cards
```css
.card {
  background: var(--surface);
  border-radius: 16px;
  padding: var(--spacing-lg);
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.card:hover {
  transform: translateY(-4px);
}
```

### Primary Buttons
```css
.btn-primary {
  background-color: var(--primary);
  color: #000;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}
.btn-primary:hover {
  background-color: #059669;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(16, 185, 129, 0.4);
}
```

## 6. Animations
All animations should feel physical and snappy.

* **Fade Up Reveal:** (Applied via IntersectionObserver on scroll)
```css
.reveal {
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}
.reveal.active {
  opacity: 1;
  transform: translateY(0);
}
```

## 7. Responsive Breakpoints
* **Mobile:** `< 640px` (Stack all grids, 100% width, 16px lateral padding)
* **Tablet:** `640px - 1024px` (2-column grids)
* **Desktop:** `> 1024px` (3+ column grids, max-width bounded to 1200px)
