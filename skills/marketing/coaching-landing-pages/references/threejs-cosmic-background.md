# Three.js Cosmic Particle Background

Reusable 3D background pattern for dark/luxury sites. 800 particles + torus rings + mouse parallax + scroll fade.

## Quick Start

```typescript
// Dynamic import to avoid SSR issues with Three.js
const CosmicBackground = dynamic(
  () => import("@/components/CosmicBackground"),
  { ssr: false }
);
```

## Core Elements

1. **Particles** — 800 points, spherical distribution, vertex colors (gold+white+purple), additive blending
2. **Rings** — Two torus geometries (gold + purple), slowly rotating
3. **Glow Sphere** — ShaderMaterial with radial alpha falloff, ambient gold glow
4. **Mouse Parallax** — Lerp-smoothed camera movement (factor 0.02)
5. **Scroll Fade** — Opacity and camera z decrease on scroll

## Key Code

```typescript
// Canvas texture for soft particle glow
const canvas = document.createElement("canvas");
canvas.width = 64; canvas.height = 64;
const ctx = canvas.getContext("2d")!;
const gradient = ctx.createRadialGradient(32, 32, 0, 32, 32, 32);
gradient.addColorStop(0, "rgba(255,255,255,0.9)");
gradient.addColorStop(0.15, "rgba(255,255,255,0.7)");
gradient.addColorStop(0.4, "rgba(201,168,76,0.3)");
gradient.addColorStop(1, "rgba(0,0,0,0)");
ctx.fillStyle = gradient;
ctx.fillRect(0, 0, 64, 64);
const texture = new THREE.CanvasTexture(canvas);

// Spherical distribution
const theta = Math.random() * Math.PI * 2;
const phi = Math.acos(2 * Math.random() - 1);
const radius = 10 + Math.random() * 30;
positions[i * 3] = Math.sin(phi) * Math.cos(theta) * radius;
positions[i * 3 + 1] = Math.sin(phi) * Math.sin(theta) * radius * 0.6; // flatten Y
positions[i * 3 + 2] = Math.cos(phi) * radius - 10;
```

## Dependencies

```json
{
  "three": "^0.170.0",
  "@react-three/fiber": "^9.0.0",
  "@react-three/drei": "^9.0.0"
}
```

## Pitfalls

- **SSR crash** — Three.js requires `window`; always `dynamic(() => import(...), { ssr: false })`
- **Memory leaks** — Dispose geometry, material, texture, renderer in useEffect cleanup
- **Performance** — `pixelRatio: Math.min(devicePixelRatio, 2)` om 4K schermen niet te crashen
- **Dark mode only** — Additive blending werkt niet op lichte achtergronden
