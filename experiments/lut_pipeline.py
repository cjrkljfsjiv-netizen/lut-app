"""
LUT Color Pipeline - MVP 色彩验证脚本
=====================================
流程：输入照片 → 色彩空间转换 → 应用 .cube LUT → 叠加胶片效果 → 输出照片

依赖安装：
    pip install Pillow numpy

用法：
    python lut_pipeline.py --input photo.jpg --lut your_lut.cube --output result.jpg
    python lut_pipeline.py --input photo.jpg --lut your_lut.cube --grain 0.04 --leak 0.3
    python lut_pipeline.py --input photo.jpg --lut your_lut.cube --preview  # 对比预览
"""

import argparse
import sys
import numpy as np
from PIL import Image, ImageFilter


# ─────────────────────────────────────────────
# 1. 读取 .cube 文件
# ─────────────────────────────────────────────

def parse_cube(path: str) -> tuple[np.ndarray, int]:
    """
    解析 .cube 文件，返回 LUT 数组和 LUT 尺寸。
    支持 1D 和 3D LUT。
    """
    lut_size = None
    lut_type = None
    data = []

    with open(path, "r") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if line.startswith("LUT_3D_SIZE"):
                lut_size = int(line.split()[-1])
                lut_type = "3D"
                continue

            if line.startswith("LUT_1D_SIZE"):
                lut_size = int(line.split()[-1])
                lut_type = "1D"
                continue

            # 跳过其他元数据行
            if line.startswith(("TITLE", "DOMAIN_MIN", "DOMAIN_MAX")):
                continue

            parts = line.split()
            if len(parts) == 3:
                try:
                    data.append([float(x) for x in parts])
                except ValueError:
                    continue

    if lut_size is None or lut_type is None:
        raise ValueError("无法解析 .cube 文件，请确认格式正确")

    lut_array = np.array(data, dtype=np.float32)

    if lut_type == "3D":
        # .cube 的顺序是 R 最快变化，reshape 成 (B, G, R, 3)
        # 然后转置成 (R, G, B, 3) 方便后续索引
        lut_array = lut_array.reshape(lut_size, lut_size, lut_size, 3)
        lut_array = lut_array.transpose(2, 1, 0, 3)  # 转成 R, G, B 索引顺序
    else:
        lut_array = lut_array.reshape(lut_size, 3)

    print(f"✅ LUT 加载成功：{lut_type} LUT，尺寸 {lut_size}")
    return lut_array, lut_size, lut_type


# ─────────────────────────────────────────────
# 2. 色彩空间转换
# ─────────────────────────────────────────────

def srgb_to_linear(img: np.ndarray) -> np.ndarray:
    """
    sRGB → 线性光空间（去除 gamma 编码）
    大多数手机照片是 sRGB，需要先转换到线性空间再做色彩处理
    """
    img = img.astype(np.float32) / 255.0
    # sRGB gamma 解码公式
    linear = np.where(
        img <= 0.04045,
        img / 12.92,
        ((img + 0.055) / 1.055) ** 2.4
    )
    return linear


def linear_to_srgb(img: np.ndarray) -> np.ndarray:
    """
    线性光空间 → sRGB（重新应用 gamma 编码，准备显示/保存）
    """
    img = np.clip(img, 0.0, 1.0)
    srgb = np.where(
        img <= 0.0031308,
        img * 12.92,
        1.055 * (img ** (1.0 / 2.4)) - 0.055
    )
    return np.clip(srgb, 0.0, 1.0)


# ─────────────────────────────────────────────
# 3. 应用 3D LUT（三线性插值）
# ─────────────────────────────────────────────

def apply_3d_lut(img_linear: np.ndarray, lut: np.ndarray, lut_size: int) -> np.ndarray:
    """
    对线性空间图像应用 3D LUT，使用三线性插值。
    
    三线性插值：在 LUT 节点之间平滑过渡，避免色带（banding）
    这是专业软件的标准做法。
    """
    h, w, _ = img_linear.shape

    # 将像素值映射到 LUT 索引空间 [0, lut_size-1]
    scale = lut_size - 1
    coords = img_linear * scale  # shape: (H, W, 3) — 每个通道的浮点索引

    # 取整数部分（低位）和小数部分（插值权重）
    idx_low = np.floor(coords).astype(np.int32)
    idx_high = np.minimum(idx_low + 1, lut_size - 1)
    frac = coords - idx_low  # 小数部分，即插值权重

    # 分离 R, G, B 的索引和权重
    r0, g0, b0 = idx_low[..., 0], idx_low[..., 1], idx_low[..., 2]
    r1, g1, b1 = idx_high[..., 0], idx_high[..., 1], idx_high[..., 2]
    fr, fg, fb = frac[..., 0:1], frac[..., 1:2], frac[..., 2:3]

    # 三线性插值：在 8 个 LUT 节点之间插值
    # 按 R, G, B 三个轴依次插值
    c000 = lut[r0, g0, b0]
    c100 = lut[r1, g0, b0]
    c010 = lut[r0, g1, b0]
    c110 = lut[r1, g1, b0]
    c001 = lut[r0, g0, b1]
    c101 = lut[r1, g0, b1]
    c011 = lut[r0, g1, b1]
    c111 = lut[r1, g1, b1]

    # 沿 R 轴插值
    c00 = c000 * (1 - fr) + c100 * fr
    c01 = c001 * (1 - fr) + c101 * fr
    c10 = c010 * (1 - fr) + c110 * fr
    c11 = c011 * (1 - fr) + c111 * fr

    # 沿 G 轴插值
    c0 = c00 * (1 - fg) + c10 * fg
    c1 = c01 * (1 - fg) + c11 * fg

    # 沿 B 轴插值
    result = c0 * (1 - fb) + c1 * fb

    return result.astype(np.float32)


def apply_1d_lut(img_linear: np.ndarray, lut: np.ndarray, lut_size: int) -> np.ndarray:
    """应用 1D LUT（对每个通道独立映射，类似色彩曲线）"""
    scale = lut_size - 1
    result = np.zeros_like(img_linear)
    for ch in range(3):
        coords = img_linear[..., ch] * scale
        idx_low = np.floor(coords).astype(np.int32)
        idx_high = np.minimum(idx_low + 1, lut_size - 1)
        frac = coords - idx_low
        result[..., ch] = lut[idx_low, ch] * (1 - frac) + lut[idx_high, ch] * frac
    return result.astype(np.float32)


# ─────────────────────────────────────────────
# 4. 胶片效果（在线性空间叠加，这是关键！）
# ─────────────────────────────────────────────

def add_film_grain(img_linear: np.ndarray, intensity: float = 0.03) -> np.ndarray:
    """
    在线性光空间叠加胶片颗粒。
    
    ⚠️  重要：必须在 LUT 之前、在线性空间里加颗粒
         在 sRGB 空间加颗粒会导致暗部颗粒过重、亮部过轻，效果假
    
    intensity: 颗粒强度，推荐 0.02 - 0.06
    """
    h, w, c = img_linear.shape

    # 生成亮度感知的颗粒：暗部颗粒稍小（模拟真实胶片特性）
    luma = 0.2126 * img_linear[..., 0] + 0.7152 * img_linear[..., 1] + 0.0722 * img_linear[..., 2]
    grain_scale = 1.0 - 0.3 * luma  # 暗部颗粒稍强

    # 生成随机噪声（高斯分布，模拟真实颗粒）
    noise = np.random.normal(0, intensity, (h, w, 1)) * grain_scale[..., np.newaxis]

    # 叠加颗粒（加性叠加在线性空间）
    result = img_linear + noise
    return np.clip(result, 0.0, 1.0)


def add_light_leak(img_linear: np.ndarray, intensity: float = 0.2,
                   color: tuple = (1.0, 0.6, 0.2), position: str = "top_right") -> np.ndarray:
    """
    添加漏光效果（模拟胶片相机的光线泄漏）。
    
    intensity: 漏光强度，推荐 0.1 - 0.4
    color: 漏光颜色，默认橙黄色（模拟钨丝灯漏光）
    position: 漏光位置，可选 top_right / top_left / bottom_right / bottom_left
    """
    h, w, _ = img_linear.shape
    leak = np.zeros((h, w, 3), dtype=np.float32)

    # 建立渐变蒙版
    y_coords, x_coords = np.mgrid[0:h, 0:w]
    y_norm = y_coords / h
    x_norm = x_coords / w

    if position == "top_right":
        dist = np.sqrt((1 - x_norm) ** 2 + y_norm ** 2)
    elif position == "top_left":
        dist = np.sqrt(x_norm ** 2 + y_norm ** 2)
    elif position == "bottom_right":
        dist = np.sqrt((1 - x_norm) ** 2 + (1 - y_norm) ** 2)
    else:  # bottom_left
        dist = np.sqrt(x_norm ** 2 + (1 - y_norm) ** 2)

    # 创建柔和的辐射渐变
    mask = np.clip(1.0 - dist * 1.5, 0, 1) ** 2
    mask = mask[..., np.newaxis]

    # 叠加漏光颜色
    leak_color = np.array(color, dtype=np.float32)
    leak = mask * leak_color * intensity

    # 使用屏幕混合模式（Screen blend）—— 模拟光线叠加
    result = 1.0 - (1.0 - img_linear) * (1.0 - leak)
    return np.clip(result, 0.0, 1.0)


def add_vignette(img_linear: np.ndarray, strength: float = 0.3) -> np.ndarray:
    """添加暗角（边缘压暗，增加胶片感）"""
    h, w, _ = img_linear.shape
    y_coords, x_coords = np.mgrid[0:h, 0:w]
    y_norm = (y_coords / h - 0.5) * 2
    x_norm = (x_coords / w - 0.5) * 2
    dist = np.sqrt(x_norm ** 2 + y_norm ** 2)
    vignette = 1.0 - np.clip(dist * strength, 0, 1)
    return img_linear * vignette[..., np.newaxis]


# ─────────────────────────────────────────────
# 5. 主处理管线
# ─────────────────────────────────────────────

def process(input_path: str, lut_path: str, output_path: str,
            grain: float = 0.03, leak: float = 0.0,
            vignette: float = 0.0, preview: bool = False):
    """
    完整的色彩处理管线：
    sRGB 输入 → 线性空间 → 胶片颗粒 → LUT → 漏光/暗角 → sRGB 输出
    """

    # ── 读取图片
    print(f"📂 读取图片：{input_path}")
    img_pil = Image.open(input_path).convert("RGB")
    img_np = np.array(img_pil, dtype=np.float32)
    print(f"   尺寸：{img_pil.width} × {img_pil.height}")

    # ── 解析 LUT
    lut_array, lut_size, lut_type = parse_cube(lut_path)

    # ── 步骤 1：sRGB → 线性空间
    print("🔄 色彩空间转换：sRGB → 线性光空间")
    img_linear = srgb_to_linear(img_np)

    # ── 步骤 2：叠加胶片颗粒（在线性空间！）
    if grain > 0:
        print(f"🎞  添加胶片颗粒（强度：{grain}）")
        img_linear = add_film_grain(img_linear, intensity=grain)

    # ── 步骤 3：应用 LUT
    print(f"🎨 应用 {lut_type} LUT...")
    if lut_type == "3D":
        img_lut = apply_3d_lut(img_linear, lut_array, lut_size)
    else:
        img_lut = apply_1d_lut(img_linear, lut_array, lut_size)

    # ── 步骤 4：叠加漏光（LUT 之后）
    if leak > 0:
        print(f"✨ 添加漏光效果（强度：{leak}）")
        img_lut = add_light_leak(img_lut, intensity=leak)

    # ── 步骤 5：暗角
    if vignette > 0:
        print(f"🌑 添加暗角（强度：{vignette}）")
        img_lut = add_vignette(img_lut, strength=vignette)

    # ── 步骤 6：线性空间 → sRGB，准备输出
    print("🔄 色彩空间转换：线性光空间 → sRGB")
    img_out = linear_to_srgb(img_lut)
    img_out_uint8 = (img_out * 255).astype(np.uint8)
    result_pil = Image.fromarray(img_out_uint8)

    # ── 输出
    if preview:
        # 左右对比图
        print("🖼  生成对比预览图...")
        combined_width = img_pil.width * 2 + 10
        combined = Image.new("RGB", (combined_width, img_pil.height), (30, 30, 30))
        combined.paste(img_pil, (0, 0))
        combined.paste(result_pil, (img_pil.width + 10, 0))
        combined.save(output_path)
        print(f"✅ 对比图已保存：{output_path}")
        print(f"   左：原图  |  右：LUT 处理后")
    else:
        result_pil.save(output_path, quality=95)
        print(f"✅ 处理完成，已保存：{output_path}")


# ─────────────────────────────────────────────
# 6. CLI 入口
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="LUT 色彩管线验证脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 基础用法（只套 LUT）
  python lut_pipeline.py --input photo.jpg --lut film.cube --output result.jpg

  # 加颗粒和漏光
  python lut_pipeline.py --input photo.jpg --lut film.cube --grain 0.04 --leak 0.25 --output result.jpg

  # 生成左右对比图
  python lut_pipeline.py --input photo.jpg --lut film.cube --grain 0.03 --preview --output compare.jpg
        """
    )

    parser.add_argument("--input",    required=True,  help="输入图片路径（JPG/PNG）")
    parser.add_argument("--lut",      required=True,  help=".cube LUT 文件路径")
    parser.add_argument("--output",   required=True,  help="输出图片路径")
    parser.add_argument("--grain",    type=float, default=0.03,  help="胶片颗粒强度（默认 0.03，推荐 0.02-0.06）")
    parser.add_argument("--leak",     type=float, default=0.0,   help="漏光强度（默认 0，推荐 0.1-0.4）")
    parser.add_argument("--vignette", type=float, default=0.0,   help="暗角强度（默认 0，推荐 0.2-0.5）")
    parser.add_argument("--preview",  action="store_true",       help="生成左右对比图")

    args = parser.parse_args()

    try:
        process(
            input_path=args.input,
            lut_path=args.lut,
            output_path=args.output,
            grain=args.grain,
            leak=args.leak,
            vignette=args.vignette,
            preview=args.preview,
        )
    except FileNotFoundError as e:
        print(f"❌ 文件未找到：{e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 处理失败：{e}")
        raise


if __name__ == "__main__":
    main()
