---
name: Multimodal Face Analyzer
description: Every face, read back, one solid-colour story card per face, each answer credited to its model.
colors:
  pop-blue: "#4b3cff"
  pop-lime: "#c6f432"
  pop-pink: "#ff5ec4"
  pop-orange: "#ff7a1a"
  pop-violet: "#a98bff"
  ink-black: "#121212"
  ink-white: "#ffffff"
  night-ground: "#121212"
  night-surface: "#1b1b1b"
  night-surface-raised: "#252525"
  night-line: "#303030"
  night-line-strong: "#737373"
  night-text: "#ffffff"
  night-muted: "#a7a7a7"
  night-ok: "#6fe08a"
  night-warn: "#ffc44d"
  night-alert: "#ff7a6b"
  day-ground: "#f3f3f5"
  day-surface: "#ffffff"
  day-surface-raised: "#ebebef"
  day-line: "#dadae0"
  day-line-strong: "#7a7a85"
  day-text: "#121212"
  day-muted: "#55555f"
  day-ok: "#1d7a3a"
  day-warn: "#8a5a00"
  day-alert: "#c4261d"
typography:
  display:
    fontFamily: "'Bricolage Grotesque', sans-serif"
    fontSize: "clamp(4rem, 2.2rem + 3.6vw, 7rem)"
    fontWeight: 800
    lineHeight: 0.85
    letterSpacing: "-0.04em"
    fontVariation: "'wdth' 75"
  stat:
    fontFamily: "'Bricolage Grotesque', sans-serif"
    fontSize: "clamp(5rem, 3rem + 6vw, 8.5rem)"
    fontWeight: 800
    lineHeight: 0.8
    letterSpacing: "-0.04em"
    fontVariation: "'wdth' 75"
    fontFeature: "'tnum'"
  headline:
    fontFamily: "'Bricolage Grotesque', sans-serif"
    fontSize: "clamp(2.6rem, 1.4rem + 4vw, 5rem)"
    fontWeight: 800
    lineHeight: 0.9
    letterSpacing: "-0.035em"
    fontVariation: "'wdth' 78"
  title:
    fontFamily: "'Bricolage Grotesque', sans-serif"
    fontSize: "clamp(1.8rem, 1.3rem + 1.6vw, 2.6rem)"
    fontWeight: 800
    lineHeight: 1
    letterSpacing: "-0.012em"
    fontVariation: "'wdth' 78"
  caption:
    fontFamily: "'Bricolage Grotesque', sans-serif"
    fontSize: "1.35rem"
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.01em"
  body:
    fontFamily: "'Bricolage Grotesque', sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.45
  label:
    fontFamily: "'Bricolage Grotesque', sans-serif"
    fontSize: "0.9rem"
    fontWeight: 600
  credit:
    fontFamily: "'JetBrains Mono', monospace"
    fontSize: "0.8rem"
    fontWeight: 400
rounded:
  sm: "12px"
  md: "20px"
  lg: "28px"
  pill: "999px"
  circle: "50%"
spacing:
  "1": "0.25rem"
  "2": "0.5rem"
  "3": "0.75rem"
  "4": "1rem"
  "5": "1.5rem"
  "6": "2.25rem"
components:
  button-primary:
    backgroundColor: "{colors.pop-lime}"
    textColor: "{colors.ink-black}"
    rounded: "{rounded.pill}"
  button-primary-day:
    backgroundColor: "{colors.pop-blue}"
    textColor: "{colors.ink-white}"
    rounded: "{rounded.pill}"
  button-secondary:
    backgroundColor: "{colors.night-surface-raised}"
    textColor: "{colors.night-text}"
    rounded: "{rounded.pill}"
  story-card-lime:
    backgroundColor: "{colors.pop-lime}"
    textColor: "{colors.ink-black}"
    rounded: "{rounded.lg}"
    padding: "1.5rem"
  story-card-pink:
    backgroundColor: "{colors.pop-pink}"
    textColor: "{colors.ink-black}"
    rounded: "{rounded.lg}"
    padding: "1.5rem"
  story-card-blue:
    backgroundColor: "{colors.pop-blue}"
    textColor: "{colors.ink-white}"
    rounded: "{rounded.lg}"
    padding: "1.5rem"
  story-card-orange:
    backgroundColor: "{colors.pop-orange}"
    textColor: "{colors.ink-black}"
    rounded: "{rounded.lg}"
    padding: "1.5rem"
  story-card-violet:
    backgroundColor: "{colors.pop-violet}"
    textColor: "{colors.ink-black}"
    rounded: "{rounded.lg}"
    padding: "1.5rem"
  hero-block:
    backgroundColor: "{colors.pop-blue}"
    textColor: "{colors.ink-white}"
    typography: "{typography.headline}"
    rounded: "{rounded.lg}"
    padding: "clamp(1.5rem, 1rem + 2vw, 2.5rem)"
  stat-block:
    backgroundColor: "{colors.pop-lime}"
    textColor: "{colors.ink-black}"
    typography: "{typography.stat}"
    rounded: "{rounded.lg}"
    padding: "clamp(1.5rem, 1rem + 2vw, 2.5rem)"
  face-pill:
    backgroundColor: "{colors.ink-black}"
    textColor: "{colors.pop-lime}"
    rounded: "{rounded.pill}"
    padding: "0.2rem 0.75rem"
  chip:
    textColor: "{colors.night-text}"
    rounded: "{rounded.pill}"
    padding: "0.3rem 0.85rem"
  input:
    backgroundColor: "{colors.night-surface-raised}"
    textColor: "{colors.night-text}"
    rounded: "{rounded.sm}"
---

# Design System: Multimodal Face Analyzer

## Overview

**Creative North Star: "The Year-End Readback"**

Results read back like a year-in-review story: each detected face gets its own solid-colour card, and the card's headline answer is set huge in condensed display type, credited to the model that produced it. The page is a dark (Night) or pale (Day) neutral ground on which a few loud, flat colour blocks carry all the emphasis. The grey dashboard of identical metric tiles is the thing this system refuses.

Density is low where the visitor first lands (intro block, count block, one card per face) and stays ordinary in the sidebar and native Streamlit controls, which are restated quietly from the same tokens so they never compete with the colour blocks. Colour is flat fill, never gradient; depth is almost entirely absent; shape is soft and generous (20 to 28px corners, pill buttons, circular face crops).

The same card is drawn server-side as a 1080x1350 PNG in the same typeface and the same fill/ink pairs, so the shared artifact and the on-screen card are one object.

**Key Characteristics:**
- Solid colour blocks with oversized condensed type are the one motif.
- Five pop fills, each paired with its own ink; a card never mixes fills.
- Every answer carries a "feature · model" credit in mono.
- Face-number pills tie the annotated photo's boxes to the cards.
- Flat: no gradients, no glass, no decorative shadows on the blocks.

## Colors

A neutral ground under five saturated, flat pop fills, each with a fixed ink.

### Primary
- **Electric Ultramarine** (pop-blue): the intro block behind "Every face, read back."; the Day theme's accent (primary buttons, focus rings, face boxes, links); the third story-card fill, inked white.
- **Acid Lime** (pop-lime): the Night accent (primary buttons, focus rings, face boxes, slider thumb, links); the count block; the first story-card fill, inked black.

### Secondary
- **Hot Bubblegum** (pop-pink): the circle that bleeds off the intro block's corner; the second story-card fill.
- **Safety Orange** (pop-orange): the fourth story-card fill.
- **Soft Violet** (pop-violet): the fifth story-card fill.

### Neutral
- **Record Black** (night-ground / ink-black): Night page ground, and the ink on lime, pink, orange and violet fills.
- **Night Surfaces** (night-surface, night-surface-raised): sidebar, summary meta block, expanders, uploader (surface); inputs, secondary buttons, popovers (raised).
- **Night Lines** (night-line, night-line-strong): hairline dividers; control and chip outlines.
- **Night Muted** (night-muted): captions, inactive tabs, secondary copy.
- **Paper Fog** (day-ground) with **Day Surfaces, Lines, Text and Muted**: the same roles for the Day theme; Day text is Record Black.
- **Status** (night/day ok, warn, alert): tint alert containers only, mixed 12% into the surface with a 45% border.

### Named Rules
**The Fill-and-Ink Rule.** Every solid fill is paired with exactly one ink (black on lime, pink, orange, violet; white on blue), and everything on the fill (text, rules, pill, crop ring) uses that ink. Never put muted grey or the accent on a pop fill.

**The Rotation Rule.** Story cards take pop fills 1 to 5 in face order and wrap around; the same fill/ink pair colours that face's PNG share card.

**The Plain Hex Rule.** Theme colour tokens are plain `#rrggbb` so their WCAG AA contrast can be checked automatically; derived tints are `color-mix()` of tokens, never new hex values.

## Typography

**Display Font:** Bricolage Grotesque (variable: opsz, wdth 75 to 100, wght 400 to 800), with sans-serif
**Body Font:** Bricolage Grotesque at normal width
**Label/Mono Font:** JetBrains Mono, only for model credits, code and the slider value

**Character:** One grotesque does everything; the drama comes from squeezing it to 75 to 78% width at weight 800 with tight negative tracking for answers and numbers, then letting it run at normal width for reading.

### Hierarchy
- **Stat** (800, 75% width, clamp 5 to 8.5rem, line-height 0.8, tabular figures): the single number in the count blocks (analyses ready, faces found).
- **Display** (800, 75% width, clamp 4 to 7rem, line-height 0.85): a story card's headline answer; wraps anywhere rather than overflowing.
- **Headline** (800, 78% width, clamp 2.6 to 5rem, line-height 0.9): the intro block's h1 only.
- **Title** (800, 78% width, clamp 1.8 to 2.6rem): section headings such as "Face by face"; the summary block's image name runs slightly smaller (clamp 1.6 to 2.4rem, line-height 0.95).
- **Caption** (700, 1.35rem, line-height 1.1): the line under a stat number.
- **Body** (400, 1rem, line-height 1.45; intro copy 1.1rem, max 34rem): running text.
- **Label** (600, 0.9rem): chips, button labels, widget labels (500).
- **Credit** (JetBrains Mono 400, 0.8rem, 85% opacity): "feature · model" under every answer.

### Named Rules
**The Squeeze Rule.** Condensed width (75 to 78%) and weight 800 belong to answers, numbers and headings. Body and labels stay at normal width.

**The Credit Rule.** Every answer shown, on screen or in the PNG, carries its lowercase "feature · model" credit. Mono appears nowhere else except code and data values.

## Layout

A single wide column (max 1440px; 5.25rem top padding under the Streamlit header) with a sidebar for controls. The intro is a two-column grid: a flexible blue block beside a 14 to 22rem lime count block. Results put the annotated photo beside a summary (count block plus a surface meta block with chips), then a "Face by face" section of story cards in columns. Grids collapse to one column at 900px; at 640px the page padding drops to 4.5rem 1rem 3rem and the intro's pink circle is removed. Spacing follows a six-step scale (0.25, 0.5, 0.75, 1, 1.5, 2.25rem); blocks sit 1rem apart, sections open with 2.25rem.

## Elevation & Depth

Flat. The colour blocks and story cards carry no shadow; hierarchy comes from fill colour and type size. A single soft ambient shadow exists for things that float over the page (popovers, dialogs, dropdowns, the hover readout on the annotated image).

### Shadow Vocabulary
- **Float** (`box-shadow: 0 24px 48px -16px rgb(0 0 0 / 0.7)` Night, `0 24px 48px -18px rgb(18 18 18 / 0.3)` Day): floating layers only.

### Named Rules
**The Flat Block Rule.** Anything sitting in the page flow is flat. Only layers that overlay the page get the Float shadow.

## Shapes

Generous and soft: large blocks and story cards 28px, surfaces, images, uploader, expanders, popovers and alerts 20px, inputs and inline code 12px. Every button, chip and number pill is a full pill (999px). Face crops are circles with a 4px ink ring. Story-card rows are separated by 2px ink rules on the top edge; neutral surfaces use 1px hairlines. The only decorative geometry is the oversized pink circle bleeding off the intro block's bottom-right corner.

## Components

### Buttons
Confident pills.
- **Shape:** full pill (999px).
- **Primary:** accent fill with accent ink (lime/black at Night, blue/white by Day); the uploader's browse button uses the same treatment.
- **Hover / Focus:** primary mixes 14% toward the text colour; focus is a 2px accent outline offset 2px.
- **Secondary:** raised surface, 1px strong line, 600 label; hover tints to accent-soft with accent border and text; 120ms ease transitions.

### Chips
- **Style:** transparent, 2px strong-line outline, pill, 600 weight 0.9rem; a leading count may be set in the accent (bold).

### Cards / Containers
- **Story card:** solid pop fill, 28px corners, 1.5rem padding, min-height 22rem; head row with the face-number pill and circular crop (6.5rem), the display answer and its credit, then up to four further answers as rows with 2px ink top rules and right-aligned credits; an optional details disclosure in ink.
- **Hero and stat blocks:** 28px corners, fluid padding (1.5 to 2.5rem); stat blocks stack number and caption with space-between.
- **Surface block / readout card:** surface or raised fill, 20 to 28px corners, no border, key/value rows split by 1px hairlines.

### Inputs / Fields
- **Style:** raised surface, 1px strong line, 12px corners.
- **Focus:** border goes to the accent with a 3px accent ring at 22%; hover shows a 45% accent border.
- **Checkbox / slider:** checked box fills with the accent; slider track stays neutral and the thumb carries the accent with a 4px halo.

### Navigation
Upload/Webcam tabs are plain text (muted, 500) over a 1px line; the selected tab turns text-coloured, 600, with a 2px accent indicator. On narrow screens tabs share the width equally.

### Face-Number Pill (signature)
A two-digit face number in a pill, shared by the boxes on the annotated photo (box colour fill, box-outline ink, 0.72rem 800, sitting on the box's top edge) and the story cards (ink fill, card colour text, 1rem 800). It is how a visitor matches a box to its card.

### Story Reveal (signature motion)
Story cards fade and rise in: 520ms, `cubic-bezier(0.16, 1, 0.3, 1)`, from 16px down at 25% opacity, staggered 70ms per card. Under reduced motion the animation and all transitions are off.

### Share Card
A 1080x1350 PNG of one story card drawn on the server in Bricolage Grotesque: same fill/ink, number pill top-left, 300px circular crop with ink ring top-right, the headline answer auto-fitted down from 300px at 75% width, four ruled rows with credits, and the demo URL along the bottom margin (72px margins throughout).

## Do's and Don'ts

### Do:
- **Do** give each face its own solid pop fill in rotation and set its headline answer in the Display style.
- **Do** pair every fill with its single ink and draw rules, pills and crop rings in that ink.
- **Do** credit every answer "feature · model" in JetBrains Mono at 0.8rem.
- **Do** use the face-number pill wherever a face is referenced, on the photo and on cards.
- **Do** keep theme colours as plain hex tokens and derive tints with `color-mix()`.
- **Do** restate any new native Streamlit widget from the tokens for both Night and Day.

### Don't:
- **Don't** build results as a grid of identical grey metric tiles.
- **Don't** use gradients, glassy translucent surfaces, or coloured side stripes on cards or blocks.
- **Don't** put tracked-caps kickers or eyebrow labels above headings or answers.
- **Don't** shadow in-flow blocks; the Float shadow is for overlays only.
- **Don't** introduce a second display face or use mono for anything but credits, code and data values.
