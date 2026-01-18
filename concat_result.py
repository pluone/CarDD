import cv2
import numpy as np
from pathlib import Path
import argparse

def load_images(dir_path, size=(300, 300), ext=('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
    """把目录下所有指定后缀的图片统一缩放后返回列表"""
    imgs = []
    for p in sorted(Path(dir_path).glob('*')):          # 按文件名排序
        if p.suffix.lower() in ext:
            img = cv2.imread(str(p))
            if img is None:                            # 读失败跳过
                print(f'Warning: skip unreadable file {p}')
                continue
            img = cv2.resize(img, size)
            imgs.append(img)
    if len(imgs) != 20:
        raise ValueError(f'Directory must contain exactly 20 images, got {len(imgs)}')
    return imgs

def build_montage(imgs, grid=(4, 5)):
    """把 20 张图按 grid 拼成一张大图"""
    h, w = imgs[0].shape[:2]
    big = np.zeros((h * grid[0], w * grid[1], 3), dtype=np.uint8)
    for idx, img in enumerate(imgs):
        r, c = divmod(idx, grid[1])
        big[r*h:(r+1)*h, c*w:(c+1)*w] = img
    return big

def main():
    parser = argparse.ArgumentParser(description='把 20 张图片拼成一张大图')
    parser.add_argument('img_dir', help='存放 20 张图片的目录')
    parser.add_argument('-o', '--out', default='montage.jpg', help='输出文件名（默认 montage.jpg）')
    parser.add_argument('-s', '--size', type=int, nargs=2, default=[300, 300], help='单张缩放宽高（默认 300 300）')
    parser.add_argument('-g', '--grid', type=int, nargs=2, default=[4, 5], help='行列数（默认 4 5）')
    parser.add_argument('--show', action='store_true', help='拼完后弹窗展示')
    args = parser.parse_args()

    imgs = load_images(args.img_dir, tuple(args.size))
    montage = build_montage(imgs, tuple(args.grid))
    cv2.imwrite(args.out, montage)
    print(f'Saved -> {args.out}  ({montage.shape[1]}x{montage.shape[0]})')

    if args.show:
        cv2.imshow('montage', montage)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
