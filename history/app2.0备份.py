"""
LUMEN — LUT Color Studio
运行：streamlit run app.py
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
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"],
section[data-testid="stSidebar"],
[data-testid="stStatusWidget"] { display: none !important; }
.stDeployButton { display: none !important; }

.main .block-container { padding: 0 !important; max-width: 100% !important; }

.g-topbar {
    padding: 1.4rem 2.8rem 1.1rem;
    border-bottom: 1px solid #1c1c1a;
    display: flex;
    align-items: baseline;
    gap: 1.6rem;
}
.g-logo { font-size: 0.88rem; font-weight: 500; letter-spacing: 0.55em; color: #e2ddd5; text-transform: uppercase; }
.g-accent { color: #a87d45; }
.g-sub { font-size: 0.55rem; letter-spacing: 0.3em; color: #2e2e2c; text-transform: uppercase; }

.g-ctrl-label {
    font-size: 0.52rem; letter-spacing: 0.28em; color: #2e2e2c;
    text-transform: uppercase; white-space: nowrap; padding-top: 6px;
}
.g-sep-line { width: 1px; height: 36px; background: #1c1c1a; margin: 0 0.4rem; align-self: center; }

/* 模式切换按钮 */
.stRadio { margin: 0 !important; }
.stRadio label { display: none !important; }
.stRadio div[role="radiogroup"] { display: flex !important; gap: 0 !important; }
.stRadio div[role="radiogroup"] label {
    display: flex !important;
    align-items: center !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.58rem !important;
    letter-spacing: 0.22em !important;
    text-transform: uppercase !important;
    color: #444440 !important;
    padding: 0.3rem 1rem !important;
    border: 1px solid #1e1e1c !important;
    border-right: none !important;
    cursor: pointer !important;
    transition: all 0.15s !important;
    white-space: nowrap !important;
}
.stRadio div[role="radiogroup"] label:last-child { border-right: 1px solid #1e1e1c !important; }
.stRadio div[role="radiogroup"] label:has(input:checked) {
    color: #a87d45 !important;
    border-color: #a87d45 !important;
    z-index: 1 !important;
}
.stRadio div[role="radiogroup"] label:hover { color: #706c64 !important; }
.stRadio input[type="radio"] { display: none !important; }

/* 文件上传 */
.stFileUploader { margin: 0 !important; padding: 0 !important; }
.stFileUploader label { display: none !important; }
.stFileUploader section {
    background: transparent !important; border: 1px solid #222220 !important;
    border-radius: 2px !important; padding: 0 1rem !important;
    min-height: 36px !important; display: flex !important;
    align-items: center !important; transition: border-color 0.15s !important;
}
.stFileUploader section:hover { border-color: #a87d45 !important; }
.stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] { padding: 0 !important; }
.stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] div span {
    font-family: 'DM Mono', monospace !important; font-size: 0.65rem !important; color: #444440 !important;
}
.stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] div small,
.stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] div + div { display: none !important; }
.stFileUploader [data-testid="stFileUploaderFile"] { background: transparent !important; padding: 0 !important; border: none !important; }
.stFileUploader [data-testid="stFileUploaderFile"] small { display: none !important; }
[data-testid="stFileUploaderFileName"] { font-family: 'DM Mono', monospace !important; font-size: 0.68rem !important; color: #a87d45 !important; }

/* LUT 选择框 */
.stSelectbox { margin: 0 !important; }
.stSelectbox label { display: none !important; }
.stSelectbox [data-baseweb="select"] > div:first-child {
    background: transparent !important; border: 1px solid #222220 !important;
    border-radius: 2px !important; font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important; color: #c0bcb4 !important;
    min-height: 36px !important; transition: border-color 0.15s !important;
}
.stSelectbox [data-baseweb="select"] > div:first-child:hover { border-color: #a87d45 !important; }
[data-baseweb="popover"] { background: #181816 !important; border: 1px solid #2a2a28 !important; }
[data-baseweb="menu"] { background: #181816 !important; }
[role="option"] { font-family: 'DM Mono', monospace !important; font-size: 0.7rem !important; background: #181816 !important; color: #888480 !important; }
[role="option"]:hover, [aria-selected="true"] { background: #222220 !important; color: #a87d45 !important; }

/* 下载按钮 */
.stDownloadButton button {
    font-family: 'DM Mono', monospace !important; font-size: 0.6rem !important;
    letter-spacing: 0.2em !important; text-transform: uppercase !important;
    background: transparent !important; border: 1px solid #a87d45 !important;
    color: #a87d45 !important; border-radius: 2px !important;
    padding: 0 1.2rem !important; min-height: 36px !important;
    transition: all 0.15s !important; white-space: nowrap !important;
}
.stDownloadButton button:hover { background: #a87d45 !important; color: #111210 !important; }

.g-panel-label { font-size: 0.52rem; letter-spacing: 0.3em; color: #252523; text-transform: uppercase; margin-bottom: 0.5rem; padding: 0 0.1rem; }
.g-panel-label-on { color: #a87d45; }

.g-empty { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 60vh; gap: 1.2rem; color: #1e1e1c; }
.g-empty-frame { width: 52px; height: 36px; border: 1px solid #1e1e1c; }
.g-empty-txt { font-size: 0.58rem; letter-spacing: 0.35em; text-transform: uppercase; }

.g-infobar { font-size: 0.52rem; letter-spacing: 0.18em; color: #222220; padding: 0.8rem 2.8rem; border-top: 1px solid #1a1a18; margin-top: 1rem; display: flex; gap: 2.8rem; }
.g-infobar b { color: #333330; font-weight: 400; }

.stImage img { width: 100% !important; height: auto !important; display: block; }
[data-testid="stHorizontalBlock"] { gap: 2px !important; }

/* iframe 无边框 */
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

def lut_to_js_array(lut_path):
    """把 LUT 序列化为 JS Uint8Array（RGBA），避免浮点纹理扩展依赖"""
    arr, size, ltype = parse_cube(lut_path)
    if ltype == "3D":
        flat = arr.transpose(2,1,0,3).reshape(-1, 3)
    else:
        flat = arr.reshape(-1, 3)
    # 转成 RGBA uint8（A 固定255）
    rgb = np.clip(flat, 0, 1)
    rgba = np.ones((len(rgb), 4), dtype=np.float32)
    rgba[:, :3] = rgb
    data = (rgba * 255).astype(np.uint8).flatten().tolist()
    return json.dumps(data), size

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LUTS_DIR   = os.path.join(SCRIPT_DIR, "assets", "luts")
os.makedirs(LUTS_DIR, exist_ok=True)


# ══════════════════════════════════════
# 实时相机 WebGL 组件
# ══════════════════════════════════════

def camera_component(lut_data_json: str, lut_size: int, height: int = 700):
    """
    注入 WebGL2 实时相机 + LUT 组件。
    LUT 作为 3D 纹理上传 GPU，fragment shader 做三线性插值。
    """
    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    background: #111210;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: {height}px;
    font-family: 'DM Mono', monospace;
    overflow: hidden;
  }}

  #container {{
    position: relative;
    width: 100%;
    max-width: 960px;
  }}

  canvas {{
    width: 100%;
    height: auto;
    display: block;
    background: #0a0a09;
  }}

  /* 底部控制条 */
  #controls {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 2rem;
    padding: 1.2rem 2rem;
    background: #0e0e0d;
    border-top: 1px solid #1c1c1a;
  }}

  #shutter {{
    width: 56px; height: 56px;
    border-radius: 50%;
    border: 2px solid #a87d45;
    background: transparent;
    cursor: pointer;
    position: relative;
    transition: all 0.15s;
    display: flex; align-items: center; justify-content: center;
  }}
  #shutter::after {{
    content: '';
    width: 42px; height: 42px;
    border-radius: 50%;
    background: #a87d45;
    transition: all 0.15s;
  }}
  #shutter:hover::after {{ background: #c49355; }}
  #shutter:active {{ transform: scale(0.94); }}

  #status {{
    font-size: 0.52rem;
    letter-spacing: 0.25em;
    color: #2e2e2c;
    text-transform: uppercase;
    min-width: 120px;
    text-align: center;
  }}
  #status.on {{ color: #a87d45; }}

  #info {{
    font-size: 0.48rem;
    letter-spacing: 0.2em;
    color: #1e1e1c;
    text-transform: uppercase;
    text-align: right;
    min-width: 120px;
  }}

  /* 闪光动画 */
  #flash {{
    position: absolute;
    inset: 0;
    background: white;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.05s;
  }}
  #flash.active {{ opacity: 0.6; }}
</style>
</head>
<body>

<div id="container">
  <canvas id="c"></canvas>
  <div id="flash"></div>
  <div id="controls">
    <div id="status">initializing...</div>
    <button id="shutter" title="拍摄"></button>
    <div id="info">LUT · {lut_size}³</div>
  </div>
</div>

<script>
// ── LUT 数据（从 Python 传入）
const LUT_DATA = {lut_data_json};
const LUT_SIZE = {lut_size};

const canvas  = document.getElementById('c');
const status  = document.getElementById('status');
const flash   = document.getElementById('flash');
const shutter = document.getElementById('shutter');

// ── WebGL2 初始化
const gl = canvas.getContext('webgl2', {{ preserveDrawingBuffer: true }});
if (!gl) {{
  status.textContent = 'WebGL2 not supported';
  status.classList.add('on');
}}

// ── Vertex Shader
const VS = `#version 300 es
in vec2 aPos;
out vec2 vUV;
void main() {{
  vUV = aPos * 0.5 + 0.5;
  vUV.y = 1.0 - vUV.y;   // flip Y
  gl_Position = vec4(aPos, 0.0, 1.0);
}}`;

// ── Fragment Shader（三线性 3D LUT 插值）
const FS = `#version 300 es
precision highp float;
precision highp sampler3D;
uniform sampler2D uVideo;
uniform sampler3D uLUT;
uniform float uSize;
in vec2 vUV;
out vec4 fragColor;

vec3 srgbToLinear(vec3 c) {{
  return mix(c / 12.92, pow((c + 0.055) / 1.055, vec3(2.4)), step(0.04045, c));
}}
vec3 linearToSrgb(vec3 c) {{
  return mix(c * 12.92, 1.055 * pow(c, vec3(1.0/2.4)) - 0.055, step(0.0031308, c));
}}

void main() {{
  vec3 color = texture(uVideo, vUV).rgb;

  // sRGB → linear
  vec3 lin = srgbToLinear(color);

  // LUT 查找：texel 中心采样，避免边界问题
  float scale  = (uSize - 1.0) / uSize;
  float offset = 0.5 / uSize;
  vec3 lutCoord = clamp(lin, 0.0, 1.0) * scale + offset;
  vec3 graded = texture(uLUT, lutCoord).rgb;

  // linear → sRGB
  vec3 out_col = linearToSrgb(clamp(graded, 0.0, 1.0));

  fragColor = vec4(out_col, 1.0);
}}`;

// ── 编译 Shader
function compileShader(type, src) {{
  const s = gl.createShader(type);
  gl.shaderSource(s, src);
  gl.compileShader(s);
  if (!gl.getShaderParameter(s, gl.COMPILE_STATUS))
    console.error(gl.getShaderInfoLog(s));
  return s;
}}

const prog = gl.createProgram();
gl.attachShader(prog, compileShader(gl.VERTEX_SHADER, VS));
gl.attachShader(prog, compileShader(gl.FRAGMENT_SHADER, FS));
gl.linkProgram(prog);
gl.useProgram(prog);

// ── 全屏四边形
const buf = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, buf);
gl.bufferData(gl.ARRAY_BUFFER,
  new Float32Array([-1,-1, 1,-1, -1,1, 1,1]), gl.STATIC_DRAW);
const aPos = gl.getAttribLocation(prog, 'aPos');
gl.enableVertexAttribArray(aPos);
gl.vertexAttribPointer(aPos, 2, gl.FLOAT, false, 0, 0);

const uVideo = gl.getUniformLocation(prog, 'uVideo');
const uLUT   = gl.getUniformLocation(prog, 'uLUT');
const uSize  = gl.getUniformLocation(prog, 'uSize');
gl.uniform1f(uSize, LUT_SIZE);

// ── 视频纹理
const videoTex = gl.createTexture();
gl.activeTexture(gl.TEXTURE0);
gl.bindTexture(gl.TEXTURE_2D, videoTex);
gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
gl.uniform1i(uVideo, 0);

// ── 3D LUT 纹理
const lutTex = gl.createTexture();
gl.activeTexture(gl.TEXTURE1);
gl.bindTexture(gl.TEXTURE_3D, lutTex);
gl.texParameteri(gl.TEXTURE_3D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
gl.texParameteri(gl.TEXTURE_3D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
gl.texParameteri(gl.TEXTURE_3D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
gl.texParameteri(gl.TEXTURE_3D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
gl.texParameteri(gl.TEXTURE_3D, gl.TEXTURE_WRAP_R, gl.CLAMP_TO_EDGE);

// 把 LUT 数据上传到 GPU（RGBA Uint8，无需浮点纹理扩展）
const lutUint8 = new Uint8Array(LUT_DATA);
gl.texImage3D(
  gl.TEXTURE_3D, 0, gl.RGBA,
  LUT_SIZE, LUT_SIZE, LUT_SIZE,
  0, gl.RGBA, gl.UNSIGNED_BYTE, lutUint8
);
gl.uniform1i(uLUT, 1);

// ── 摄像头
const video = document.createElement('video');
video.autoplay = true;
video.playsInline = true;
video.muted = true;

navigator.mediaDevices.getUserMedia({{
  video: {{ facingMode: 'environment', width: {{ ideal: 1920 }}, height: {{ ideal: 1080 }} }},
  audio: false
}})
.then(stream => {{
  video.srcObject = stream;
  video.play();
  status.textContent = 'live';
  status.classList.add('on');
  video.addEventListener('loadedmetadata', () => {{
    canvas.width  = video.videoWidth;
    canvas.height = video.videoHeight;
    gl.viewport(0, 0, canvas.width, canvas.height);
    requestAnimationFrame(render);
  }});
}})
.catch(err => {{
  status.textContent = 'camera denied';
  console.error(err);
}});

// ── 渲染循环
function render() {{
  if (video.readyState >= video.HAVE_CURRENT_DATA) {{
    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, videoTex);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, video);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  }}
  requestAnimationFrame(render);
}}

// ── 快门：捕获当前帧保存
shutter.addEventListener('click', () => {{
  // 闪光效果
  flash.classList.add('active');
  setTimeout(() => flash.classList.remove('active'), 120);

  // 导出 canvas 为图片
  const link = document.createElement('a');
  const ts   = new Date().toISOString().replace(/[:.]/g,'-').slice(0,19);
  link.download = `lumen_${{ts}}.jpg`;
  canvas.toBlob(blob => {{
    link.href = URL.createObjectURL(blob);
    link.click();
    URL.revokeObjectURL(link.href);
  }}, 'image/jpeg', 0.93);
}});
</script>
</body>
</html>
"""
    components.html(html, height=height + 100, scrolling=False)


# ══════════════════════════════════════
# 界面
# ══════════════════════════════════════

# 顶栏
st.markdown("""
<div class="g-topbar">
  <span class="g-logo">LU<span class="g-accent">·</span>MEN</span>
  <span class="g-sub">LUT Color Studio &nbsp;/&nbsp; v0.2</span>
</div>
""", unsafe_allow_html=True)

all_luts = scan_luts(LUTS_DIR)

# 控制栏
col_mode, col_sep0, col_label2, col_lut, col_sep2, col_upload_label, col_upload, col_sep3, col_dl = \
    st.columns([1.5, 0.12, 0.4, 3.2, 0.12, 0.4, 2.5, 0.12, 1.3])

with col_mode:
    mode = st.radio("mode", ["📷  照片", "🎥  相机"],
                    horizontal=True, label_visibility="collapsed")

with col_sep0:
    st.markdown('<div class="g-sep-line"></div>', unsafe_allow_html=True)

with col_label2:
    st.markdown('<div class="g-ctrl-label">LUT</div>', unsafe_allow_html=True)

with col_lut:
    if all_luts:
        sel_name = st.selectbox("lut", list(all_luts.keys()),
                                 label_visibility="collapsed")
        sel_path = all_luts[sel_name]
    else:
        st.caption("请将 .cube 文件放入 assets/luts/")
        sel_name = sel_path = None

with col_sep2:
    st.markdown('<div class="g-sep-line"></div>', unsafe_allow_html=True)

# 只在照片模式显示上传
is_camera = "相机" in mode

with col_upload_label:
    if not is_camera:
        st.markdown('<div class="g-ctrl-label">照片</div>', unsafe_allow_html=True)

with col_upload:
    if not is_camera:
        uploaded = st.file_uploader("p", type=["jpg","jpeg","png","tiff"],
                                     label_visibility="collapsed")
    else:
        uploaded = None

with col_sep3:
    if not is_camera:
        st.markdown('<div class="g-sep-line"></div>', unsafe_allow_html=True)

with col_dl:
    if not is_camera and uploaded and sel_path:
        img_bytes = uploaded.read()
        result    = process_image(img_bytes, sel_path)
        fname     = f"{os.path.splitext(uploaded.name)[0]}_{sel_name}.jpg"
        st.download_button("⬇ 导出", to_jpeg(result), fname, "image/jpeg")

st.markdown('<div style="height:1px;background:#1c1c1a;margin-top:0.6rem;"></div>',
            unsafe_allow_html=True)

# ── 相机模式
if is_camera:
    if not sel_path:
        st.markdown("""
        <div class="g-empty">
          <div class="g-empty-txt">请先选择 LUT</div>
        </div>""", unsafe_allow_html=True)
    else:
        lut_json, lut_sz = lut_to_js_array(sel_path)
        camera_component(lut_json, lut_sz, height=620)

# ── 照片模式
else:
    if not uploaded:
        st.markdown("""
        <div class="g-empty">
          <div class="g-empty-frame"></div>
          <div class="g-empty-txt">上传照片开始</div>
        </div>""", unsafe_allow_html=True)
    elif not sel_path:
        st.markdown("""
        <div class="g-empty">
          <div class="g-empty-txt">请先添加 LUT 文件</div>
        </div>""", unsafe_allow_html=True)
    else:
        if "img_bytes" not in dir(): img_bytes = uploaded.read()
        if "result"    not in dir(): result    = process_image(img_bytes, sel_path)

        st.markdown('<div style="padding: 1.2rem 2.8rem 0;">', unsafe_allow_html=True)
        col_l, col_r = st.columns(2, gap="small")
        with col_l:
            st.markdown('<div class="g-panel-label">— ORIGINAL</div>', unsafe_allow_html=True)
            st.image(Image.open(io.BytesIO(img_bytes)).convert("RGB"), use_container_width=True)
        with col_r:
            st.markdown(f'<div class="g-panel-label g-panel-label-on">— {sel_name}</div>',
                        unsafe_allow_html=True)
            st.image(result, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        h, w = result.shape[:2]
        st.markdown(
            f'<div class="g-infobar">'
            f'<span><b>LUT &nbsp;</b>{sel_name}</span>'
            f'<span><b>RES &nbsp;</b>{w}×{h}</span>'
            f'<span><b>INTERP &nbsp;</b>Trilinear 3D</span>'
            f'<span><b>SPACE &nbsp;</b>sRGB → Linear → sRGB</span>'
            f'</div>', unsafe_allow_html=True)
