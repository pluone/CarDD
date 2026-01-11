import json
import os
from tqdm import tqdm


def merge_coco_datasets(annotations_dir, output_file, subsets=None):
    """
    将多个COCO格式的子集（train, val, test）合并成一个完整的数据集。

    Args:
        annotations_dir (str): 存放各个子集标注文件的目录路径。
                               例如: /path/to/your/split_dataset/annotations/
        output_file (str): 合并后的完整标注文件的保存路径和文件名。
        subsets (list, optional): 需要合并的子集名称列表。
                                  例如: ['train', 'val', 'test']。
                                  如果为None，则会自动查找所有符合 `instances_*2017.json` 格式的文件。
    """
    # 如果没有指定子集，则自动发现
    if subsets is None:
        subsets = []
        for filename in os.listdir(annotations_dir):
            if filename.startswith('instances_') and filename.endswith('2017.json'):
                # 从文件名中提取子集名称，如 'train' 从 'instances_train2017.json'
                subset_name = filename.replace('instances_', '').replace('2017.json', '')
                subsets.append(subset_name)
        if not subsets:
            print(f"错误：在目录 '{annotations_dir}' 中没有找到任何COCO标注文件。")
            return

    print(f"发现并准备合并以下子集: {', '.join(subsets)}")

    # 用于存储合并后的数据
    merged_data = {
        'info': None,
        'licenses': None,
        'categories': None,
        'images': [],
        'annotations': []
    }

    # 用于重新编号标注ID
    next_annotation_id = 1

    for subset in subsets:
        ann_file = os.path.join(annotations_dir, f'instances_{subset}2017.json')
        print(f"\n正在处理子集: {subset} (文件: {ann_file})")

        if not os.path.exists(ann_file):
            print(f"警告：文件 '{ann_file}' 不存在，已跳过。")
            continue

        with open(ann_file, 'r') as f:
            subset_data = json.load(f)

        # 确保所有子集的元数据（info, licenses, categories）是一致的
        # 我们用第一个子集的元数据作为基准
        if merged_data['info'] is None:
            merged_data['info'] = subset_data.get('info', {})
            merged_data['licenses'] = subset_data.get('licenses', [])
            merged_data['categories'] = subset_data.get('categories', [])
        else:
            # 这里可以添加检查，确保所有子集的categories等信息一致
            pass

        # 合并图片信息
        num_images = len(subset_data['images'])
        merged_data['images'].extend(subset_data['images'])
        print(f"  - 已合并 {num_images} 张图片。")

        # 合并标注信息，并重新编号ID
        num_annotations = len(subset_data['annotations'])
        print(f"  - 正在处理 {num_annotations} 个标注 (将重新编号ID)...")
        for ann in tqdm(subset_data['annotations'], desc=f'Processing {subset} annotations'):
            # 创建一个新的标注字典，避免修改原始数据
            new_ann = ann.copy()
            # 分配新的全局唯一ID
            new_ann['id'] = next_annotation_id
            next_annotation_id += 1
            merged_data['annotations'].append(new_ann)

    print(f"\n合并完成！")
    print(f"总计合并图片数: {len(merged_data['images'])}")
    print(f"总计合并标注数: {len(merged_data['annotations'])}")

    # 保存合并后的文件
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(merged_data, f, indent=4)  # 使用indent=4让JSON文件更易读
    print(f"合并后的标注文件已保存至: {output_file}")


# --- 使用示例 ---
if __name__ == '__main__':
    # 请根据你的实际情况修改以下路径
    # 假设你的拆分后数据集结构如下：
    # /path/to/your/split_dataset/
    # ├── annotations/
    # │   ├── instances_train2017.json
    # │   ├── instances_val2017.json
    # │   └── instances_test2017.json
    # ├── train2017/
    # ├── val2017/
    # └── test2017/

    # 标注文件所在目录
    ANNOTATIONS_DIR = '/Users/lu/Code/dataset/CarDD_release/CarDD_COCO/annotations'
    # 合并后的文件保存路径
    OUTPUT_MERGED_FILE = '/Users/lu/Code/dataset/CarDD_release/CarDD_COCO/annotations/instances_merged.json'

    # 调用函数进行合并
    # 你可以明确指定要合并的子集，例如 ['train', 'val']
    # 如果不指定，脚本会自动查找所有符合格式的文件
    merge_coco_datasets(
        annotations_dir=ANNOTATIONS_DIR,
        output_file=OUTPUT_MERGED_FILE
        # subsets=['train', 'val', 'test'] # 可选参数
    )
