import json
import os
import shutil
from tqdm import tqdm
from pycocotools.coco import COCO


def split_coco_dataset(images_dir, annotations_file, output_dir, train_ratio=0.8, val_ratio=0.1):
    """
    将COCO格式的数据集拆分为训练集、验证集和测试集。

    Args:
        images_dir (str): 原始图片所在目录的路径。
        annotations_file (str): 原始COCO标注文件(.json)的路径。
        output_dir (str): 输出目录，用于存放拆分后的数据集。
        train_ratio (float): 训练集所占比例 (默认: 0.8)。
        val_ratio (float): 验证集所占比例 (默认: 0.1)。
                          测试集比例将为 1 - train_ratio - val_ratio。
    """
    # 检查参数
    assert train_ratio + val_ratio <= 1.0, "训练集和验证集的比例之和不能超过1.0"
    test_ratio = 1.0 - train_ratio - val_ratio

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    train_images_dir = os.path.join(output_dir, 'train2017')
    val_images_dir = os.path.join(output_dir, 'val2017')
    test_images_dir = os.path.join(output_dir, 'test2017')
    annotations_output_dir = os.path.join(output_dir, 'annotations')

    for dir_path in [train_images_dir, val_images_dir, test_images_dir, annotations_output_dir]:
        os.makedirs(dir_path, exist_ok=True)

    # 加载COCO标注
    print(f"加载标注文件: {annotations_file}")
    coco = COCO(annotations_file)
    with open(annotations_file, 'r') as f:
        coco_data = json.load(f)

    # 获取所有图片ID并打乱
    img_ids = coco.getImgIds()
    # np.random.seed(42) # 为了结果可复现，可以设置一个随机种子
    # np.random.shuffle(img_ids)

    total_imgs = len(img_ids)
    train_split = int(total_imgs * train_ratio)
    val_split = int(total_imgs * (train_ratio + val_ratio))

    train_img_ids = img_ids[:train_split]
    val_img_ids = img_ids[train_split:val_split]
    test_img_ids = img_ids[val_split:]

    print(f"数据集拆分完成:")
    print(f"训练集图片数: {len(train_img_ids)}")
    print(f"验证集图片数: {len(val_img_ids)}")
    print(f"测试集图片数: {len(test_img_ids)}")

    # 定义一个函数来创建子数据集
    def create_subset(img_ids, subset_name, subset_images_dir):
        print(f"\n正在创建 {subset_name} 子集...")

        # 筛选图片信息
        subset_imgs = [img for img in coco_data['images'] if img['id'] in img_ids]

        # 筛选标注信息
        subset_ann_ids = coco.getAnnIds(imgIds=img_ids)
        subset_anns = coco.loadAnns(subset_ann_ids)

        # 构建新的COCO JSON对象
        subset_coco = {
            'info': coco_data['info'],
            'licenses': coco_data['licenses'],
            'categories': coco_data['categories'],
            'images': subset_imgs,
            'annotations': subset_anns
        }

        # 保存标注文件
        output_ann_file = os.path.join(annotations_output_dir, f'instances_{subset_name}2017.json')
        with open(output_ann_file, 'w') as f:
            json.dump(subset_coco, f)
        print(f"  标注文件已保存至: {output_ann_file}")

        # 复制图片文件
        print(f"  正在复制 {subset_name} 图片...")
        for img in tqdm(subset_imgs, desc=f'Copying {subset_name} images'):
            src_img_path = os.path.join(images_dir, img['file_name'])
            dst_img_path = os.path.join(subset_images_dir, img['file_name'])
            shutil.copy2(src_img_path, dst_img_path)  # 使用copy2保留元数据

        print(f"{subset_name} 子集创建完毕。")

    # 执行创建
    create_subset(train_img_ids, 'train', train_images_dir)
    create_subset(val_img_ids, 'val', val_images_dir)
    if test_ratio > 0:
        create_subset(test_img_ids, 'test', test_images_dir)

    print("\n所有子集创建完毕！")


# --- 使用示例 ---
if __name__ == '__main__':
    # 请根据你的实际情况修改以下路径
    # 假设你的数据集结构如下：
    # /path/to/your/dataset/
    # ├── images/
    # │   ├── 000000000001.jpg
    # │   ├── 000000000002.jpg
    # │   └── ...
    # └── annotations/
    #     └── instances_default.json

    SOURCE_IMAGES_DIR = '/Users/lu/Code/dataset/CarDD_filtered/data'
    SOURCE_ANNOTATIONS_FILE = '/Users/lu/Code/dataset/CarDD_filtered/labels.json'
    OUTPUT_DIR = '/Users/lu/Code/dataset/CarDD_filtered_split'

    # 调用函数进行拆分
    split_coco_dataset(
        images_dir=SOURCE_IMAGES_DIR,
        annotations_file=SOURCE_ANNOTATIONS_FILE,
        output_dir=OUTPUT_DIR,
        train_ratio=0.7,  # 80% 训练集
        val_ratio=0.1  # 10% 验证集
        # 剩余 10% 为测试集
    )
