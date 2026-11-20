/* Spindle: the live 3D sconce for the home page.
   Scene, materials, lights, chrome probe and film pass are ported unchanged from the approved demo
   (~/projects/frosted-glass, commit 2c2c024). Do not retune them here without Austin seeing it.
   What this file adds for the site:
     - one canvas, one WebGL context, moved between the hosts marked [data-sconce] (hero, pick)
     - framing per host and a scroll pull-back on the hero (track gets .pull, progress in --p)
     - a label you can change: house label drawn here (no real artwork), or the visitor's own photo, local only
     - phone manners: vertical swipes scroll the page, the loop stops off screen, pixel ratio steps down if slow
   Loaded after window load by the inline module in index.html. If anything here fails the still image stays. */
import * as THREE from 'three';
import { RGBELoader } from './vendor/addons/loaders/RGBELoader.js';
import { EffectComposer } from './vendor/addons/postprocessing/EffectComposer.js';
import { RenderPass } from './vendor/addons/postprocessing/RenderPass.js';
import { ShaderPass } from './vendor/addons/postprocessing/ShaderPass.js';
import { OutputPass } from './vendor/addons/postprocessing/OutputPass.js';

const root = document.documentElement;
const hosts = {};
document.querySelectorAll('[data-sconce]').forEach(el => { hosts[el.dataset.sconce] = el; });
const track = document.querySelector('.hero3d');
const params = new URLSearchParams(location.search);
const MAXQ = params.get('q') === 'max';                 // capture mode: never step quality down
const calm = matchMedia('(prefers-reduced-motion: reduce)').matches;
const mobile = matchMedia('(pointer: coarse)').matches;
const tick = () => new Promise(r => setTimeout(r, 0));   // let the page breathe between heavy steps

const canvas = document.createElement('canvas');
canvas.className = 'sconce-canvas';
canvas.setAttribute('role', 'img');
canvas.setAttribute('aria-label', 'Live 3D model of the Spindle: a black record on a wall with a chrome dome at its centre and a warm glow behind it. Drag to tilt it.');

let renderer;
try {
  renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: 'high-performance' });
} catch (e) { root.classList.add('no3d'); throw e; }
let PR = Math.min(Math.max(devicePixelRatio, 1) * 1.5, 3); // supersampled so circle edges stay clean
renderer.setPixelRatio(PR);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.VSMShadowMap;
renderer.shadowMap.autoUpdate = false;

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(30, 1, 0.1, 100);

// ---------- dimensions (12 in record scaled so radius = 1.5) ----------
const R = 1.5, LABEL_R = 0.5, THICK = 0.016, STANDOFF = 0.34;
const GAPS = [0.62, 0.86, 1.10];           // silent bands between the songs
const mkRand = seed => { let s = seed; return () => (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296; };
const rand = mkRand(20241971);

// ---------- the room the chrome sees: a photographed hotel room (Poly Haven, CC0) ----------
// It lives on layer 1, so only the reflection probe sees it. The page camera never does.
const ROOM_LAYER = 1;
const ROOM_LEVEL = 0.5;                  // a dim evening room: walls fall to grey, windows and lamps stay hot
const roomMat = new THREE.MeshBasicMaterial({ color: 0x000000 });
const roomGeo = new THREE.SphereGeometry(40, 64, 32); roomGeo.scale(1, 1, -1);
const room = new THREE.Mesh(roomGeo, roomMat);
room.layers.set(ROOM_LAYER);
room.rotation.set(-0.3, -0.35, 0);
scene.add(room);
const pmrem = new THREE.PMREMGenerator(renderer);
const hdrReady = new Promise(done => {
  new RGBELoader().load(new URL('../assets/hotel_room_1k.hdr', import.meta.url).href, hdr => {
    hdr.colorSpace = THREE.LinearSRGBColorSpace;
    roomMat.map = hdr; roomMat.color.setScalar(ROOM_LEVEL); roomMat.needsUpdate = true;
    const envScene = new THREE.Scene();
    const copy = new THREE.Mesh(roomGeo, roomMat); copy.rotation.copy(room.rotation);
    envScene.add(copy);
    scene.environment = pmrem.fromScene(envScene, 0, 0.1, 100).texture;
    done(true);
  }, undefined, () => done(false));
});

// ---------- the wall ----------
function wallBump() {   // orange-peel roller texture of painted drywall
  const n = 256, small = document.createElement('canvas'); small.width = small.height = n;
  const sg = small.getContext('2d'), id = sg.createImageData(n, n);
  for (let i = 0; i < n * n; i++) { const v = 96 + rand() * 64; id.data[i * 4] = id.data[i * 4 + 1] = id.data[i * 4 + 2] = v; id.data[i * 4 + 3] = 255; }
  sg.putImageData(id, 0, 0);
  const c = document.createElement('canvas'); c.width = c.height = 512;
  const g = c.getContext('2d'); g.imageSmoothingEnabled = true; g.imageSmoothingQuality = 'high';
  g.drawImage(small, 0, 0, 512, 512);
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(28, 28);
  t.anisotropy = 8; return t;
}
const wall = new THREE.Mesh(
  new THREE.PlaneGeometry(60, 60),      // demo was 30 with repeat 14: same texel size, room for the pull-back
  new THREE.MeshStandardMaterial({ color: '#8a8178', roughness: 0.9, metalness: 0, envMapIntensity: 0.6, bumpMap: wallBump(), bumpScale: 0.6 })
);
wall.receiveShadow = true;
scene.add(wall);

// warm wash the LED strip throws on the wall: hottest just behind the rim, long soft tail
function haloTex() {
  const N = 1024, c = document.createElement('canvas'); c.width = c.height = N;
  const g = c.getContext('2d'), m = N / 2;
  const grd = g.createRadialGradient(m, m, 0, m, m, m);
  const S = 2.1;                         // plane half-size in record radii
  for (let i = 0; i <= 64; i++) {
    const rr = i / 64 * S;               // radius in record radii
    const d = Math.abs(rr - 0.9);        // the strip sits just inside the rim
    let a = 1 / (1 + Math.pow(d / 0.16, 2.0));
    a *= 1 - THREE.MathUtils.smoothstep(rr, S * 0.72, S);
    a *= THREE.MathUtils.smoothstep(rr, 0.15, 0.6);
    const warm = Math.min(1, d / 0.5);   // deeper orange as it thins out
    grd.addColorStop(i / 64, `rgba(255,${Math.round(178 - 44 * warm)},${Math.round(98 - 52 * warm)},${a.toFixed(4)})`);
  }
  g.fillStyle = grd; g.fillRect(0, 0, N, N);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}
const HALO = 0.5;
const haloMap = haloTex();
const mkHalo = () => new THREE.Mesh(
  new THREE.PlaneGeometry(R * 4.2, R * 4.2),
  new THREE.MeshBasicMaterial({ map: haloMap, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, opacity: HALO })
);
const halo = mkHalo();
halo.position.z = 0.002;
scene.add(halo);

// ---------- lights ----------
const key = new THREE.SpotLight('#fff1e0', 34, 30, Math.PI / 5, 1.0, 1.4); // overhead, soft edge
key.position.set(0, 9.5, 5.5);
key.castShadow = true;
key.shadow.mapSize.set(2048, 2048);
key.shadow.radius = 14;
key.shadow.blurSamples = 24;
key.shadow.bias = -0.0004;
scene.add(key, key.target);
// the lamp itself, so the mirror has something to catch: a small hot disc where the key light hangs
const lamp = new THREE.Mesh(new THREE.CircleGeometry(0.55, 48), new THREE.MeshBasicMaterial({ color: new THREE.Color(1, 0.93, 0.84).multiplyScalar(26) }));
lamp.position.copy(key.position); lamp.lookAt(0, 0, 0); lamp.layers.set(ROOM_LAYER);
scene.add(lamp);
const mkLed = () => new THREE.PointLight('#ffae5a', 3.6, 4, 1.6); // the strip, behind the disc
const ledRing = mkLed();
ledRing.position.set(0, 0, STANDOFF * 0.5);
scene.add(ledRing);
scene.add(new THREE.HemisphereLight('#fff4ea', '#2a2420', 0.2));

// ---------- the record ----------
const sconce = new THREE.Group();          // pivots about the center post
sconce.position.z = STANDOFF;
scene.add(sconce);

const DOME_R = 0.188, DOME_H = 0.105, RIM_H = 0.026, SEAT = 0.014, BEZEL_R = DOME_R + 0.02;
const TEX = Math.min(mobile ? 3072 : 4096, renderer.capabilities.maxTextureSize);

// The face is painted once (grooves, dust). After that only the label circle is repainted.
function paintLabelInto(g, size, labelCanvas, dustRand) {
  const m = size / 2, px = m / R;
  g.save(); g.beginPath(); g.arc(m, m, LABEL_R * px, 0, 7); g.clip();
  const lw = LABEL_R * px * 2;
  g.drawImage(labelCanvas, m - lw / 2, m - lw / 2, lw, lw);
  g.globalCompositeOperation = 'multiply'; g.fillStyle = 'rgb(205,200,194)'; g.fillRect(0, 0, size, size);
  g.globalCompositeOperation = 'source-over';
  // the cap sits on the paper: soft occlusion hugging the bezel
  const ao = g.createRadialGradient(m, m, BEZEL_R * px * 0.96, m, m, (BEZEL_R + 0.07) * px);
  ao.addColorStop(0, 'rgba(8,5,3,0.62)'); ao.addColorStop(0.3, 'rgba(8,5,3,0.24)'); ao.addColorStop(1, 'rgba(8,5,3,0)');
  g.fillStyle = ao; g.fillRect(0, 0, size, size);
  // the same dust the vinyl carries, on the paper too (seeded, so it does not jump between labels)
  const rnd = mkRand(dustRand);
  for (let i = 0; i < 300; i++) {
    const a = rnd() * 6.283, r = Math.sqrt(rnd()) * LABEL_R * px, s = (0.25 + rnd() * rnd() * 1.5) * size / 2048;
    g.fillStyle = `rgba(214,208,198,${(0.05 + rnd() * 0.22).toFixed(3)})`;
    g.beginPath(); g.arc(m + Math.cos(a) * r, m + Math.sin(a) * r, s, 0, 7); g.fill();
  }
  g.restore();
}
function vinylFace(labelCanvas, size = TEX, seed = 5) {
  const c = document.createElement('canvas'); c.width = c.height = size;
  const g = c.getContext('2d'), m = size / 2, px = m / R;
  g.fillStyle = '#050506'; g.fillRect(0, 0, size, size);
  // the faintest trace of each groove; the shine does the real work
  for (let r = LABEL_R + 0.09; r < R - 0.04; r += 0.0036) {
    if (GAPS.some(gp => Math.abs(r - gp) < 0.012)) continue;
    g.strokeStyle = `rgba(255,255,255,${0.004 + rand() * 0.012})`;
    g.lineWidth = size / 2048; g.beginPath(); g.arc(m, m, r * px, 0, 7); g.stroke();
  }
  // a lived-in record: a little dust and a couple of fibres, nothing you notice until it is missing
  for (let i = 0; i < 2600; i++) {
    const a = rand() * 6.283, r = Math.sqrt(rand()) * R * px, s = (0.25 + rand() * rand() * 1.5) * size / 2048;
    g.fillStyle = `rgba(214,208,198,${(0.05 + rand() * 0.22).toFixed(3)})`;
    g.beginPath(); g.arc(m + Math.cos(a) * r, m + Math.sin(a) * r, s, 0, 7); g.fill();
  }
  g.lineWidth = 0.6 * size / 2048; g.lineCap = 'round';
  for (let i = 0; i < 26; i++) {
    const a = rand() * 6.283, r = (0.36 + rand() * 0.61) * R * px, x = m + Math.cos(a) * r, y = m + Math.sin(a) * r;
    const b = rand() * 6.283, len = (4 + rand() * 16) * size / 2048, bend = (rand() - 0.5) * len;
    g.strokeStyle = `rgba(214,208,198,${(0.06 + rand() * 0.14).toFixed(3)})`;
    g.beginPath(); g.moveTo(x, y);
    g.quadraticCurveTo(x + Math.cos(b) * len / 2 - Math.sin(b) * bend, y + Math.sin(b) * len / 2 + Math.cos(b) * bend, x + Math.cos(b) * len, y + Math.sin(b) * len);
    g.stroke();
  }
  paintLabelInto(g, size, labelCanvas, seed);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = renderer.capabilities.getMaxAnisotropy();
  t.userData.seed = seed;
  return t;
}
// which way the grooves smear a highlight (across the groove = along the radius), and where
function grooveAniso() {
  const N = 1024, d = new Uint8Array(N * N * 4), ss = THREE.MathUtils.smoothstep, e = 0.008;
  for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) {
    const u = (x + .5) / N * 2 - 1, v = (y + .5) / N * 2 - 1, l = Math.hypot(u, v) || 1, r = l * R;
    const i = (y * N + x) * 4;
    d[i] = (u / l * .5 + .5) * 255; d[i + 1] = (v / l * .5 + .5) * 255;
    let k = ss(r, LABEL_R + 0.08, LABEL_R + 0.08 + e) * (1 - ss(r, R - 0.045, R - 0.045 + e));
    for (const gp of GAPS) k *= 0.35 + 0.65 * ss(Math.abs(r - gp), 0.006, 0.006 + e);
    d[i + 2] = k * 255; d[i + 3] = 255;
  }
  const t = new THREE.DataTexture(d, N, N); t.needsUpdate = true; t.magFilter = t.minFilter = THREE.LinearFilter; return t;
}
// gloss: matte paper, mirror-smooth dead wax and gaps, and music that changes loudness band by band
function roughMap() {
  const N = 2048, c = document.createElement('canvas'); c.width = c.height = N;
  const g = c.getContext('2d'), m = N / 2, px = m / R;
  const grey = v => { const b = Math.round(THREE.MathUtils.clamp(v, 0, 1) * 255); return `rgb(${b},${b},${b})`; };
  g.fillStyle = grey(0.2); g.fillRect(0, 0, N, N);
  let wander = 0;
  for (let p = Math.ceil(R * px); p > LABEL_R * px; p -= 1) {
    const r = p / px;
    wander = wander * 0.93 + (rand() - 0.5) * 0.05;
    let v = 0.29 + wander + (rand() - 0.5) * 0.05;
    if (r > R - 0.04 || r < LABEL_R + 0.085) v = 0.13;
    else if (GAPS.some(gp => Math.abs(r - gp) < 0.009)) v = 0.17;
    g.strokeStyle = grey(v); g.lineWidth = 2; g.beginPath(); g.arc(m, m, p, 0, 7); g.stroke();
  }
  g.fillStyle = grey(0.62); g.beginPath(); g.arc(m, m, LABEL_R * px, 0, 7); g.fill();
  const t = new THREE.CanvasTexture(c); t.anisotropy = 8; return t;
}
// relief you can only see in the shine: label step, the pressing ring, the gaps, the raised outer bead
function reliefMap() {
  const N = 2048, d = new Uint8Array(N * N * 4);
  const bump = (r, at, w, amp) => { const x = (r - at) / w; return -2 * x * Math.exp(-x * x) * amp; }; // slope of a gaussian ridge
  for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) {
    const u = (x + .5) / N * 2 - 1, v = (y + .5) / N * 2 - 1, l = Math.hypot(u, v) || 1, r = l * R;
    let s = bump(r, LABEL_R, 0.006, -0.5) + bump(r, 0.345, 0.006, -0.45) + bump(r, R - 0.018, 0.016, 0.5) + bump(r, LABEL_R + 0.05, 0.012, 0.18);
    for (const gp of GAPS) s += bump(r, gp, 0.009, -0.12);
    const nx = -s * u / l, ny = -s * v / l, nl = Math.hypot(nx, ny, 1);
    const i = (y * N + x) * 4;
    d[i] = (nx / nl * .5 + .5) * 255; d[i + 1] = (ny / nl * .5 + .5) * 255; d[i + 2] = (1 / nl * .5 + .5) * 255; d[i + 3] = 255;
  }
  const t = new THREE.DataTexture(d, N, N); t.magFilter = THREE.LinearFilter; t.minFilter = THREE.LinearMipmapLinearFilter;
  t.generateMipmaps = true; t.anisotropy = 8; t.needsUpdate = true; return t;
}

// ---------- the label: a plain house label drawn here. No real label artwork, logos or marks, ever. ----------
const LABEL_N = 1024;
const DEFAULT_LABEL = { color: '#b4432e', top: 'Your record here', bottom: 'Change the record. Change the room.' };
let paperGrain = null;
function grain() {
  if (paperGrain) return paperGrain;
  const n = 256, c = document.createElement('canvas'); c.width = c.height = n;
  const g = c.getContext('2d'), id = g.createImageData(n, n), rnd = mkRand(77);
  for (let i = 0; i < n * n; i++) { const v = 128 + (rnd() - 0.5) * 90; id.data[i * 4] = id.data[i * 4 + 1] = id.data[i * 4 + 2] = v; id.data[i * 4 + 3] = 255; }
  g.putImageData(id, 0, 0);
  return (paperGrain = c);
}
function arcText(g, str, font, size, minSize, radius, mid, dir, track, maxArc) {
  const chars = [...str]; let s = size, widths, total;
  for (;;) {
    g.font = font(s);
    widths = chars.map(ch => g.measureText(ch).width + track * s);
    total = widths.reduce((a, b) => a + b, 0);
    if (total <= maxArc * radius || s <= minSize) break;
    s -= 2;
  }
  const m = LABEL_N / 2;
  let a = mid - dir * total / radius / 2;
  g.textAlign = 'center'; g.textBaseline = 'alphabetic';
  chars.forEach((ch, i) => {
    const ang = a + dir * widths[i] / 2 / radius;
    g.save(); g.translate(m + Math.cos(ang) * radius, m + Math.sin(ang) * radius); g.rotate(ang + dir * Math.PI / 2);
    g.fillText(ch, 0, 0); g.restore();
    a += dir * widths[i] / radius;
  });
}
function houseLabel({ color, top, bottom }) {
  const N = LABEL_N, c = document.createElement('canvas'); c.width = c.height = N;
  const g = c.getContext('2d'), m = N / 2;
  const col = new THREE.Color(color), hsl = {}; col.getHSL(hsl);
  const lum = 0.2126 * col.r + 0.7152 * col.g + 0.0722 * col.b;      // linear, good enough to pick an ink
  const ink = lum < 0.22 ? '#efe4cd' : '#1b1714';
  g.fillStyle = color; g.fillRect(0, 0, N, N);
  // paper: a breath of uneven ink and fibre, then the edge darkens the way old labels do
  g.globalAlpha = 0.16; g.globalCompositeOperation = 'overlay';
  g.imageSmoothingEnabled = true; g.drawImage(grain(), 0, 0, N, N);
  g.globalAlpha = 0.10; g.drawImage(grain(), 0, 0, 256, 256, -40, -60, N * 2.6, N * 2.6);
  g.globalAlpha = 1; g.globalCompositeOperation = 'source-over';
  const edge = g.createRadialGradient(m, m, m * 0.55, m, m, m);
  edge.addColorStop(0, 'rgba(0,0,0,0)'); edge.addColorStop(0.86, 'rgba(20,10,0,0.06)'); edge.addColorStop(1, 'rgba(20,10,0,0.22)');
  g.fillStyle = edge; g.fillRect(0, 0, N, N);
  // printed rules
  g.strokeStyle = ink; g.globalAlpha = 0.9;
  g.lineWidth = 5; g.beginPath(); g.arc(m, m, m * 0.945, 0, 7); g.stroke();
  g.lineWidth = 2; g.beginPath(); g.arc(m, m, m * 0.915, 0, 7); g.stroke();
  g.lineWidth = 2; g.beginPath(); g.arc(m, m, m * 0.475, 0, 7); g.stroke();
  // type: the name over the top, the title under, small print left and right
  g.fillStyle = ink;
  const T = (top || '').trim().toUpperCase().slice(0, 40), B = (bottom || '').trim().slice(0, 48);
  if (T) arcText(g, T, s => `600 ${s}px "Inter Tight", "Helvetica Neue", Arial, sans-serif`, 98, 34, m * 0.63, -Math.PI / 2, 1, 0.06, 2.5);
  if (B) arcText(g, B, s => `italic 400 ${s}px "Instrument Serif", Georgia, serif`, 84, 34, m * 0.80, Math.PI / 2, -1, 0.01, 2.3);
  g.globalAlpha = 0.85;
  g.font = '500 25px "JetBrains Mono", ui-monospace, Menlo, monospace'; g.textAlign = 'center'; g.textBaseline = 'middle';
  const side = (x, a, b) => { g.fillText(a, x, m - 17); g.fillText(b, x, m + 17); };
  side(m - m * 0.70, 'SIDE', 'ONE'); side(m + m * 0.70, 'STEREO', '33 1/3');
  g.globalAlpha = 1;
  // ring wear: years in a sleeve leave a paler circle
  g.strokeStyle = 'rgba(255,250,240,0.07)'; g.lineWidth = 9; g.beginPath(); g.arc(m, m, m * 0.69, 0.4, 5.2); g.stroke();
  g.strokeStyle = 'rgba(255,250,240,0.05)'; g.lineWidth = 4; g.beginPath(); g.arc(m, m, m * 0.87, 2.2, 6.0); g.stroke();
  return c;
}
function photoLabel(img, zoom = 1) {       // the visitor's own photo. Drawn here, never sent anywhere.
  const N = LABEL_N, c = document.createElement('canvas'); c.width = c.height = N;
  const g = c.getContext('2d');
  const w = img.naturalWidth || img.width, h = img.naturalHeight || img.height, s = Math.min(w, h) / zoom;
  g.fillStyle = '#111'; g.fillRect(0, 0, N, N);
  g.imageSmoothingQuality = 'high';
  g.drawImage(img, (w - s) / 2, (h - s) / 2, s, s, 0, 0, N, N);
  return c;
}

// ---------- chrome dome cap on a rolled bezel ----------
// A true mirror: every frame a probe at the cap photographs the room, the label and the vinyl
// around it, and the chrome shows exactly that. No stand-in highlights.
const probeRT = new THREE.WebGLCubeRenderTarget(mobile ? 384 : 512, { type: THREE.HalfFloatType, generateMipmaps: true, minFilter: THREE.LinearMipmapLinearFilter });
const probe = new THREE.CubeCamera(0.02, 100, probeRT);
probe.layers.enable(ROOM_LAYER);
scene.add(probe);
const chrome = new THREE.ShaderMaterial({
  uniforms: { env: { value: probeRT.texture }, tint: { value: new THREE.Color(0.66, 0.665, 0.675) }, soft: { value: 0.6 } },
  vertexShader: `
    varying vec3 vPos; varying vec3 vNrm;
    void main(){
      vec4 w = modelMatrix * vec4(position, 1.0);
      vPos = w.xyz; vNrm = mat3(modelMatrix) * normal;
      gl_Position = projectionMatrix * viewMatrix * w;
    }`,
  fragmentShader: `
    uniform samplerCube env; uniform vec3 tint; uniform float soft;
    varying vec3 vPos; varying vec3 vNrm;
    void main(){
      vec3 V = normalize(vPos - cameraPosition);
      vec3 N = normalize(vNrm);
      if (dot(N, V) > 0.0) N = -N;
      vec3 Rf = reflect(V, N);
      vec3 c = textureLod(env, Rf, soft).rgb;
      float f = pow(1.0 - clamp(dot(N, -V), 0.0, 1.0), 5.0);
      gl_FragColor = vec4(c * mix(tint, vec3(1.0), f), 1.0);
    }`,
});
const sphR = (DOME_R * DOME_R + DOME_H * DOME_H) / (2 * DOME_H);
const capParts = [];
let faceMat, discGeo = {};
function buildDisc(group, mat) {
  const face = new THREE.Mesh(discGeo.face, mat);
  face.position.z = THICK / 2; face.castShadow = true;
  const edge = new THREE.Mesh(discGeo.edge, discGeo.edgeMat);
  edge.rotation.x = Math.PI / 2; edge.castShadow = true;
  const back = new THREE.Mesh(discGeo.back, discGeo.backMat);
  back.rotation.y = Math.PI; back.position.z = -THICK / 2; back.castShadow = true;
  const dome = new THREE.Mesh(discGeo.dome, chrome);
  dome.rotation.x = Math.PI / 2;
  dome.position.z = THICK / 2 + SEAT - (sphR - DOME_H);
  dome.castShadow = true;
  const rim = new THREE.Mesh(discGeo.rim, chrome);
  rim.rotation.x = Math.PI / 2; rim.position.z = THICK / 2; rim.castShadow = true;
  const seam = new THREE.Mesh(discGeo.seam, discGeo.seamMat);
  seam.position.z = THICK / 2 + SEAT;
  group.add(face, edge, back, dome, rim, seam);
  capParts.push(dome, rim, seam);
}
const probeAt = new THREE.Vector3();
function shootProbe() {
  probeAt.set(0, 0, THICK / 2 + SEAT + DOME_H * 0.55); sconce.localToWorld(probeAt);
  probe.position.copy(probeAt);
  for (const p of capParts) p.visible = false;
  probe.update(renderer, scene);
  for (const p of capParts) p.visible = true;
}

// ---------- film: MSAA, then a breath of grain so the wall gradient never bands ----------
const rt = new THREE.WebGLRenderTarget(1, 1, { type: THREE.HalfFloatType, samples: 4 });
const composer = new EffectComposer(renderer, rt);
composer.addPass(new RenderPass(scene, camera));
composer.addPass(new OutputPass());
const film = new ShaderPass({
  uniforms: { tDiffuse: { value: null }, t: { value: 0 }, aspect: { value: 1 } },
  vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }',
  fragmentShader: `
    uniform sampler2D tDiffuse; uniform float t, aspect; varying vec2 vUv;
    float hash(vec2 p){ vec3 q = fract(vec3(p.xyx) * 0.1031); q += dot(q, q.yzx + 33.33); return fract((q.x + q.y) * q.z); }
    void main(){
      vec3 c = texture2D(tDiffuse, vUv).rgb;
      vec2 p = (vUv - 0.5) * vec2(min(aspect, 1.0), min(1.0 / aspect, 1.0)) * 2.0;
      c *= 1.0 - 0.2 * smoothstep(0.55, 1.35, length(p));
      float n = hash(gl_FragCoord.xy + fract(t) * 291.0) + hash(gl_FragCoord.yx + fract(t * 1.37) * 173.0) - 1.0;
      c += n * 0.016;
      gl_FragColor = vec4(c, 1.0);
    }`,
});
composer.addPass(film);

// ---------- framing: where the record sits in each host, and the hero pull-back ----------
let active = null, pull = 0, W = 0, H = 0, gridN = 0;
const ease = x => x * x * (3 - 2 * x);
const mix = (a, b, t) => a + (b - a) * t;
function frameFor(name, w, h, p) {
  if (gridN) return { d: Math.min(w, h) / (gridN * 1.36), cx: 0.5, cy: 0.5 };
  if (name === 'hero') {
    const wide = w >= 900 && w > h;
    const a = wide ? { d: Math.min(0.86 * h, 0.5 * w), cx: 0.70, cy: 0.5 } : { d: Math.min(0.98 * w, 0.56 * h), cx: 0.5, cy: 0.33 };
    const b = wide ? { d: 0.40 * h, cx: 0.5, cy: 0.45 } : { d: 0.52 * w, cx: 0.5, cy: 0.40 };
    const t = ease(p);
    return { d: mix(a.d, b.d, t), cx: mix(a.cx, b.cx, t), cy: mix(a.cy, b.cy, t) };
  }
  return { d: 0.8 * Math.min(w, h), cx: 0.5, cy: 0.5 };
}
function layout(force) {
  if (!active) return;
  const w = Math.max(2, active.clientWidth), h = Math.max(2, active.clientHeight);
  if (force || w !== W || h !== H) {
    W = w; H = h;
    renderer.setPixelRatio(PR);
    renderer.setSize(w, h, false);
    composer.setPixelRatio(PR);
    composer.setSize(w, h);
    film.uniforms.aspect.value = w / h;
    camera.aspect = w / h;
  }
  const f = frameFor(active.dataset.sconce, w, h, pull);
  const tanV = Math.tan(THREE.MathUtils.degToRad(camera.fov) / 2);
  camera.position.set(0, 0, (R * 2 * h / f.d) / 2 / tanV);
  camera.lookAt(0, 0, 0);
  camera.setViewOffset(w, h, (0.5 - f.cx) * w, (0.5 - f.cy) * h, w, h);
  camera.updateProjectionMatrix();
}

// ---------- interaction: drag to tilt, it springs back ----------
const target = new THREE.Vector2();
const tilt = new THREE.Vector2();
const vel = new THREE.Vector2();
const gyro = new THREE.Vector2();
const goal = new THREE.Vector2();
let dragging = false, start = null, touch = false, reach = 0, gyroAsked = false;
const MAX = 0.62; // about 35 degrees

function onDown(e) {
  dragging = true; reach = 0;
  touch = e.pointerType === 'touch';
  start = { x: e.clientX, y: e.clientY };
  try { canvas.setPointerCapture(e.pointerId); } catch (_) {}
}
function onMove(e) {
  if (!dragging) return;
  const s = 2.4 / Math.min(W, H, 900);
  const dx = e.clientX - start.x, dy = e.clientY - start.y;
  reach = Math.max(reach, Math.abs(dx));
  // on a touch screen a vertical swipe belongs to the page (touch-action: pan-y), so only sideways tilts
  target.set(THREE.MathUtils.clamp(dx * s, -MAX, MAX), touch ? 0 : THREE.MathUtils.clamp(dy * s, -MAX, MAX));
  if (reach > 12) root.classList.add('sconce-touched');
}
function onUp(e) {
  if (!dragging) return;
  dragging = false; target.set(0, 0);
  // iOS shares the gyroscope only if asked. Ask after a deliberate tilt, never on first touch.
  if (e && e.type === 'pointerup' && reach > 40 && !gyroAsked && typeof DeviceOrientationEvent !== 'undefined' && DeviceOrientationEvent.requestPermission) {
    gyroAsked = true;
    try { DeviceOrientationEvent.requestPermission().catch(() => {}); } catch (_) {}
  }
}
canvas.addEventListener('pointerdown', onDown);
canvas.addEventListener('pointermove', onMove);
canvas.addEventListener('pointerup', onUp);
canvas.addEventListener('pointercancel', onUp);
addEventListener('deviceorientation', e => {
  if (e.gamma == null || calm) return;
  gyro.set(THREE.MathUtils.clamp(e.gamma / 45, -1, 1) * 0.18, THREE.MathUtils.clamp((e.beta - 50) / 45, -1, 1) * 0.12);
});

// ---------- loop ----------
const clock = new THREE.Clock();
let running = false, frames = 0, slow = 0, steps = 0;
function frame() {
  const raw = clock.getDelta(), dt = Math.min(raw, 1 / 30), t = clock.elapsedTime;
  if (active === hosts.hero && track && track.classList.contains('pull')) {
    const r = track.getBoundingClientRect(), span = r.height - active.offsetHeight;
    const top = parseFloat(getComputedStyle(active).top) || 0;
    const p = span > 0 ? THREE.MathUtils.clamp((top - r.top) / span, 0, 1) : 0;
    if (p !== pull) { pull = p; track.style.setProperty('--p', p.toFixed(3)); track.classList.toggle('past', p > 0.42); }
  }
  layout(false);
  goal.copy(target);
  if (!dragging && !gridN) { goal.add(gyro); if (!calm) goal.x += Math.sin(t * 0.6) * 0.02; }
  const k = dragging ? 140 : 38, damp = dragging ? 22 : 5.5; // snappy while held, a little wobble on release
  vel.x += ((goal.x - tilt.x) * k - vel.x * damp) * dt;
  vel.y += ((goal.y - tilt.y) * k - vel.y * damp) * dt;
  tilt.addScaledVector(vel, dt);

  sconce.rotation.set(tilt.y, tilt.x, 0);
  // lift it off the wall as it tilts, so the far edge never sinks into the drywall
  const ang = Math.min(Math.hypot(tilt.x, tilt.y), 1.2);
  sconce.position.z = Math.max(STANDOFF, R * Math.sin(ang) + 0.08);
  // the edge that lifts off the wall lets more light out
  halo.position.set(sconce.position.x - tilt.x * 0.25, sconce.position.y + tilt.y * 0.25, 0.002);
  halo.material.opacity = HALO + Math.min(0.1, (Math.abs(tilt.x) + Math.abs(tilt.y)) * 0.15);
  film.uniforms.t.value = t;
  renderer.shadowMap.needsUpdate = true;   // shadows once per frame, for the page camera
  composer.render();
  shootProbe();                            // the mirror reuses them; it shows on the next frame

  // a phone that cannot hold the frame rate gets fewer pixels, not a slideshow
  if (!MAXQ && steps < 3 && ++frames > 20) {
    slow += raw;
    if (frames === 80) {
      if (slow / 60 > 0.026 && PR > 1.25) { PR = Math.max(1.25, PR * 0.75); steps++; layout(true); }
      else steps = 3;
      frames = 0; slow = 0;
    }
  }
}
function run(on) {
  if (on === running) return;
  running = on; clock.getDelta();
  renderer.setAnimationLoop(on ? frame : null);
}

// ---------- hosts: the one canvas goes wherever the visitor is looking ----------
const seen = new Map();
function attach(host) {
  if (host === active) return;
  if (active) { freeze(active); active.classList.remove('live', 'snap'); }
  active = host;
  if (!host) { run(false); return; }
  dragging = false; target.set(0, 0);
  host.appendChild(canvas);
  layout(true);
  frame(); frame();                        // second pass so the mirror is not a frame behind when it appears
  if (host.dataset.was) host.classList.add('snap');
  host.dataset.was = '1';
  requestAnimationFrame(() => host.classList.add('live'));
  run(!document.hidden);
}
function freeze(host) {                    // leave a still of what they made behind, so the frame is never stale
  if (host !== hosts.pick || !labelState.custom) return;
  const img = host.querySelector('img'); if (!img) return;
  try {
    composer.render();
    const url = canvas.toDataURL('image/jpeg', 0.86);
    host.querySelectorAll('source').forEach(s => s.remove());
    img.removeAttribute('srcset'); img.src = url;
  } catch (_) {}
}
function choose() {
  const v = k => (hosts[k] ? seen.get(hosts[k]) || 0 : 0);
  if (gridN) return;
  if (v('pick') >= 0.35) attach(hosts.pick);
  else if (v('hero') > 0) attach(hosts.hero);
  else if (v('pick') > 0) attach(hosts.pick);
  else attach(null);
}
document.addEventListener('visibilitychange', () => run(!!active && !document.hidden));

// ---------- label state and the picker ----------
const labelState = { ...DEFAULT_LABEL, artist: '', title: '', photo: null, zoom: 1, custom: false, house: false };
// Reference label until the visitor makes their own: a photo of a real Led Zeppelin IV side-two pressing (Austin 2026-11-12).
let refLabel = null;
const refReady = new Promise(res => { const im = new Image(); im.onload = () => { refLabel = im; res(); }; im.onerror = () => res(); im.src = 'img/label-zep4.jpg'; });
let faceTex = null, repaintTimer = 0;
function currentLabel() {
  if (labelState.photo) return photoLabel(labelState.photo, labelState.zoom);
  if (!labelState.house && refLabel) return photoLabel(refLabel, 1.036);
  const typed = labelState.artist || labelState.title;
  return houseLabel({
    color: labelState.color,
    top: typed ? (labelState.artist || labelState.title) : DEFAULT_LABEL.top,
    bottom: typed ? (labelState.artist ? labelState.title : '') : DEFAULT_LABEL.bottom,
  });
}
function repaint() {
  if (!faceTex) return;
  paintLabelInto(faceTex.image.getContext('2d'), faceTex.image.width, currentLabel(), faceTex.userData.seed);
  faceTex.needsUpdate = true;
}
function setLabel(patch, now) {
  Object.assign(labelState, patch); labelState.custom = true;
  if (!('house' in patch)) labelState.house = true;
  clearTimeout(repaintTimer);
  if (now) repaint(); else repaintTimer = setTimeout(repaint, 180);
}
function wirePicker() {
  const box = document.querySelector('[data-pick]'); if (!box) return;
  const artist = box.querySelector('[data-pick-artist]'), title = box.querySelector('[data-pick-title]');
  const file = box.querySelector('[data-pick-file]'), zoom = box.querySelector('[data-pick-zoom]');
  const photoRow = box.querySelector('[data-pick-photo-row]'), clear = box.querySelector('[data-pick-clear]');
  const chips = [...box.querySelectorAll('[data-pick-color]')];
  const drawn = () => { labelState.photo = null; if (photoRow) photoRow.hidden = true; if (file) file.value = ''; };
  const typed = () => { drawn(); setLabel({ artist: artist ? artist.value : '', title: title ? title.value : '' }); };
  if (artist) artist.addEventListener('input', typed);
  if (title) title.addEventListener('input', typed);
  chips.forEach(ch => ch.addEventListener('click', () => {
    chips.forEach(o => o.setAttribute('aria-pressed', o === ch ? 'true' : 'false'));
    drawn(); setLabel({ color: ch.dataset.pickColor }, true);
  }));
  if (file) file.addEventListener('change', () => {
    const f = file.files && file.files[0]; if (!f || !/^image\//.test(f.type)) return;
    const url = URL.createObjectURL(f), img = new Image();
    img.onload = () => { URL.revokeObjectURL(url); if (zoom) zoom.value = 1; if (photoRow) photoRow.hidden = false; setLabel({ photo: img, zoom: 1 }, true); };
    img.onerror = () => URL.revokeObjectURL(url);
    img.src = url;
  });
  if (zoom) zoom.addEventListener('input', () => setLabel({ zoom: parseFloat(zoom.value) || 1 }));
  if (clear) clear.addEventListener('click', () => { drawn(); if (artist) artist.value = ''; if (title) title.value = ''; setLabel({ artist: '', title: '', color: DEFAULT_LABEL.color, house: false }, true); });
  box.classList.add('ready');
}

// ---------- a wall of them. Used only to render the still on the page (see README: capture). ----------
const WALL = [
  ['#27406b', 'Blue hour'], ['#e6dcc4', 'Sunday morning'], ['#2d6f6a', 'First dance'],
  ['#c96f2e', 'The one from the flea market'], ['#b4432e', ''], ['#1f1c1a', 'Play it loud'],
  ['#7a3550', 'Last call'], ['#d8a53a', 'Side two'], ['#4a5d3a', 'The one Dad played'],
];
function grid(n) {
  gridN = n; const gap = R * 2.72, off = (n - 1) / 2; let i = 0;
  key.angle = Math.PI / 3.2; key.intensity = 60; key.position.set(0, 13, 9); key.shadow.mapSize.set(4096, 4096);
  for (let row = 0; row < n; row++) for (let colm = 0; colm < n; colm++, i++) {
    const x = (colm - off) * gap, y = (off - row) * gap;
    if (row === (n - 1) / 2 && colm === (n - 1) / 2) continue;         // the centre one is the live sconce
    const w = WALL[i % WALL.length];
    const g = new THREE.Group(); g.position.set(x, y, STANDOFF);
    const mat = faceMat.clone();
    mat.map = vinylFace(houseLabel({ color: w[0], top: w[1], bottom: 'Side one' }), 2048, 11 + i);
    buildDisc(g, mat); scene.add(g);
    const h = mkHalo(); h.position.set(x, y, 0.002); scene.add(h);
    const l = mkLed(); l.position.set(x, y, STANDOFF * 0.5); scene.add(l);
  }
  layout(true);
}

// ---------- start ----------
async function boot() {
  if (!hosts.hero && !hosts.pick) return;
  await tick();
  faceMat = new THREE.MeshPhysicalMaterial({
    color: '#ffffff', roughness: 1, roughnessMap: roughMap(), metalness: 0,
    anisotropy: 0.85,
    specularColor: new THREE.Color(1.0, 0.9, 0.8),   // black vinyl throws window light back warm-neutral, not navy
    envMapIntensity: 0.75,
  });
  await tick();
  faceMat.anisotropyMap = grooveAniso();
  await tick();
  faceMat.normalMap = reliefMap(); faceMat.normalScale = new THREE.Vector2(1, 1);
  await tick();
  discGeo = {
    face: new THREE.CircleGeometry(R, 512),
    edge: new THREE.CylinderGeometry(R, R, THICK, 512, 1, true),
    edgeMat: new THREE.MeshPhysicalMaterial({ color: '#070708', roughness: 0.25 }),
    back: new THREE.CircleGeometry(R, 256),
    backMat: new THREE.MeshStandardMaterial({ color: '#0b0b0c', roughness: 0.4 }),
    dome: new THREE.SphereGeometry(sphR, 256, 96, 0, Math.PI * 2, 0, Math.asin(DOME_R / sphR)),
    seam: new THREE.RingGeometry(DOME_R - 0.004, DOME_R + 0.006, 256),
    seamMat: new THREE.MeshBasicMaterial({ color: 0x020202 }),
  };
  const prof = [new THREE.Vector2(BEZEL_R, 0), new THREE.Vector2(BEZEL_R, RIM_H - 0.01)];
  for (let i = 1; i <= 10; i++) { const a = i / 10 * Math.PI / 2; prof.push(new THREE.Vector2(BEZEL_R - 0.01 + 0.01 * Math.cos(a), RIM_H - 0.01 + 0.01 * Math.sin(a))); }
  prof.push(new THREE.Vector2(DOME_R + 0.007, RIM_H), new THREE.Vector2(DOME_R + 0.005, RIM_H - 0.002), new THREE.Vector2(DOME_R + 0.005, SEAT));
  discGeo.rim = new THREE.LatheGeometry(prof, 256);
  buildDisc(sconce, faceMat);
  await tick();
  // the label is set in the page fonts, so wait for them (briefly) before drawing it
  try {
    await Promise.race([
      Promise.all(['600 80px "Inter Tight"', 'italic 400 80px "Instrument Serif"', '500 25px "JetBrains Mono"'].map(f => document.fonts.load(f))),
      new Promise(r => setTimeout(r, 2500)),
    ]);
  } catch (_) {}
  await Promise.race([refReady, new Promise(r => setTimeout(r, 2500))]);
  faceTex = vinylFace(currentLabel());
  faceMat.map = faceTex; faceMat.needsUpdate = true;
  await tick();
  await hdrReady;

  // the pull-back adds scroll length, so it is only switched on if nobody has started reading yet
  if (track && !calm && scrollY < 60) track.classList.add('pull');
  wirePicker();
  root.classList.add('has3d');
  window.SpindleSconce = { setLabel, grid, state: labelState, renderer };
  const io = new IntersectionObserver(es => { es.forEach(e => seen.set(e.target, e.isIntersecting ? e.intersectionRatio : 0)); choose(); }, { threshold: [0, 0.15, 0.35, 0.6, 0.9] });
  Object.values(hosts).forEach(h => io.observe(h));
  addEventListener('resize', () => layout(false));
  renderer.domElement.addEventListener('webglcontextlost', e => { e.preventDefault(); run(false); if (active) active.classList.remove('live', 'snap'); root.classList.add('no3d'); root.classList.remove('has3d'); });
}
boot().catch(err => { root.classList.add('no3d'); if (window.console) console.warn('[sconce3d] still image stays:', err); });
