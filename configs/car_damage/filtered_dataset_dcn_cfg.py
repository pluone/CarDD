# The new config inherits a base config to highlight the necessary modification
# _base_ = '/root/autodl-nas/code/ODIS/CarDD_detection/configs/dcn/mask_rcnn_r50_fpn_dconv_c3-c5_1x_coco.py'

# _base_ = '../dcn/mask-rcnn_r101-dconv-c3-c5_fpn_1x_coco.py'
_base_ = '../dcn/mask-rcnn_r50-dconv-c3-c5_fpn_1x_coco.py'
# _base_ = '/root/autodl-nas/code/ODIS/CarDD_detection/configs/dcn/cascade_mask_rcnn_x101_32x4d_fpn_dconv_c3-c5_1x_coco.py'

train_cfg = dict(
    type='EpochBasedTrainLoop',  # The training loop type. Refer to https://github.com/open-mmlab/mmengine/blob/main/mmengine/runner/loops.py
    max_epochs=12,  # Maximum training epochs
    val_interval=1)  # Validation intervals. Run validation every epoch.

checkpoint_config = dict(create_symlink=False)
classes = ('dent', 'scratch', 'crack')
n_classes = len(classes)

# We also need to change the num_classes in head to match the dataset's annotation
model = dict(
    roi_head=dict(
        bbox_head=dict(num_classes=n_classes),
        mask_head=dict(num_classes=n_classes)))

# Modify dataset related settings
dataset_type = 'COCODataset'
data_root = '/root/onethingai-tmp/data/CarDD_filtered/'

metainfo = {
    'classes': ('dent', 'scratch', 'crack'),
}
train_dataloader = dict(
    batch_size=12,  # 单个 GPU 的 batch size
    num_workers=2,  # 单个 GPU 分配的数据加载线程数
    dataset=dict(
        data_root=data_root,
        metainfo=metainfo,
        ann_file='annotations/instances_train2017.json',
        data_prefix=dict(img='train2017/'),
        filter_cfg=dict(filter_empty_gt=True),
    ))
val_dataloader = dict(
    dataset=dict(
        data_root=data_root,
        metainfo=metainfo,
        ann_file='annotations/instances_val2017.json',
        data_prefix=dict(img='val2017/')))
test_dataloader = dict(
    dataset=dict(
        data_root=data_root,
        metainfo=metainfo,
        ann_file='annotations/instances_test2017.json',
        data_prefix=dict(img='test2017/')))

# 修改评价指标相关配置
val_evaluator = dict(ann_file=data_root + 'annotations/instances_val2017.json')
test_evaluator = dict(ann_file=data_root + 'annotations/instances_test2017.json')

# We can use the pre-trained Mask RCNN model to obtain higher performance
# load_from = '/root/autodl-nas/model/pretrained/mask_rcnn_r50_fpn_dconv_c3-c5_1x_coco_20200203-4d9ad43b.pth'
# load_from = 'https://download.openmmlab.com/mmdetection/v2.0/dcn/mask_rcnn_r101_fpn_dconv_c3-c5_1x_coco/mask_rcnn_r101_fpn_dconv_c3-c5_1x_coco_20200216-a71f5bce.pth'
# 上面是 r101, 下面 r50
load_from = 'https://download.openmmlab.com/mmdetection/v2.0/dcn/mask_rcnn_r50_fpn_dconv_c3-c5_1x_coco/mask_rcnn_r50_fpn_dconv_c3-c5_1x_coco_20200203-4d9ad43b.pth'
# load_from = '/root/autodl-nas/model/pretrained/cascade_mask_rcnn_x101_32x4d_fpn_dconv_c3-c5_1x_coco-e75f90c8.pth'
