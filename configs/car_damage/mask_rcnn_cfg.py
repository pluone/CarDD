# The new config inherits a base config to highlight the necessary modification
# _base_ = '/root/autodl-nas/code/ODIS/CarDD_detection/configs/mask_rcnn/mask_rcnn_r50_fpn_1x_coco.py'
# _base_ = '../mask_rcnn/mask-rcnn_r50_fpn_2x_coco.py'
_base_ = '../mask_rcnn/mask-rcnn_r50_fpn_1x_coco.py'
# _base_ = '/root/autodl-nas/code/ODIS/CarDD_detection/configs/mask_rcnn/mask_rcnn_r101_fpn_1x_coco.py'
# _base_ = '/root/autodl-nas/code/ODIS/CarDD_detection/configs/mask_rcnn/mask_rcnn_r101_fpn_2x_coco.py'

# lr_config = dict(step=[16, 22])
train_cfg = dict(
    type='EpochBasedTrainLoop',  # The training loop type. Refer to https://github.com/open-mmlab/mmengine/blob/main/mmengine/runner/loops.py
    max_epochs=12,  # Maximum training epochs
    val_interval=1)  # Validation intervals. Run validation every epoch.

runner = dict(type='EpochBasedRunner', max_epochs=12)

checkpoint_config = dict(create_symlink=False)
# We also need to change the num_classes in head to match the dataset's annotation
model = dict(
    roi_head=dict(
        bbox_head=dict(num_classes=3),
        mask_head=dict(num_classes=3)))

# Modify dataset related settings
dataset_type = 'COCODataset'
classes = ('dent', 'scratch', 'crack')
data_root = '/root/onethingai-tmp/CarDD_dataset/'

metainfo = {
    'classes': ('dent', 'scratch', 'crack'),
}
train_dataloader = dict(
    batch_size=8,  # 单个 GPU 的 batch size
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

# optimizer = dict(lr=0.01)  # LR
# evaluation = dict(interval=4) 


# We can use the pre-trained Mask RCNN model to obtain higher performance
# load_from = '/root/autodl-nas/model/pretrained/mask_rcnn_r50_fpn_1x_coco_20200205-d4b0c5d6.pth'
load_from = 'https://download.openmmlab.com/mmdetection/v2.0/mask_rcnn/mask_rcnn_r50_fpn_2x_coco/mask_rcnn_r50_fpn_2x_coco_bbox_mAP-0.392__segm_mAP-0.354_20200505_003907-3e542a40.pth'
# load_from = '/root/autodl-nas/model/pretrained/mask_rcnn_r101_fpn_1x_coco_20200204-1efe0ed5.pth'
# load_from = '/root/autodl-nas/model/pretrained/mask_rcnn_r101_fpn_2x_coco_bbox_mAP-0.408__segm_mAP-0.366_20200505_071027-14b391c7.pth'
