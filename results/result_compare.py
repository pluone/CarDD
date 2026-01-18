import json
import matplotlib.pyplot as plt
import pandas as pd

# 加载数据
def load_scalars(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            data.append(json.loads(line.strip()))
    return pd.DataFrame(data)

# 加载两个文件（替换为实际路径）
maskrcnn_df = load_scalars("./results/maskrcnn_scalars.json")
dcn_df = load_scalars("./results/dcn_scalars.json")

# 1. 绘制bbox_mAP趋势
plt.figure(figsize=(12, 6))
# 提取有mAP的行
maskrcnn_map = maskrcnn_df[maskrcnn_df['coco/bbox_mAP'].notna()]['coco/bbox_mAP']
dcn_map = dcn_df[dcn_df['coco/bbox_mAP'].notna()]['coco/bbox_mAP']
# 步骤数
maskrcnn_steps = maskrcnn_df[maskrcnn_df['coco/bbox_mAP'].notna()]['step']
dcn_steps = dcn_df[dcn_df['coco/bbox_mAP'].notna()]['step']

plt.plot(maskrcnn_steps, maskrcnn_map, label='Mask R-CNN', marker='o', linewidth=2)
plt.plot(dcn_steps, dcn_map, label='Mask R-CNN+DCN', marker='s', linewidth=2)
plt.xlabel('Step')
plt.ylabel('bbox_mAP@0.5:0.95')
plt.title('bbox_mAP Trend Comparison')
plt.legend()
plt.grid(True)
plt.savefig('map_trend.png')


# 2. 新增：绘制bbox_mAP_50趋势（IoU=0.5）
plt.figure(figsize=(12, 6))
# 提取有mAP_50的行（注意字段名需和json文件中一致，若不同请替换）
# 常见字段名：coco/bbox_mAP_50 或 bbox_mAP_50
maskrcnn_map50 = maskrcnn_df[maskrcnn_df['coco/bbox_mAP_50'].notna()]['coco/bbox_mAP_50']
dcn_map50 = dcn_df[dcn_df['coco/bbox_mAP_50'].notna()]['coco/bbox_mAP_50']
# 步骤数
maskrcnn_steps50 = maskrcnn_df[maskrcnn_df['coco/bbox_mAP_50'].notna()]['step']
dcn_steps50 = dcn_df[dcn_df['coco/bbox_mAP_50'].notna()]['step']

plt.plot(maskrcnn_steps50, maskrcnn_map50, label='Mask R-CNN', marker='^', linewidth=2, color='orange')
plt.plot(dcn_steps50, dcn_map50, label='Mask R-CNN+DCN', marker='*', linewidth=2, color='green')
plt.xlabel('Step')
plt.ylabel('bbox_mAP@0.5 (mAP_50)')
plt.title('Mask R-CNN vs DCN IoU=0.5 Trend Comparison')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('map50_trend.png', dpi=150, bbox_inches='tight')
plt.close()



# 2. 绘制损失趋势
plt.figure(figsize=(12, 6))
# 提取迭代数和损失
maskrcnn_iter = maskrcnn_df[maskrcnn_df['loss'].notna()]['iter']
maskrcnn_loss = maskrcnn_df[maskrcnn_df['loss'].notna()]['loss']
dcn_iter = dcn_df[dcn_df['loss'].notna()]['iter']
dcn_loss = dcn_df[dcn_df['loss'].notna()]['loss']

plt.plot(maskrcnn_iter[:20], maskrcnn_loss[:20], label='Mask R-CNN', linewidth=2)  # 取前20个迭代对比
plt.plot(dcn_iter[:20], dcn_loss[:20], label='Mask R-CNN+DCN', linewidth=2)
plt.xlabel('Iteration')
plt.ylabel('Total Loss')
plt.title('Training Loss Trend (Early Stage)')
plt.legend()
plt.grid(True)
plt.savefig('loss_trend.png')





