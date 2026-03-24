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

/* 相机模式锁定滚动 */
body.camera-mode { overflow: hidden !important; touch-action: none !important; }
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

def camera_component(lut_names: list, lut_base_url: str = "http://localhost:8501/app/static/luts", height: int = 680):
    lut_names_js = json.dumps(lut_names)
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<meta name="apple-mobile-web-app-capable" content="yes">
<style>
*{{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;}}
html,body{{
  background:#0a0a0a;
  font-family:-apple-system,sans-serif;
  height:100%;overflow:hidden;position:fixed;width:100%;
  user-select:none;color:#fff;
  touch-action:none;
}}

/* 取景器 — 圆角，留边距，DAZZ 风格 */
#viewer{{
  position:absolute;
  top:0;left:0;right:0;
  bottom:160px;
  margin:0 0 0 0;
  overflow:hidden;
  border-radius:0 0 20px 20px;
  background:#111;
}}
canvas{{width:100%;height:100%;object-fit:cover;display:block;}}

/* 闪光 */
#flash{{
  position:absolute;inset:0;border-radius:inherit;
  background:#fff;opacity:0;pointer-events:none;z-index:50;
  transition:opacity 0.04s;
}}
#flash.go{{opacity:0.85;}}

/* Loading */
#loading{{
  position:absolute;inset:0;border-radius:inherit;
  background:rgba(0,0,0,0.5);
  display:flex;align-items:center;justify-content:center;
  opacity:0;pointer-events:none;transition:opacity 0.2s;z-index:40;
}}
#loading.show{{opacity:1;}}
.ring{{
  width:22px;height:22px;
  border:1.5px solid rgba(255,255,255,0.15);
  border-top-color:#fff;border-radius:50%;
  animation:spin 0.7s linear infinite;
}}
@keyframes spin{{to{{transform:rotate(360deg);}}}}

/* 顶部极简 HUD */
#hud{{
  position:absolute;top:0;left:0;right:0;
  padding:12px 16px 8px;
  display:flex;align-items:center;justify-content:space-between;
  z-index:10;
  background:linear-gradient(to bottom,rgba(0,0,0,0.35),transparent);
  pointer-events:none;
}}
#live-dot{{
  width:6px;height:6px;border-radius:50%;
  background:rgba(255,255,255,0.2);
  transition:background 0.3s;
}}
#live-dot.on{{background:#ff3b30;box-shadow:0 0 5px #ff3b30;}}
#lut-name{{
  font-size:10px;font-weight:300;letter-spacing:0.14em;
  color:rgba(255,255,255,0.45);text-transform:uppercase;
  max-width:160px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;
}}

/* 对焦框 + 曝光调节（合并组件） */
#focus-group{{
  position:absolute;
  pointer-events:none;
  z-index:20;
  opacity:0;transition:opacity 0.15s;
  transform:translate(-50%,-50%);
}}
#focus-group.show{{opacity:1;pointer-events:all;}}

#focus-ring{{
  width:64px;height:64px;
  border:1.5px solid rgba(255,200,60,0.9);
  border-radius:4px;
  position:relative;
}}
/* 四角高亮 */
#focus-ring::before,#focus-ring::after{{
  content:'';position:absolute;
  width:10px;height:10px;
  border-color:rgba(255,200,60,1);border-style:solid;
}}
#focus-ring::before{{top:-1px;left:-1px;border-width:2px 0 0 2px;}}
#focus-ring::after{{bottom:-1px;right:-1px;border-width:0 2px 2px 0;}}

/* 曝光调节手柄 */
#ev-handle{{
  position:absolute;
  left:calc(100% + 12px);
  top:50%;transform:translateY(-50%);
  display:flex;align-items:center;gap:6px;
  cursor:ns-resize;
  white-space:nowrap;
}}
#ev-sun{{
  width:22px;height:22px;
  display:flex;align-items:center;justify-content:center;
  border:1px solid rgba(255,200,60,0.7);
  border-radius:50%;
  color:rgba(255,200,60,0.9);
  font-size:11px;
}}
#ev-value-badge{{
  font-size:10px;font-weight:500;
  color:rgba(255,200,60,0.9);
  letter-spacing:0.05em;
  min-width:30px;
}}

/* LUT 条 */
#lut-strip-wrap{{
  position:absolute;
  bottom:0;left:0;right:0;
  height:158px;
  background:#0a0a0a;
  display:flex;flex-direction:column;
  justify-content:flex-start;
  padding-top:8px;
}}
#lut-strip{{
  display:flex;gap:5px;
  overflow-x:auto;padding:4px 14px;
  scrollbar-width:none;-webkit-overflow-scrolling:touch;
  flex-shrink:0;
}}
#lut-strip::-webkit-scrollbar{{display:none;}}
.lut-pill{{
  flex-shrink:0;
  padding:4px 11px;border-radius:3px;
  font-size:9px;font-weight:400;letter-spacing:0.12em;
  color:rgba(255,255,255,0.3);
  background:rgba(255,255,255,0.04);
  border:1px solid rgba(255,255,255,0.07);
  cursor:pointer;transition:all 0.12s;white-space:nowrap;
  text-transform:uppercase;
  -webkit-user-select:none;
}}
.lut-pill.active{{
  color:rgba(255,255,255,0.85);
  border-color:rgba(255,255,255,0.35);
  background:rgba(255,255,255,0.07);
}}

/* 控制行 */
#ctrl-row{{
  flex:1;
  display:flex;align-items:center;
  justify-content:space-between;
  padding:0 28px;
}}

/* 焦距按钮 */
#zoom-btns{{display:flex;gap:3px;align-items:center;}}
.zoom-btn{{
  background:transparent;border:none;
  color:rgba(255,255,255,0.35);
  font-size:11px;font-weight:400;letter-spacing:0.04em;
  padding:5px 9px;cursor:pointer;border-radius:3px;
  transition:all 0.15s;
}}
.zoom-btn.active{{
  color:rgba(255,255,255,0.85);
  background:rgba(255,255,255,0.08);
}}

/* 翻转 */
#flip-btn{{
  background:transparent;border:none;
  width:34px;height:34px;
  display:flex;align-items:center;justify-content:center;
  cursor:pointer;border-radius:50%;
  transition:transform 0.4s;
  color:rgba(255,255,255,0.5);
}}
#flip-btn:active{{transform:rotate(180deg);}}

/* 快门 */
#shutter{{
  width:66px;height:66px;border-radius:50%;
  border:2.5px solid rgba(255,255,255,0.85);
  background:transparent;cursor:pointer;
  display:flex;align-items:center;justify-content:center;
  transition:transform 0.08s;flex-shrink:0;
}}
#shutter:active{{transform:scale(0.92);}}
#shutter-inner{{
  width:52px;height:52px;border-radius:50%;
  background:rgba(255,255,255,0.87);
  transition:background 0.08s;
}}
#shutter:active #shutter-inner{{background:rgba(255,255,255,0.45);}}
</style>
</head>
<body>

<div id="viewer">
  <canvas id="c"></canvas>
  <div id="flash"></div>
  <div id="loading"><div class="ring"></div></div>
  <div id="hud">
    <div id="live-dot"></div>
    <div id="lut-name">—</div>
  </div>
  <!-- 对焦 + 曝光组合 -->
  <div id="focus-group">
    <div id="focus-ring"></div>
    <div id="ev-handle">
      <div id="ev-sun">☀</div>
      <div id="ev-value-badge"></div>
    </div>
  </div>
</div>

<div id="lut-strip-wrap">
  <div id="lut-strip"></div>
  <div id="ctrl-row">
    <div id="zoom-btns"></div>
    <button id="shutter"><div id="shutter-inner"></div></button>
    <button id="flip-btn">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M1 4v6h6"/><path d="M23 20v-6h-6"/>
        <path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15"/>
      </svg>
    </button>
  </div>
</div>

<script>
const LUT_NAMES = {lut_names_js};
const LUT_BASE  = "{lut_base_url}";
const LUT_CACHE = {{}};
let currentName = LUT_NAMES[0]||'';
let evValue=0, zoomValue=1;
let facingMode='environment';

// WebGL
const canvas=document.getElementById('c');
const gl=canvas.getContext('webgl2',{{preserveDrawingBuffer:true}});

const VS=`#version 300 es
in vec2 aPos;out vec2 vUV;
void main(){{vUV=vec2(aPos.x*.5+.5,.5-aPos.y*.5);gl_Position=vec4(aPos,0,1);}}`;
const FS=`#version 300 es
precision highp float;precision highp sampler3D;
uniform sampler2D uVideo;uniform sampler3D uLUT;
uniform float uSize,uEV,uZoom;
in vec2 vUV;out vec4 fragColor;
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
gl.linkProgram(prog);gl.useProgram(prog);

const buf=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buf);
gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,1,1]),gl.STATIC_DRAW);
const aPos=gl.getAttribLocation(prog,'aPos');
gl.enableVertexAttribArray(aPos);gl.vertexAttribPointer(aPos,2,gl.FLOAT,false,0,0);

const [uVideo,uLUT,uSize,uEV,uZoom]=['uVideo','uLUT','uSize','uEV','uZoom'].map(n=>gl.getUniformLocation(prog,n));
gl.uniform1f(uEV,0);gl.uniform1f(uZoom,1);

const vTex=gl.createTexture();
gl.activeTexture(gl.TEXTURE0);gl.bindTexture(gl.TEXTURE_2D,vTex);
[gl.TEXTURE_MIN_FILTER,gl.TEXTURE_MAG_FILTER].forEach(p=>gl.texParameteri(gl.TEXTURE_2D,p,gl.LINEAR));
[gl.TEXTURE_WRAP_S,gl.TEXTURE_WRAP_T].forEach(p=>gl.texParameteri(gl.TEXTURE_2D,p,gl.CLAMP_TO_EDGE));
gl.uniform1i(uVideo,0);

const lTex=gl.createTexture();
gl.activeTexture(gl.TEXTURE1);gl.bindTexture(gl.TEXTURE_3D,lTex);
[gl.TEXTURE_MIN_FILTER,gl.TEXTURE_MAG_FILTER].forEach(p=>gl.texParameteri(gl.TEXTURE_3D,p,gl.LINEAR));
[gl.TEXTURE_WRAP_S,gl.TEXTURE_WRAP_T,gl.TEXTURE_WRAP_R].forEach(p=>gl.texParameteri(gl.TEXTURE_3D,p,gl.CLAMP_TO_EDGE));
gl.uniform1i(uLUT,1);

function uploadIdentityLUT(){{
  const rgba=new Uint8Array([0,0,0,255,255,0,0,255,0,255,0,255,255,255,0,255,0,0,255,255,255,0,255,255,0,255,255,255,255,255,255,255]);
  gl.activeTexture(gl.TEXTURE1);gl.bindTexture(gl.TEXTURE_3D,lTex);
  gl.texImage3D(gl.TEXTURE_3D,0,gl.RGBA,2,2,2,0,gl.RGBA,gl.UNSIGNED_BYTE,rgba);
  gl.uniform1f(uSize,2);
}}

function parseCube(text){{
  let size=33,data=[];
  for(const raw of text.split('\\n')){{
    const line=raw.trim();
    if(!line||line.startsWith('#'))continue;
    if(line.startsWith('LUT_3D_SIZE')){{size=parseInt(line.split(/[\\s]+/)[1]);continue;}}
    if(/^[A-Z_]/.test(line))continue;
    const p=line.split(/[\\s]+/),nums=p.map(Number);
    if(p.length===3&&nums.every(n=>!isNaN(n)))data.push(...nums);
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
  gl.activeTexture(gl.TEXTURE1);gl.bindTexture(gl.TEXTURE_3D,lTex);
  gl.texImage3D(gl.TEXTURE_3D,0,gl.RGBA,size,size,size,0,gl.RGBA,gl.UNSIGNED_BYTE,rgba);
  gl.uniform1f(uSize,size);
}}

const loading=document.getElementById('loading');
const lutName=document.getElementById('lut-name');

async function switchLUT(name){{
  if(name===currentName&&LUT_CACHE[name])return;
  loading.classList.add('show');
  document.querySelectorAll('.lut-pill').forEach(p=>p.classList.toggle('active',p.dataset.name===name));
  try{{
    if(!LUT_CACHE[name]){{
      const r=await fetch(LUT_BASE+'/'+encodeURIComponent(name)+'.cube');
      if(!r.ok)throw new Error('HTTP '+r.status);
      LUT_CACHE[name]=parseCube(await r.text());
    }}
    const {{size,data}}=LUT_CACHE[name];
    if(!data||!data.length)throw new Error('empty');
    uploadLUT(size,data);currentName=name;
    lutName.textContent=name.replace(/_33_Rec709/g,'').replace(/_/g,' ');
    document.querySelectorAll('.lut-pill').forEach(p=>p.classList.toggle('active',p.dataset.name===name));
  }}catch(e){{
    console.error(e);
    document.querySelectorAll('.lut-pill').forEach(p=>p.classList.toggle('active',p.dataset.name===currentName));
  }}
  finally{{loading.classList.remove('show');}}
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
video.autoplay=true;video.playsInline=true;video.muted=true;
const liveDot=document.getElementById('live-dot');
let stream=null;

async function startCamera(){{
  if(stream)stream.getTracks().forEach(t=>t.stop());
  try{{
    stream=await navigator.mediaDevices.getUserMedia({{
      video:{{facingMode,width:{{ideal:1920}},height:{{ideal:1080}}}},audio:false
    }});
    video.srcObject=stream;video.play();
    liveDot.classList.add('on');
    video.addEventListener('loadedmetadata',()=>{{
      canvas.width=video.videoWidth;canvas.height=video.videoHeight;
      gl.viewport(0,0,canvas.width,canvas.height);
      uploadIdentityLUT();
      requestAnimationFrame(render);
      switchLUT(LUT_NAMES[0]);
    }},{{once:true}});
  }}catch(e){{liveDot.style.background='#555';}}
}}
startCamera();

function render(){{
  if(video.readyState>=2){{
    gl.activeTexture(gl.TEXTURE0);gl.bindTexture(gl.TEXTURE_2D,vTex);
    gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,gl.RGBA,gl.UNSIGNED_BYTE,video);
    gl.drawArrays(gl.TRIANGLE_STRIP,0,4);
  }}
  requestAnimationFrame(render);
}}

// ── 对焦 + 曝光 合并交互 ──
const focusGroup=document.getElementById('focus-group');
const evHandle=document.getElementById('ev-handle');
const evSun=document.getElementById('ev-sun');
const evBadge=document.getElementById('ev-value-badge');
let focusTimer=null;
let dragging=false;
let dragStartY=0;
let dragStartEV=0;

// 点击取景器：显示对焦框
document.getElementById('viewer').addEventListener('pointerdown',e=>{{
  if(e.target===evSun||e.target===evHandle||e.target.closest('#ev-handle'))return;
  const x=e.clientX,y=e.clientY;
  focusGroup.style.left=x+'px';
  focusGroup.style.top=y+'px';
  focusGroup.classList.add('show');
  clearTimeout(focusTimer);
  focusTimer=setTimeout(()=>{{
    if(!dragging)focusGroup.classList.remove('show');
  }},3000);
}});

// 拖动太阳图标调曝光
evSun.addEventListener('pointerdown',e=>{{
  e.preventDefault();e.stopPropagation();
  dragging=true;
  dragStartY=e.clientY;
  dragStartEV=evValue;
  evSun.setPointerCapture(e.pointerId);
}});
evSun.addEventListener('pointermove',e=>{{
  if(!dragging)return;
  const delta=(dragStartY-e.clientY)/80;
  evValue=Math.max(-2,Math.min(2,dragStartEV+delta));
  gl.uniform1f(uEV,evValue);
  const s=evValue>=0?'+':'';
  evBadge.textContent=s+evValue.toFixed(1);
  clearTimeout(focusTimer);
}});
evSun.addEventListener('pointerup',e=>{{
  dragging=false;
  focusTimer=setTimeout(()=>focusGroup.classList.remove('show'),2000);
}});

// 焦距
const zoomDefs=[{{label:'28mm',zoom:1}},{{label:'35mm',zoom:1.25}},{{label:'50mm',zoom:1.8}}];
const zoomBtns=document.getElementById('zoom-btns');
zoomDefs.forEach((z,i)=>{{
  const btn=document.createElement('button');
  btn.className='zoom-btn'+(i===0?' active':'');
  btn.textContent=z.label;btn.dataset.zoom=z.zoom;
  btn.addEventListener('pointerdown',e=>{{
    e.preventDefault();zoomValue=z.zoom;gl.uniform1f(uZoom,z.zoom);
    document.querySelectorAll('.zoom-btn').forEach(b=>b.classList.toggle('active',b.dataset.zoom==z.zoom));
  }});
  zoomBtns.appendChild(btn);
}});

// Pinch zoom
let lastDist=0;
document.getElementById('viewer').addEventListener('touchstart',e=>{{
  if(e.touches.length===2)lastDist=Math.hypot(e.touches[0].clientX-e.touches[1].clientX,e.touches[0].clientY-e.touches[1].clientY);
}},{{passive:true}});
document.getElementById('viewer').addEventListener('touchmove',e=>{{
  if(e.touches.length===2){{
    const d=Math.hypot(e.touches[0].clientX-e.touches[1].clientX,e.touches[0].clientY-e.touches[1].clientY);
    zoomValue=Math.max(1,Math.min(4,zoomValue*(d/lastDist)));
    gl.uniform1f(uZoom,zoomValue);lastDist=d;
  }}
}},{{passive:true}});

// 翻转
document.getElementById('flip-btn').addEventListener('pointerdown',async e=>{{
  e.preventDefault();
  facingMode=facingMode==='environment'?'user':'environment';
  await startCamera();
}});

// 快门
const flash=document.getElementById('flash');
document.getElementById('shutter').addEventListener('pointerdown',e=>{{
  e.preventDefault();
  flash.classList.add('go');setTimeout(()=>flash.classList.remove('go'),100);
  const ts=new Date().toISOString().replace(/[:.]/g,'-').slice(0,19);
  canvas.toBlob(blob=>{{
    const a=document.createElement('a');
    a.download='lumen_'+currentName.replace(/_33_Rec709/g,'')+'_'+ts+'.jpg';
    a.href=URL.createObjectURL(blob);a.click();URL.revokeObjectURL(a.href);
  }},'image/jpeg',0.95);
}});
</script>
</body>
</html>"""
    components.html(html, height=height, scrolling=False)


# ══════════════════════════════════════
# 界面
# ══════════════════════════════════════

st.markdown("""
<div class="g-topbar">
  <span class="g-logo">LUMEN</span>
</div>
""", unsafe_allow_html=True)

all_luts  = scan_luts(LUTS_DIR)
lut_names = list(all_luts.keys())

col_mode, col_spacer, col_photo_controls = st.columns([1.4, 0.1, 8])

with col_mode:
    mode = st.radio("mode",["📷  照片","🎥  相机"],horizontal=True,label_visibility="collapsed")

is_camera = "相机" in mode

# 照片模式的控制在右侧展开
if not is_camera:
    with col_spacer:
        st.markdown('<div class="g-sep-line"></div>',unsafe_allow_html=True)
    with col_photo_controls:
        sub1, sub2, sub3, sub4, sub5 = st.columns([0.3, 3.5, 0.1, 2.5, 1.2])
        with sub1:
            st.markdown('<div class="g-ctrl-label">LUT</div>',unsafe_allow_html=True)
        with sub2:
            if all_luts:
                sel_name = st.selectbox("lut",lut_names,label_visibility="collapsed")
                sel_path = all_luts[sel_name]
            else:
                sel_name = sel_path = None
        with sub3:
            st.markdown('<div class="g-sep-line"></div>',unsafe_allow_html=True)
        with sub4:
            uploaded = st.file_uploader("p",type=["jpg","jpeg","png","tiff"],
                                         label_visibility="collapsed")
        with sub5:
            if uploaded and sel_path:
                img_bytes = uploaded.read()
                result    = process_image(img_bytes,sel_path)
                fname     = f"{os.path.splitext(uploaded.name)[0]}_{sel_name}.jpg"
                st.download_button("⬇ 导出",to_jpeg(result),fname,"image/jpeg")
else:
    sel_name = lut_names[0] if lut_names else None
    sel_path = all_luts.get(sel_name)
    uploaded = None

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
