"""
LUMEN — LUT Color Studio v0.6
本地运行：streamlit run app.py
Streamlit Cloud：直接部署即可
"""

import streamlit as st
import streamlit.components.v1 as components
import numpy as np
from PIL import Image
import io, os, glob, json

st.set_page_config(
    page_title="LUMEN",
    page_icon="🎞",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; }
html, body, [class*="css"], .stApp {
    font-family: 'DM Mono', monospace !important;
    background-color: #111210 !important;
    color: #b8b4ac !important;
}
#MainMenu, footer, header,
[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stSidebarCollapseButton"], [data-testid="collapsedControl"],
section[data-testid="stSidebar"], [data-testid="stStatusWidget"] { display: none !important; }
.stDeployButton { display: none !important; }
.main .block-container { padding: 0 !important; max-width: 100% !important; }

.g-topbar {
    padding: 1.2rem 2rem 0.9rem;
    border-bottom: 1px solid #1c1c1a;
    display: flex; align-items: baseline; gap: 1.4rem;
}
.g-logo { font-size: 0.85rem; font-weight: 500; letter-spacing: 0.55em; color: #e2ddd5; text-transform: uppercase; }
.g-accent { color: #a87d45; }
.g-sub { font-size: 0.52rem; letter-spacing: 0.3em; color: #2e2e2c; text-transform: uppercase; }

.stRadio { margin: 0 !important; }
.stRadio label { display: none !important; }
.stRadio div[role="radiogroup"] { display: flex !important; gap: 0 !important; }
.stRadio div[role="radiogroup"] label {
    display: flex !important; align-items: center !important;
    font-family: 'DM Mono', monospace !important; font-size: 0.55rem !important;
    letter-spacing: 0.2em !important; text-transform: uppercase !important;
    color: #444440 !important; padding: 0.3rem 0.9rem !important;
    border: 1px solid #1e1e1c !important; border-right: none !important;
    cursor: pointer !important; white-space: nowrap !important;
    transition: all 0.15s !important;
}
.stRadio div[role="radiogroup"] label:last-child { border-right: 1px solid #1e1e1c !important; }
.stRadio div[role="radiogroup"] label:has(input:checked) { color: #a87d45 !important; border-color: #a87d45 !important; }
.stRadio input[type="radio"] { display: none !important; }

.g-ctrl-label { font-size: 0.5rem; letter-spacing: 0.28em; color: #2e2e2c; text-transform: uppercase; white-space: nowrap; padding-top: 6px; }
.g-sep-line { width: 1px; height: 36px; background: #1c1c1a; margin: 0 0.3rem; align-self: center; }

.stFileUploader { margin: 0 !important; padding: 0 !important; }
.stFileUploader label { display: none !important; }
.stFileUploader section {
    background: transparent !important; border: 1px solid #222220 !important;
    border-radius: 2px !important; padding: 0 0.8rem !important;
    min-height: 36px !important; display: flex !important; align-items: center !important;
}
.stFileUploader section:hover { border-color: #a87d45 !important; }
.stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] { padding: 0 !important; }
.stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] div span {
    font-family: 'DM Mono', monospace !important; font-size: 0.62rem !important; color: #444440 !important;
}
.stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] div small,
.stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] div + div { display: none !important; }
.stFileUploader [data-testid="stFileUploaderFile"] { background: transparent !important; padding: 0 !important; border: none !important; }
.stFileUploader [data-testid="stFileUploaderFile"] small { display: none !important; }
[data-testid="stFileUploaderFileName"] { font-family: 'DM Mono', monospace !important; font-size: 0.65rem !important; color: #a87d45 !important; }

.stSelectbox { margin: 0 !important; }
.stSelectbox label { display: none !important; }
.stSelectbox [data-baseweb="select"] > div:first-child {
    background: transparent !important; border: 1px solid #222220 !important;
    border-radius: 2px !important; font-family: 'DM Mono', monospace !important;
    font-size: 0.7rem !important; color: #c0bcb4 !important; min-height: 36px !important;
}
.stSelectbox [data-baseweb="select"] > div:first-child:hover { border-color: #a87d45 !important; }
[data-baseweb="popover"] { background: #181816 !important; border: 1px solid #2a2a28 !important; }
[data-baseweb="menu"] { background: #181816 !important; }
[role="option"] { font-family: 'DM Mono', monospace !important; font-size: 0.68rem !important; background: #181816 !important; color: #888480 !important; }
[role="option"]:hover, [aria-selected="true"] { background: #222220 !important; color: #a87d45 !important; }

.stDownloadButton button {
    font-family: 'DM Mono', monospace !important; font-size: 0.58rem !important;
    letter-spacing: 0.18em !important; text-transform: uppercase !important;
    background: transparent !important; border: 1px solid #a87d45 !important;
    color: #a87d45 !important; border-radius: 2px !important;
    padding: 0 1rem !important; min-height: 36px !important; white-space: nowrap !important;
}
.stDownloadButton button:hover { background: #a87d45 !important; color: #111210 !important; }

.g-panel-label { font-size: 0.5rem; letter-spacing: 0.3em; color: #252523; text-transform: uppercase; margin-bottom: 0.5rem; }
.g-panel-label-on { color: #a87d45; }
.g-empty { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 60vh; gap: 1.2rem; color: #1e1e1c; }
.g-empty-frame { width: 48px; height: 34px; border: 1px solid #1e1e1c; }
.g-empty-txt { font-size: 0.55rem; letter-spacing: 0.35em; text-transform: uppercase; }
.g-infobar { font-size: 0.5rem; letter-spacing: 0.18em; color: #222220; padding: 0.7rem 2rem; border-top: 1px solid #1a1a18; margin-top: 1rem; display: flex; gap: 2rem; flex-wrap: wrap; }
.g-infobar b { color: #333330; font-weight: 400; }
.stImage img { width: 100% !important; height: auto !important; display: block; }
[data-testid="stHorizontalBlock"] { gap: 2px !important; }
iframe { border: none !important; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════
# 色彩处理
# ══════════════════════════════════════

@st.cache_data
def parse_cube(path):
    size, ltype, data = None, None, []
    with open(path, "r", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"): continue
            if line.startswith("LUT_3D_SIZE"): size, ltype = int(line.split()[-1]), "3D"; continue
            if line.startswith("LUT_1D_SIZE"): size, ltype = int(line.split()[-1]), "1D"; continue
            if line.startswith(("TITLE","DOMAIN_MIN","DOMAIN_MAX")): continue
            p = line.split()
            if len(p) == 3:
                try: data.append([float(x) for x in p])
                except: continue
    arr = np.array(data, dtype=np.float32)
    if ltype == "3D":
        arr = arr.reshape(size, size, size, 3).transpose(2,1,0,3)
    else:
        arr = arr.reshape(size, 3)
    return arr, size, ltype

def srgb_to_linear(img):
    img = img.astype(np.float32)/255.0
    return np.where(img<=0.04045, img/12.92, ((img+0.055)/1.055)**2.4)

def linear_to_srgb(img):
    img = np.clip(img,0,1)
    return np.clip(np.where(img<=0.0031308, img*12.92, 1.055*(img**(1/2.4))-0.055),0,1)

def apply_3d_lut(img, lut, size):
    s=size-1; c=img*s
    lo=np.floor(c).astype(np.int32); hi=np.minimum(lo+1,size-1); f=c-lo
    r0,g0,b0=lo[...,0],lo[...,1],lo[...,2]
    r1,g1,b1=hi[...,0],hi[...,1],hi[...,2]
    fr,fg,fb=f[...,0:1],f[...,1:2],f[...,2:3]
    c00=lut[r0,g0,b0]*(1-fr)+lut[r1,g0,b0]*fr
    c01=lut[r0,g0,b1]*(1-fr)+lut[r1,g0,b1]*fr
    c10=lut[r0,g1,b0]*(1-fr)+lut[r1,g1,b0]*fr
    c11=lut[r0,g1,b1]*(1-fr)+lut[r1,g1,b1]*fr
    return ((c00*(1-fg)+c10*fg)*(1-fb)+(c01*(1-fg)+c11*fg)*fb).astype(np.float32)

@st.cache_data
def process_image(img_bytes, lut_path):
    pil=Image.open(io.BytesIO(img_bytes)).convert("RGB")
    if max(pil.size)>2800: pil.thumbnail((2800,2800),Image.LANCZOS)
    arr=np.array(pil,dtype=np.float32)
    lin=srgb_to_linear(arr)
    lut,size,ltype=parse_cube(lut_path)
    out=apply_3d_lut(lin,lut,size)
    return (linear_to_srgb(out)*255).astype(np.uint8)

def to_jpeg(arr,q=93):
    buf=io.BytesIO(); Image.fromarray(arr).save(buf,"JPEG",quality=q); return buf.getvalue()

def scan_luts(d):
    paths=sorted(glob.glob(os.path.join(d,"*.cube"))+glob.glob(os.path.join(d,"*.CUBE")))
    return {os.path.splitext(os.path.basename(p))[0]: p for p in paths}

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LUTS_DIR   = os.path.join(SCRIPT_DIR, "assets", "luts")
os.makedirs(LUTS_DIR, exist_ok=True)

# 检测运行环境，生成正确的静态文件 URL
IS_CLOUD = os.path.exists('/mount/src')
if IS_CLOUD:
    # Cloud: 用 GitHub Raw 直接提供 LUT 文件，稳定可靠
    LUT_STATIC_BASE = "https://raw.githubusercontent.com/cjrkljfsjiv-netizen/lut-app/main/static/luts"
else:
    LUT_STATIC_BASE = "http://localhost:8501/app/static/luts" 


# ══════════════════════════════════════
# 相机组件
# LUT 通过 Streamlit 静态文件服务按需加载
# 本地：/app/static/luts/xxx.cube
# ══════════════════════════════════════

def camera_component(lut_names: list, lut_base_url: str = "http://localhost:8501/app/static/luts", height: int = 820):
    lut_names_js = json.dumps(lut_names)

    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; -webkit-tap-highlight-color:transparent; }}

  body {{
    background:#000;
    font-family: -apple-system, 'SF Pro Text', sans-serif;
    height: 100svh;
    overflow: hidden;
    user-select: none;
    color: #fff;
  }}

  /* ── 全屏取景器 ── */
  #viewer {{
    position: fixed;
    inset: 0;
    background: #000;
  }}
  canvas {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }}

  /* ── 闪光 ── */
  #flash {{
    position: fixed; inset: 0;
    background: #fff; opacity: 0;
    pointer-events: none;
    transition: opacity 0.04s;
    z-index: 100;
  }}
  #flash.go {{ opacity: 0.8; }}

  /* ── 顶部 HUD ── */
  #hud-top {{
    position: fixed;
    top: 0; left: 0; right: 0;
    padding: env(safe-area-inset-top, 12px) 20px 12px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    z-index: 10;
    background: linear-gradient(to bottom, rgba(0,0,0,0.5), transparent);
  }}
  .hud-pill {{
    background: rgba(0,0,0,0.45);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border-radius: 20px;
    padding: 5px 12px;
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 0.02em;
    color: rgba(255,255,255,0.85);
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .hud-pill.live {{ color: #f0c040; }}
  .hud-dot {{
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #f0c040;
    animation: pulse 1.5s ease-in-out infinite;
  }}
  @keyframes pulse {{ 0%,100% {{ opacity:1; }} 50% {{ opacity:0.3; }} }}

  /* 曝光指示 */
  #ev-hud {{
    font-size: 13px;
    font-weight: 600;
    color: #f0c040;
    opacity: 0;
    transition: opacity 0.3s;
    min-width: 60px;
    text-align: center;
  }}
  #ev-hud.show {{ opacity: 1; }}

  /* 当前 LUT 名 */
  #lut-hud {{
    font-size: 11px;
    font-weight: 500;
    color: rgba(255,255,255,0.7);
    letter-spacing: 0.05em;
    text-transform: uppercase;
    max-width: 140px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }}

  /* ── 对焦框 ── */
  #focus-box {{
    position: fixed;
    width: 72px; height: 72px;
    border: 1.5px solid #f0c040;
    border-radius: 4px;
    opacity: 0;
    pointer-events: none;
    z-index: 10;
    transition: opacity 0.2s;
    transform: translate(-50%, -50%);
  }}
  #focus-box::before, #focus-box::after {{
    content: '';
    position: absolute;
    background: #f0c040;
  }}
  #focus-box::before {{ top: -6px; left: 50%; width: 1px; height: 12px; transform: translateX(-50%); }}
  #focus-box::after  {{ left: -6px; top: 50%; height: 1px; width: 12px; transform: translateY(-50%); }}
  #focus-box.show {{ opacity: 1; }}

  /* ── 曝光滑条（点击后弹出） ── */
  #ev-bar {{
    position: fixed;
    right: 16px;
    top: 50%;
    transform: translateY(-50%);
    z-index: 10;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.25s;
  }}
  #ev-bar.show {{ opacity: 1; pointer-events: all; }}
  .ev-icon {{ font-size: 16px; }}
  #ev-slider {{
    writing-mode: vertical-lr;
    direction: rtl;
    -webkit-appearance: none;
    appearance: none;
    width: 4px;
    height: 140px;
    background: rgba(255,255,255,0.3);
    border-radius: 2px;
    outline: none;
  }}
  #ev-slider::-webkit-slider-thumb {{
    -webkit-appearance: none;
    width: 20px; height: 20px;
    border-radius: 50%;
    background: #f0c040;
    cursor: pointer;
    border: 2px solid #fff;
    box-shadow: 0 2px 6px rgba(0,0,0,0.4);
  }}

  /* ── LUT 选择条 ── */
  #lut-strip-wrap {{
    position: fixed;
    bottom: calc(140px + env(safe-area-inset-bottom, 0px));
    left: 0; right: 0;
    z-index: 10;
    padding: 0 16px;
    opacity: 1;
    transition: opacity 0.2s;
  }}
  #lut-strip {{
    display: flex;
    gap: 8px;
    overflow-x: auto;
    padding: 8px 0;
    scrollbar-width: none;
    -webkit-overflow-scrolling: touch;
  }}
  #lut-strip::-webkit-scrollbar {{ display: none; }}

  .lut-pill {{
    flex-shrink: 0;
    padding: 5px 14px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 0.03em;
    color: rgba(255,255,255,0.55);
    background: rgba(0,0,0,0.35);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.12);
    cursor: pointer;
    transition: all 0.15s;
    white-space: nowrap;
    -webkit-user-select: none;
  }}
  .lut-pill.active {{
    color: #000;
    background: #f0c040;
    border-color: #f0c040;
    font-weight: 600;
  }}
  .lut-pill.loading {{
    opacity: 0.4;
  }}

  /* Loading overlay */
  #loading-overlay {{
    position: fixed; inset: 0;
    background: rgba(0,0,0,0.5);
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; letter-spacing: 0.1em; color: rgba(255,255,255,0.7);
    text-transform: uppercase;
    opacity: 0; pointer-events: none;
    transition: opacity 0.2s;
    z-index: 50;
  }}
  #loading-overlay.show {{ opacity: 1; }}

  /* ── 底部控制栏 ── */
  #controls {{
    position: fixed;
    bottom: 0; left: 0; right: 0;
    height: calc(130px + env(safe-area-inset-bottom, 0px));
    padding-bottom: env(safe-area-inset-bottom, 0px);
    background: linear-gradient(to top, rgba(0,0,0,0.6), transparent);
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    padding-bottom: max(20px, env(safe-area-inset-bottom));
    z-index: 10;
  }}

  #shutter-row {{
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 40px;
    gap: 0;
    position: relative;
  }}

  /* 缩放显示 */
  #zoom-display {{
    position: absolute;
    left: 40px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
  }}
  .zoom-btn {{
    background: rgba(0,0,0,0.4);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 999px;
    color: #fff;
    font-size: 13px;
    font-weight: 600;
    padding: 6px 14px;
    cursor: pointer;
    transition: all 0.15s;
  }}
  .zoom-btn.active {{
    background: rgba(240,192,64,0.9);
    color: #000;
    border-color: #f0c040;
  }}

  /* EV 按钮 */
  #ev-btn {{
    position: absolute;
    right: 40px;
    background: rgba(0,0,0,0.4);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 999px;
    color: #fff;
    font-size: 13px;
    font-weight: 500;
    padding: 6px 12px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 4px;
  }}
  #ev-btn.active {{ border-color: #f0c040; color: #f0c040; }}

  /* 快门按钮 */
  #shutter {{
    width: 72px; height: 72px;
    border-radius: 50%;
    border: 3px solid #fff;
    background: transparent;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: transform 0.1s;
    flex-shrink: 0;
  }}
  #shutter:active {{ transform: scale(0.92); }}
  #shutter-inner {{
    width: 58px; height: 58px;
    border-radius: 50%;
    background: #fff;
    transition: background 0.1s;
  }}
  #shutter:active #shutter-inner {{ background: rgba(255,255,255,0.7); }}
</style>
</head>
<body>

<div id="viewer"><canvas id="c"></canvas></div>
<div id="flash"></div>
<div id="focus-box"></div>
<div id="loading-overlay">Loading...</div>

<!-- 顶部 HUD -->
<div id="hud-top">
  <div class="hud-pill" id="live-tag">
    <div class="hud-dot"></div>
    <span>—</span>
  </div>
  <div id="ev-hud">EV +0.0</div>
  <div id="lut-hud">—</div>
</div>

<!-- 右侧曝光滑条 -->
<div id="ev-bar">
  <span class="ev-icon">☀️</span>
  <input type="range" id="ev-slider" min="-2" max="2" step="0.1" value="0">
  <span class="ev-icon">🌑</span>
</div>

<!-- LUT 条带 -->
<div id="lut-strip-wrap">
  <div id="lut-strip"></div>
</div>

<!-- 底部控制 -->
<div id="controls">
  <div id="shutter-row">
    <div id="zoom-display">
      <button class="zoom-btn active" data-zoom="1">1×</button>
    </div>
    <button id="shutter"><div id="shutter-inner"></div></button>
    <button id="ev-btn">
      <span>±</span>
      <span id="ev-label">0.0</span>
    </button>
  </div>
</div>

<script>
const LUT_NAMES = {lut_names_js};
const LUT_BASE  = "{lut_base_url}";
const LUT_CACHE = {{}};
let currentName = LUT_NAMES[0] || '';
let evValue = 0;
let zoomValue = 1;
let evBarVisible = false;

// ── WebGL
const canvas = document.getElementById('c');
const gl = canvas.getContext('webgl2', {{ preserveDrawingBuffer: true, antialias: false }});

const VS = `#version 300 es
in vec2 aPos; out vec2 vUV;
void main() {{
  vUV = vec2(aPos.x*0.5+0.5, 0.5-aPos.y*0.5);
  gl_Position = vec4(aPos,0,1);
}}`;
const FS = `#version 300 es
precision highp float; precision highp sampler3D;
uniform sampler2D uVideo; uniform sampler3D uLUT;
uniform float uSize,uEV,uZoom;
in vec2 vUV; out vec4 fragColor;
vec3 toL(vec3 c){{return mix(c/12.92,pow((c+.055)/1.055,vec3(2.4)),step(.04045,c));}}
vec3 toS(vec3 c){{c=clamp(c,0.,1.);return mix(c*12.92,1.055*pow(c,vec3(1./2.4))-.055,step(.0031308,c));}}
void main(){{
  vec2 uv=(vUV-.5)/uZoom+.5;
  if(uv.x<0.||uv.x>1.||uv.y<0.||uv.y>1.){{fragColor=vec4(0,0,0,1);return;}}
  vec3 col=clamp(toL(texture(uVideo,uv).rgb)*pow(2.,uEV),0.,1.);
  float sc=(uSize-1.)/uSize,off=.5/uSize;
  fragColor=vec4(toS(clamp(texture(uLUT,col*sc+off).rgb,0.,1.)),1.);
}}`;

function mkS(t,s){{const sh=gl.createShader(t);gl.shaderSource(sh,s);gl.compileShader(sh);return sh;}}
const prog=gl.createProgram();
gl.attachShader(prog,mkS(gl.VERTEX_SHADER,VS));
gl.attachShader(prog,mkS(gl.FRAGMENT_SHADER,FS));
gl.linkProgram(prog); gl.useProgram(prog);

const buf=gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER,buf);
gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,1,1]),gl.STATIC_DRAW);
const aPos=gl.getAttribLocation(prog,'aPos');
gl.enableVertexAttribArray(aPos); gl.vertexAttribPointer(aPos,2,gl.FLOAT,false,0,0);

const [uVideo,uLUT,uSize,uEV,uZoom]=['uVideo','uLUT','uSize','uEV','uZoom'].map(n=>gl.getUniformLocation(prog,n));
gl.uniform1f(uEV,0); gl.uniform1f(uZoom,1);

const vTex=gl.createTexture();
gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D,vTex);
[gl.TEXTURE_MIN_FILTER,gl.TEXTURE_MAG_FILTER].forEach(p=>gl.texParameteri(gl.TEXTURE_2D,p,gl.LINEAR));
[gl.TEXTURE_WRAP_S,gl.TEXTURE_WRAP_T].forEach(p=>gl.texParameteri(gl.TEXTURE_2D,p,gl.CLAMP_TO_EDGE));
gl.uniform1i(uVideo,0);

const lTex=gl.createTexture();
gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_3D,lTex);
[gl.TEXTURE_MIN_FILTER,gl.TEXTURE_MAG_FILTER].forEach(p=>gl.texParameteri(gl.TEXTURE_3D,p,gl.LINEAR));
[gl.TEXTURE_WRAP_S,gl.TEXTURE_WRAP_T,gl.TEXTURE_WRAP_R].forEach(p=>gl.texParameteri(gl.TEXTURE_3D,p,gl.CLAMP_TO_EDGE));
gl.uniform1i(uLUT,1);

// Identity LUT fallback
function uploadIdentityLUT() {{
  const size=2, n=8, rgba=new Uint8Array(n*4);
  let i=0;
  for(let b=0;b<size;b++) for(let g=0;g<size;g++) for(let r=0;r<size;r++) {{
    rgba[i*4]=r*255; rgba[i*4+1]=g*255; rgba[i*4+2]=b*255; rgba[i*4+3]=255; i++;
  }}
  gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_3D,lTex);
  gl.texImage3D(gl.TEXTURE_3D,0,gl.RGBA,2,2,2,0,gl.RGBA,gl.UNSIGNED_BYTE,rgba);
  gl.uniform1f(uSize,2);
}}

function parseCube(text){{
  let size=33,data=[];
  for(const raw of text.split('\n')){{
    const line=raw.trim();
    if(!line||line.startsWith('#')) continue;
    if(line.startsWith('LUT_3D_SIZE')){{size=parseInt(line.split(/\s+/)[1]);continue;}}
    if(/^[A-Z_]/.test(line)) continue;
    const p=line.split(/\s+/),nums=p.map(Number);
    if(p.length===3&&nums.every(n=>!isNaN(n))) data.push(...nums);
  }}
  return {{size,data:new Float32Array(data)}};
}}

function uploadLUT(size,floatData){{
  const n=size*size*size,rgba=new Uint8Array(n*4);
  for(let i=0;i<n;i++){{
    rgba[i*4]  =Math.min(255,floatData[i*3]  *255+.5)|0;
    rgba[i*4+1]=Math.min(255,floatData[i*3+1]*255+.5)|0;
    rgba[i*4+2]=Math.min(255,floatData[i*3+2]*255+.5)|0;
    rgba[i*4+3]=255;
  }}
  gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_3D,lTex);
  gl.texImage3D(gl.TEXTURE_3D,0,gl.RGBA,size,size,size,0,gl.RGBA,gl.UNSIGNED_BYTE,rgba);
  gl.uniform1f(uSize,size);
}}

const overlay  = document.getElementById('loading-overlay');
const lutHud   = document.getElementById('lut-hud');
const liveTag  = document.getElementById('live-tag').querySelector('span');

async function switchLUT(name){{
  if(name===currentName&&LUT_CACHE[name]) return;
  overlay.classList.add('show');
  document.querySelectorAll('.lut-pill').forEach(p=>{{
    p.classList.toggle('active', p.dataset.name===name);
    p.classList.toggle('loading', p.dataset.name===name&&!LUT_CACHE[name]);
  }});
  try{{
    if(!LUT_CACHE[name]){{
      const url=`${{LUT_BASE}}/${{encodeURIComponent(name)}}.cube`;
      const r=await fetch(url);
      if(!r.ok) throw new Error('HTTP '+r.status);
      const text=await r.text();
      LUT_CACHE[name]=parseCube(text);
    }}
    const {{size,data}}=LUT_CACHE[name];
    if(!data||data.length===0) throw new Error('Empty LUT');
    uploadLUT(size,data);
    currentName=name;
    const display=name.replace(/_33_Rec709/g,'').replace(/_/g,' ');
    lutHud.textContent=display;
  }}catch(e){{
    console.error('LUT fail:',e);
    document.querySelectorAll('.lut-pill').forEach(p=>p.classList.toggle('active',p.dataset.name===currentName));
  }}
  finally{{
    overlay.classList.remove('show');
    document.querySelectorAll('.lut-pill').forEach(p=>p.classList.remove('loading'));
  }}
}}

// LUT 条带
const strip=document.getElementById('lut-strip');
LUT_NAMES.forEach(name=>{{
  const p=document.createElement('div');
  p.className='lut-pill'+(name===LUT_NAMES[0]?' active':'');
  p.dataset.name=name;
  p.textContent=name.replace(/_33_Rec709/g,'').replace(/_/g,' ');
  p.addEventListener('pointerdown',e=>{{e.preventDefault();switchLUT(name);}});
  strip.appendChild(p);
}});

// 摄像头
const video=document.createElement('video');
video.autoplay=true; video.playsInline=true; video.muted=true;

let stream = null;

navigator.mediaDevices.getUserMedia({{
  video:{{facingMode:'environment',width:{{ideal:1920}},height:{{ideal:1080}}}},audio:false
}}).then(s=>{{
  stream = s;
  video.srcObject=s; video.play();
  liveTag.textContent='LIVE';
  video.addEventListener('loadedmetadata',()=>{{
    canvas.width=video.videoWidth; canvas.height=video.videoHeight;
    gl.viewport(0,0,canvas.width,canvas.height);
    uploadIdentityLUT();
    requestAnimationFrame(render);
    switchLUT(LUT_NAMES[0]);
  }});
}}).catch(()=>{{ liveTag.textContent='NO CAM'; }});

function render(){{
  if(video.readyState>=2){{
    gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D,vTex);
    gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,gl.RGBA,gl.UNSIGNED_BYTE,video);
    gl.drawArrays(gl.TRIANGLE_STRIP,0,4);
  }}
  requestAnimationFrame(render);
}}

// ── 点击对焦 + 曝光
const focusBox = document.getElementById('focus-box');
document.getElementById('viewer').addEventListener('pointerdown', e=>{{
  const x=e.clientX, y=e.clientY;
  focusBox.style.left=x+'px';
  focusBox.style.top=y+'px';
  focusBox.classList.add('show');
  setTimeout(()=>focusBox.classList.remove('show'), 1200);
  // 隐藏曝光条
  evBarVisible=false;
  document.getElementById('ev-bar').classList.remove('show');
  document.getElementById('ev-btn').classList.remove('active');
}});

// ── 缩放按钮
const zoomLevels=[1,2,3];
let zoomIdx=0;
const zoomDisplay=document.getElementById('zoom-display');
zoomDisplay.innerHTML='';
zoomLevels.forEach((z,i)=>{{
  const btn=document.createElement('button');
  btn.className='zoom-btn'+(i===0?' active':'');
  btn.textContent=z+'×';
  btn.dataset.zoom=z;
  btn.addEventListener('pointerdown',e=>{{
    e.preventDefault();
    zoomIdx=i; zoomValue=z;
    gl.uniform1f(uZoom,z);
    document.querySelectorAll('.zoom-btn').forEach(b=>b.classList.toggle('active',b.dataset.zoom==z));
  }});
  zoomDisplay.appendChild(btn);
}});

// Pinch-to-zoom
let lastDist=0;
document.getElementById('viewer').addEventListener('touchstart',e=>{{
  if(e.touches.length===2){{
    lastDist=Math.hypot(e.touches[0].clientX-e.touches[1].clientX,e.touches[0].clientY-e.touches[1].clientY);
  }}
}},{{passive:true}});
document.getElementById('viewer').addEventListener('touchmove',e=>{{
  if(e.touches.length===2){{
    const dist=Math.hypot(e.touches[0].clientX-e.touches[1].clientX,e.touches[0].clientY-e.touches[1].clientY);
    const delta=dist/lastDist;
    zoomValue=Math.max(1,Math.min(4,zoomValue*delta));
    gl.uniform1f(uZoom,zoomValue);
    lastDist=dist;
  }}
}},{{passive:true}});

// ── 曝光按钮
const evBtn=document.getElementById('ev-btn');
const evBar=document.getElementById('ev-bar');
const evHud=document.getElementById('ev-hud');
const evLabel=document.getElementById('ev-label');

evBtn.addEventListener('pointerdown',e=>{{
  e.preventDefault(); e.stopPropagation();
  evBarVisible=!evBarVisible;
  evBar.classList.toggle('show',evBarVisible);
  evBtn.classList.toggle('active',evBarVisible);
}});

document.getElementById('ev-slider').addEventListener('input',e=>{{
  evValue=parseFloat(e.target.value);
  gl.uniform1f(uEV,evValue);
  const sign=evValue>=0?'+':'';
  evLabel.textContent=sign+evValue.toFixed(1);
  evHud.textContent='EV '+sign+evValue.toFixed(1);
  evHud.classList.add('show');
  clearTimeout(evHud._t);
  evHud._t=setTimeout(()=>evHud.classList.remove('show'),2000);
}});

// ── 快门
const flash=document.getElementById('flash');
document.getElementById('shutter').addEventListener('pointerdown',e=>{{
  e.preventDefault();
  flash.classList.add('go');
  setTimeout(()=>flash.classList.remove('go'),120);
  const ts=new Date().toISOString().replace(/[:.]/g,'-').slice(0,19);
  const safeName=currentName.replace(/_33_Rec709/g,'');
  canvas.toBlob(blob=>{{
    const a=document.createElement('a');
    a.download=`lumen_${{safeName}}_${{ts}}.jpg`;
    a.href=URL.createObjectURL(blob); a.click();
    URL.revokeObjectURL(a.href);
  }},'image/jpeg',0.95);
}});
</script>
</body>
</html>
"""
    components.html(html, height=height, scrolling=False)


# ══════════════════════════════════════
# 界面
# ══════════════════════════════════════

st.markdown("""
<div class="g-topbar">
  <span class="g-logo">LU<span class="g-accent">·</span>MEN</span>
  <span class="g-sub">LUT Color Studio &nbsp;/&nbsp; v0.6</span>
</div>
""", unsafe_allow_html=True)

all_luts  = scan_luts(LUTS_DIR)
lut_names = list(all_luts.keys())

col_mode,col_s0,col_l2,col_lut,col_s2,col_ul,col_s3,col_dl = \
    st.columns([1.4,0.1,3,0.1,0.35,2.5,0.1,1.2])

with col_mode:
    mode = st.radio("mode",["📷  照片","🎥  相机"],horizontal=True,label_visibility="collapsed")

is_camera = "相机" in mode

with col_s0:
    st.markdown('<div class="g-sep-line"></div>',unsafe_allow_html=True)

with col_l2:
    if not is_camera and all_luts:
        sel_name = st.selectbox("lut",lut_names,label_visibility="collapsed")
        sel_path = all_luts[sel_name]
    else:
        sel_name = lut_names[0] if lut_names else None
        sel_path = all_luts.get(sel_name)

with col_s2:
    if not is_camera:
        st.markdown('<div class="g-sep-line"></div>',unsafe_allow_html=True)

with col_ul:
    uploaded = st.file_uploader("p",type=["jpg","jpeg","png","tiff"],
                                 label_visibility="collapsed") if not is_camera else None

with col_s3:
    if not is_camera:
        st.markdown('<div class="g-sep-line"></div>',unsafe_allow_html=True)

with col_dl:
    if not is_camera and uploaded and sel_path:
        img_bytes = uploaded.read()
        result    = process_image(img_bytes,sel_path)
        fname     = f"{os.path.splitext(uploaded.name)[0]}_{sel_name}.jpg"
        st.download_button("⬇ 导出",to_jpeg(result),fname,"image/jpeg")

st.markdown('<div style="height:1px;background:#1c1c1a;margin-top:0.5rem;"></div>',unsafe_allow_html=True)

if is_camera:
    if not lut_names:
        st.markdown('<div class="g-empty"><div class="g-empty-txt">请先添加 LUT 文件</div></div>',unsafe_allow_html=True)
    else:
        camera_component(lut_names, LUT_STATIC_BASE)
else:
    if not uploaded:
        st.markdown("""
        <div class="g-empty">
          <div class="g-empty-frame"></div>
          <div class="g-empty-txt">上传照片开始</div>
        </div>""",unsafe_allow_html=True)
    elif not sel_path:
        st.markdown('<div class="g-empty"><div class="g-empty-txt">请先添加 LUT</div></div>',unsafe_allow_html=True)
    else:
        if "img_bytes" not in dir(): img_bytes=uploaded.read()
        if "result" not in dir(): result=process_image(img_bytes,sel_path)
        st.markdown('<div style="padding:1.2rem 2rem 0;">',unsafe_allow_html=True)
        col_l,col_r=st.columns(2,gap="small")
        with col_l:
            st.markdown('<div class="g-panel-label">— ORIGINAL</div>',unsafe_allow_html=True)
            st.image(Image.open(io.BytesIO(img_bytes)).convert("RGB"),use_container_width=True)
        with col_r:
            st.markdown(f'<div class="g-panel-label g-panel-label-on">— {sel_name}</div>',unsafe_allow_html=True)
            st.image(result,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)
        h,w=result.shape[:2]
        st.markdown(f'<div class="g-infobar"><span><b>LUT &nbsp;</b>{sel_name}</span><span><b>RES &nbsp;</b>{w}×{h}</span><span><b>INTERP &nbsp;</b>Trilinear 3D</span></div>',unsafe_allow_html=True)
