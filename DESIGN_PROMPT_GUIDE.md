# 🧩 Design Prompt Guide

A comprehensive reasoning and prompting framework outlining how to communicate effectively with designers (and AI agents) to extend the Food Security Intelligence System.

## 1. Description Templates

When requesting new pages, components, or updates, follow this template to ensure the result matches the project aesthetic:

**Structure:**
1. **Goal:** [What are we building?]
2. **Aesthetic/Tone:** [Dark minimalist, tech-forward, etc.]
3. **Core Elements:** [Data viz, form, text-heavy, etc.]
4. **Color Constraints:** [Strictly adhere to the Emerald/Navy palette or introduce X warm tone]
5. **Animation Requests:** [Fade-ins, hover states, counters]

---

## 2. Prompt Arsenal (Copy & Paste)

### 🌑 1. The "Dark Minimalist" Approach
> "Create a dark, minimalist analytics dashboard page. Follow the Apple-inspired styling. Use #0f172a for the background and #1e293b for data cards. Remove all borders and rely entirely on spacing and subtle box-shadows. The page should focus on typography and generous white space. Use #10b981 sparingly—only for primary structural calls-to-action."

### 🔬 2. The "Tech-Forward / Deep Data" Approach
> "Reimagine the landing page with a tech-forward aesthetic. Maintain the dark theme but introduce subtle grid overlays in the background. Add animated data visualizations (like glowing SVG line charts). Emphasize the API architecture using code snippets with syntax highlighting. Use snappy, 200ms transitions on every interactive element."

### 🌍 3. The "Humanitarian Impact" Approach
> "Redesign the home section to emphasize human impact. We need to strike an emotional yet professional tone. Incorporate real farmer stories into elegant, glassmorphic cards. Use warmer secondary tones alongside the emerald green. Add large impact numbers prominently with counter animations. Make the overall feel hopeful and empowering."

---

## 3. Power Prompting Techniques

- **Constraint-basing:** Always define what *not* to do. (e.g., "Do not use primary bright blue. Do not use heavy borders.")
- **Emotional framing:** Start by defining the emotion the user should feel (e.g., "The user should feel a sense of urgent clarity.")
- **Reference pointing:** "Make the navigation feel like Apple's top nav. Make the dashboard cards feel like Vercel's UI."

## 4. Alternative Color Extensions
If extending the design beyond the primary palette:

* **Oceanic Trust:** Introduce `#0ea5e9` (Sky Blue) for secondary data points.
* **Earthy Warmth:** Introduce `#d97706` (Amber) for warnings and humanitarian emphasis.
* **Deep Monochrome:** Strip out all colors except stark `#ffffff` and `#0f172a`, using opacity steps for hierarchy.

Use these prompts and principles to ensure every new frontend file generated for the `famine-early-warning` project feels premium, cohesive, and intentional.
