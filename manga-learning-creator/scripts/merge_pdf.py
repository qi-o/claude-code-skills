#!/usr/bin/env python3
"""
漫画 PDF 合并脚本
将多张漫画页面图片合并为单个 PDF 文件
"""

import argparse
import sys

# 配置 UTF-8 输出（解决 Windows GBK 编码问题）
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
        sys.stderr.reconfigure(encoding='utf-8', errors='backslashreplace')
except (AttributeError, Exception):
    pass

from pathlib import Path

def merge_images_to_pdf(input_dir: str, output_file: str, pattern: str = "manga_page_*.png"):
    """
    将图片合并为 PDF

    Args:
        input_dir: 输入目录
        output_file: 输出 PDF 文件路径
        pattern: 文件匹配模式
    """
    try:
        from PIL import Image
    except ImportError:
        print("❌ 请先安装 Pillow: pip install Pillow")
        sys.exit(1)

    input_path = Path(input_dir)
    output_path = Path(output_file)

    # 确保输出目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 查找所有匹配的图片文件
    image_files = sorted(input_path.glob(pattern))

    if not image_files:
        print(f"❌ 在 {input_dir} 中未找到匹配 '{pattern}' 的图片文件")
        sys.exit(1)

    print(f"📚 找到 {len(image_files)} 张图片")

    # 加载所有图片
    images = []
    for img_file in image_files:
        print(f"  📷 加载: {img_file.name}")
        img = Image.open(img_file)
        # 转换为 RGB 模式（PDF 不支持 RGBA）
        if img.mode == 'RGBA':
            # 创建白色背景
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        images.append(img)

    if not images:
        print("❌ 没有可用的图片")
        sys.exit(1)

    # 保存为 PDF
    print(f"\n📄 正在生成 PDF: {output_file}")

    # 第一张图片作为基础，其余追加
    first_image = images[0]
    other_images = images[1:] if len(images) > 1 else []

    first_image.save(
        output_path,
        "PDF",
        resolution=300.0,
        save_all=True,
        append_images=other_images
    )

    print(f"✅ PDF 生成成功: {output_path}")
    print(f"   共 {len(images)} 页")

    return str(output_path)


def main():
    parser = argparse.ArgumentParser(
        description="将漫画页面图片合并为 PDF",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python merge_pdf.py --input ./pages --output ./output/manga.pdf
  python merge_pdf.py -i ./pages -o ./manga.pdf --pattern "page_*.png"
        """
    )

    parser.add_argument(
        "-i", "--input",
        required=True,
        help="输入图片目录"
    )

    parser.add_argument(
        "-o", "--output",
        required=True,
        help="输出 PDF 文件路径"
    )

    parser.add_argument(
        "-p", "--pattern",
        default="manga_page_*.png",
        help="图片文件匹配模式 (默认: manga_page_*.png)"
    )

    args = parser.parse_args()

    merge_images_to_pdf(args.input, args.output, args.pattern)


if __name__ == "__main__":
    main()
