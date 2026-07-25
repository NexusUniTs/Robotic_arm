# Design System Strategy: Robotic Command Interface

## 1. Overview & Creative North Star
The Creative North Star for this system is **"The Nexus Laboratory."** 

This isn't a typical dashboard; it is a high-precision, tactical environment designed for an era where the digital and physical merge. While traditional industrial interfaces are rigid and literal, this system breaks the "template" look by using intentional asymmetry and depth-defying glassmorphism. It moves away from the flat, "web-app" aesthetic toward a sophisticated, HUD-inspired (Heads-Up Display) experience. 

We utilize a hierarchy of semi-transparent layers, where the UI feels like it’s floating over the hardware telemetry. By prioritizing JetBrains Mono for all data-driven readouts, we establish a sense of technical authority—every character feels programmed and precise.

## 2. Colors: Depth and Luminance
The palette is built on deep obsidian tones (`#0a0e14`) contrasted with high-vibrancy "neon" accents that guide the eye to critical nexus controls.

### The "No-Line" Rule
Explicitly prohibit 1px solid borders for sectioning. Boundaries must be defined solely through background color shifts. A `surface-container-low` section sitting on a `background` provides all the separation needed. If elements feel lost, adjust the tonal tier, do not reach for a line.

### Surface Hierarchy & Nesting
Treat the UI as a series of stacked sheets of synthetic material. 
- **Base Layer:** `surface` (#0a0e14)
- **Primary Layout Sections:** `surface-container` (#151a21)
- **Active Interactive Cards:** `surface-container-high` (#1b2028)
- **Floating Controls:** `surface-container-highest` (#20262f)

### The "Glass & Gradient" Rule
To achieve the futuristic command center feel, floating elements (like 6-axis control overlays) must use `surface-variant` with a `backdrop-blur` of 20px–40px. Use subtle gradients for primary CTAs, transitioning from `primary` (#8ff5ff) to `primary-container` (#00eefc) to provide visual "soul" that a flat fill cannot achieve.

## 3. Typography: The Engineering Aesthetic
The type system creates a dialogue between human-centric headlines and machine-centric telemetry.

- **Headline & Display:** Space Grotesk. Its geometric construction feels modern and slightly "off-grid." Use `display-lg` for macro-status (e.g., "SYSTEM ARMED").
- **Telemetry & Data:** JetBrains Mono. Use for all coordinate readouts, axis values, and the 6-axis slider labels. This mono-spacing ensures that as numbers fluctuate during robotic movement, the layout remains stable and readable.
- **Labels & Hierarchy:** Small caps and `label-sm` should be used for secondary axis data. High contrast between `on-surface` and `on-surface-variant` is required to keep the interface from feeling cluttered.

## 4. Elevation & Depth
Depth is a functional tool for safety and focus in a high-stakes robotic environment.

- **Tonal Layering:** Place a `surface-container-lowest` card on a `surface-container-low` section to create a soft, natural lift. No shadows are needed for static elements.
- **Ambient Shadows:** For floating telemetry cards, use extra-diffused shadows with 4%-8% opacity. Use a tint of the `primary` color for the shadow to simulate the light of a glowing screen reflecting off the backplate.
- **The "Ghost Border" Fallback:** If a border is required for accessibility on interactive sliders, use the `outline-variant` token at 15% opacity. Never use 100% opaque lines.
- **Emergency Priority:** The Neon Red Emergency Stop uses `tertiary` (#ff7073) with a outer glow (shadow) of the same color to ensure it is the most visually "elevated" object in the entire stack.

## 5. Components

### Control Sliders (6-Axis)
- **Track:** Use `surface-container-highest` for the background track.
- **Progress:** A gradient from `primary` to `primary-dim`. 
- **Thumb:** A high-gloss, glassmorphic circle using `primary-fixed` with a subtle white inner-glow to represent a physical touchpoint.

### Telemetry Cards
- **Construction:** No borders. Background: `surface-container-high` with 70% opacity and 30px backdrop blur.
- **Content:** Forbid divider lines. Use `spacing-6` (1.3rem) of vertical white space to separate data clusters. 
- **Header:** Use `label-md` in `on-surface-variant` for the data category (e.g., "TORQUE") and `headline-sm` in JetBrains Mono for the value.

### Buttons & Interaction
- **Primary (Action):** Gradient fill of `primary` to `primary-container`. Corner radius: `md` (0.375rem).
- **Secondary (Control):** `surface-variant` with `on-surface` text.
- **Emergency Stop:** A large, circular component using `tertiary` (#ff7073). On hover/active, the `tertiary-container` (#fc003b) should bloom, creating a pulsing neon effect.

### Chips & Status Indicators
- Use `secondary-container` for active state chips.
- Status indicators for "Connected/Disconnected" should be small glowing dots using `primary` (Active) or `error` (Failure), mimicking LED hardware lights.

## 6. Do's and Don'ts

### Do
- **DO** use the Spacing Scale religiously. Consistent gaps (like `8` for card padding and `4` for internal elements) replace the need for borders.
- **DO** overlap elements slightly. Placing a floating control card so it partially obscures a background telemetry feed creates a "stacked lens" look.
- **DO** use JetBrains Mono for any number that changes.

### Don't
- **DON'T** use `surface-container-lowest` for floating elements; that tier is for recessed backgrounds.
- **DON'T** use traditional grey shadows. They look "muddy" in a high-tech dark mode. Use tinted or ambient glows.
- **DON'T** use standard "Select" dropdowns. Use glassmorphic selection chips to maintain the HUD aesthetic.
- **DON'T** use 100% opacity backgrounds for modals. Use the `surface-variant` with a 0.8 opacity and heavy blur to maintain the sense of place.