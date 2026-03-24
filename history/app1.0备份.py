"""
LUMEN — LUT Color Studio
运行：streamlit run app.py
"""

import streamlit as st
import numpy as np
from PIL import Image
import io, os, glob

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

/* 隐藏所有 Streamlit chrome */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"],
section[data-testid="stSidebar"],
[data-testid="stStatusWidget"] { display: none !important; }
.stDeployButton { display: none !important; }

.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── 顶栏 ── */
.g-topbar {
    padding: 1.4rem 2.8rem 1.1rem;
    border-bottom: 1px solid #1c1c1a;
    display: flex;
    align-items: baseline;
    gap: 1.6rem;
}
.g-logo {
    font-size: 0.88rem;
    font-weight: 500;
    letter-spacing: 0.55em;
    color: #e2ddd5;
    text-transform: uppercase;
}
.g-accent { color: #a87d45; }
.g-sub {
    font-size: 0.55rem;
    letter-spacing: 0.3em;
    color: #2e2e2c;
    text-transform: uppercase;
}

/* ── 控制栏标签 ── */
.g-ctrl-label {
    font-size: 0.52rem;
    letter-spacing: 0.28em;
    color: #2e2e2c;
    text-transform: uppercase;
    white-space: nowrap;
    padding-top: 6px;
}
.g-sep-line {
    width: 1px;
    height: 36px;
    background: #1c1c1a;
    margin: 0 0.4rem;
    align-self: center;
}

/* 文件上传 */
.stFileUploader { margin: 0 !important; padding: 0 !important; }
.stFileUploader label { display: none !important; }
.stFileUploader section {
    background: transparent !important;
    border: 1px solid #222220 !important;
    border-radius: 2px !important;
    padding: 0 1rem !important;
    min-height: 36px !important;
    display: flex !important;
    align-items: center !important;
    transition: border-color 0.15s !important;
}
.stFileUploader section:hover { border-color: #a87d45 !important; }
.stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] {
    padding: 0 !important;
}
.stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] div span {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.65rem !important;
    color: #444440 !important;
}
.stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] div small,
.stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] div + div {
    display: none !important;
}
.stFileUploader [data-testid="stFileUploaderFile"] {
    background: transparent !important;
    padding: 0 !important;
    border: none !important;
}
.stFileUploader [data-testid="stFileUploaderFile"] small { display: none !important; }
[data-testid="stFileUploaderFileName"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.68rem !important;
    color: #a87d45 !important;
}

/* LUT 选择框 */
.stSelectbox { margin: 0 !important; }
.stSelectbox label { display: none !important; }
.stSelectbox [data-baseweb="select"] > div:first-child {
    background: transparent !important;
    border: 1px solid #222220 !important;
    border-radius: 2px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    color: #c0bcb4 !important;
    min-height: 36px !important;
    transition: border-color 0.15s !important;
}
.stSelectbox [data-baseweb="select"] > div:first-child:hover {
    border-color: #a87d45 !important;
}
[data-baseweb="popover"] {
    background: #181816 !important;
    border: 1px solid #2a2a28 !important;
}
[data-baseweb="menu"] { background: #181816 !important; }
[role="option"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.7rem !important;
    background: #181816 !important;
    color: #888480 !important;
}
[role="option"]:hover, [aria-selected="true"] {
    background: #222220 !important;
    color: #a87d45 !important;
}

/* 下载按钮 */
.stDownloadButton button {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.6rem !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    background: transparent !important;
    border: 1px solid #a87d45 !important;
    color: #a87d45 !important;
    border-radius: 2px !important;
    padding: 0 1.2rem !important;
    min-height: 36px !important;
    transition: all 0.15s !important;
    white-space: nowrap !important;
}
.stDownloadButton button:hover {
    background: #a87d45 !important;
    color: #111210 !important;
}

/* ── 图片区 ── */
.g-panel-label {
    font-size: 0.52rem;
    letter-spacing: 0.3em;
    color: #252523;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    padding: 0 0.1rem;
}
.g-panel-label-on { color: #a87d45; }

.g-empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 60vh;
    gap: 1.2rem;
    color: #1e1e1c;
}
.g-empty-frame {
    width: 52px; height: 36px;
    border: 1px solid #1e1e1c;
}
.g-empty-txt {
    font-size: 0.58rem;
    letter-spacing: 0.35em;
    text-transform: uppercase;
}

/* 底部信息栏 */
.g-infobar {
    font-size: 0.52rem;
    letter-spacing: 0.18em;
    color: #222220;
    padding: 0.8rem 2.8rem;
    border-top: 1px solid #1a1a18;
    margin-top: 1rem;
    display: flex;
    gap: 2.8rem;
}
.g-infobar b { color: #333330; font-weight: 400; }

.stImage img { width: 100% !important; height: auto !important; display: block; }
[data-testid="stHorizontalBlock"] { gap: 2px !important; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════
# 色彩处理
# ══════════════════════════════════════

@st.cache_data
def parse_cube(path: str):
    lut_size, lut_type, data = None, None, []
    with open(path, "r", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"): continue
            if line.startswith("LUT_3D_SIZE"):
                lut_size, lut_type = int(line.split()[-1]), "3D"; continue
            if line.startswith("LUT_1D_SIZE"):
                lut_size, lut_type = int(line.split()[-1]), "1D"; continue
            if line.startswith(("TITLE","DOMAIN_MIN","DOMAIN_MAX")): continue
            parts = line.split()
            if len(parts) == 3:
                try: data.append([float(x) for x in parts])
                except: continue
    arr = np.array(data, dtype=np.float32)
    if lut_type == "3D":
        arr = arr.reshape(lut_size, lut_size, lut_size, 3).transpose(2, 1, 0, 3)
    else:
        arr = arr.reshape(lut_size, 3)
    return arr, lut_size, lut_type

def srgb_to_linear(img):
    img = img.astype(np.float32) / 255.0
    return np.where(img <= 0.04045, img / 12.92, ((img + 0.055) / 1.055) ** 2.4)

def linear_to_srgb(img):
    img = np.clip(img, 0, 1)
    return np.clip(np.where(img <= 0.0031308, img * 12.92,
                            1.055 * (img ** (1/2.4)) - 0.055), 0, 1)

def apply_3d_lut(img, lut, size):
    scale = size - 1
    coords = img * scale
    lo = np.floor(coords).astype(np.int32)
    hi = np.minimum(lo + 1, size - 1)
    f = coords - lo
    r0,g0,b0 = lo[...,0], lo[...,1], lo[...,2]
    r1,g1,b1 = hi[...,0], hi[...,1], hi[...,2]
    fr,fg,fb = f[...,0:1], f[...,1:2], f[...,2:3]
    c00 = lut[r0,g0,b0]*(1-fr) + lut[r1,g0,b0]*fr
    c01 = lut[r0,g0,b1]*(1-fr) + lut[r1,g0,b1]*fr
    c10 = lut[r0,g1,b0]*(1-fr) + lut[r1,g1,b0]*fr
    c11 = lut[r0,g1,b1]*(1-fr) + lut[r1,g1,b1]*fr
    return ((c00*(1-fg)+c10*fg)*(1-fb) + (c01*(1-fg)+c11*fg)*fb).astype(np.float32)

def apply_1d_lut(img, lut, size):
    scale = size - 1; result = np.zeros_like(img)
    for ch in range(3):
        c = img[...,ch] * scale
        lo = np.floor(c).astype(np.int32); hi = np.minimum(lo+1, size-1); f = c - lo
        result[...,ch] = lut[lo,ch]*(1-f) + lut[hi,ch]*f
    return result.astype(np.float32)

@st.cache_data
def process_image(img_bytes: bytes, lut_path: str) -> np.ndarray:
    pil = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    if max(pil.size) > 2800:
        pil.thumbnail((2800, 2800), Image.LANCZOS)
    arr = np.array(pil, dtype=np.float32)
    lin = srgb_to_linear(arr)
    lut, size, ltype = parse_cube(lut_path)
    out = apply_3d_lut(lin, lut, size) if ltype == "3D" else apply_1d_lut(lin, lut, size)
    return (linear_to_srgb(out) * 255).astype(np.uint8)

def to_jpeg(arr: np.ndarray, quality=93) -> bytes:
    buf = io.BytesIO()
    Image.fromarray(arr).save(buf, format="JPEG", quality=quality)
    return buf.getvalue()

def scan_luts(directory: str) -> dict:
    paths = sorted(glob.glob(os.path.join(directory, "*.cube")) +
                   glob.glob(os.path.join(directory, "*.CUBE")))
    return {os.path.splitext(os.path.basename(p))[0]: p for p in paths}

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LUTS_DIR   = os.path.join(SCRIPT_DIR, "assets", "luts")
os.makedirs(LUTS_DIR, exist_ok=True)


# ══════════════════════════════════════
# 界面
# ══════════════════════════════════════

# 顶栏
st.markdown("""
<div class="g-topbar">
  <span class="g-logo">LU<span class="g-accent">·</span>MEN</span>
  <span class="g-sub">LUT Color Studio &nbsp;/&nbsp; v0.1</span>
</div>
""", unsafe_allow_html=True)

# 控制栏
all_luts = scan_luts(LUTS_DIR)

col_label1, col_upload, col_sep, col_label2, col_lut, col_sep2, col_dl = \
    st.columns([0.5, 3, 0.15, 0.5, 3.5, 0.15, 1.4])

with col_label1:
    st.markdown('<div class="g-ctrl-label">照片</div>', unsafe_allow_html=True)

with col_upload:
    uploaded = st.file_uploader("p", type=["jpg","jpeg","png","tiff"],
                                 label_visibility="collapsed")

with col_sep:
    st.markdown('<div class="g-sep-line"></div>', unsafe_allow_html=True)

with col_label2:
    st.markdown('<div class="g-ctrl-label">LUT</div>', unsafe_allow_html=True)

with col_lut:
    if all_luts:
        sel_name = st.selectbox("l", list(all_luts.keys()),
                                 label_visibility="collapsed")
        sel_path = all_luts[sel_name]
    else:
        st.caption("请将 .cube 文件放入 assets/luts/")
        sel_name = sel_path = None

with col_sep2:
    st.markdown('<div class="g-sep-line"></div>', unsafe_allow_html=True)

with col_dl:
    if uploaded and sel_path:
        img_bytes = uploaded.read()
        result = process_image(img_bytes, sel_path)
        fname = f"{os.path.splitext(uploaded.name)[0]}_{sel_name}.jpg"
        st.download_button("⬇ 导出", to_jpeg(result), fname, "image/jpeg")

st.markdown('<div style="height:1px;background:#1c1c1a;margin-top:0.6rem;"></div>',
            unsafe_allow_html=True)

# 图片区
if not uploaded:
    st.markdown("""
    <div class="g-empty">
      <div class="g-empty-frame"></div>
      <div class="g-empty-txt">上传照片开始</div>
    </div>
    """, unsafe_allow_html=True)

elif not sel_path:
    st.markdown("""
    <div class="g-empty">
      <div class="g-empty-txt">请先添加 LUT 文件</div>
    </div>
    """, unsafe_allow_html=True)

else:
    if "img_bytes" not in dir():
        img_bytes = uploaded.read()
    if "result" not in dir():
        result = process_image(img_bytes, sel_path)

    st.markdown('<div style="padding: 1.2rem 2.8rem 0;">', unsafe_allow_html=True)
    col_l, col_r = st.columns(2, gap="small")

    with col_l:
        st.markdown('<div class="g-panel-label">— ORIGINAL</div>', unsafe_allow_html=True)
        st.image(Image.open(io.BytesIO(img_bytes)).convert("RGB"), use_container_width=True)

    with col_r:
        st.markdown(
            f'<div class="g-panel-label g-panel-label-on">— {sel_name}</div>',
            unsafe_allow_html=True)
        st.image(result, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    h, w = result.shape[:2]
    st.markdown(
        f'<div class="g-infobar">'
        f'<span><b>LUT &nbsp;</b>{sel_name}</span>'
        f'<span><b>SIZE &nbsp;</b>{w} × {h} px</span>'
        f'<span><b>INTERP &nbsp;</b>Trilinear 3D</span>'
        f'<span><b>SPACE &nbsp;</b>sRGB → Linear → sRGB</span>'
        f'</div>',
        unsafe_allow_html=True
    )
