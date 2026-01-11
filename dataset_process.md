### 1.将原始数据集合并

原始数据集经过 7:2:1 的比例进行划分，得到三个标记文件，现在首先需要把标记文件合并为一个，把图片数据也合并到一个文件夹下。

具体代码在文件 [merge_dataset.py](merge_dataset.py) 中

### 2.过滤数据集后导出

使用 fiftyone 这个工具来查看合并后的整体数据集，并进行标签过滤

读取数据集
```
import fiftyone as fo

dataset = fo.Dataset.from_dir(
    dataset_dir="/Users/lu/Code/dataset/CarDD_all",
    dataset_type=fo.types.COCODetectionDataset,
    data_path="data",
    labels_path="annotations/instances.json"
)
```

过滤数据集标签

```
from fiftyone import ViewField as F

labels = ["dent", "scratch", "crack"]

view = (
    dataset
    .filter_labels("detections",    F("label").is_in(labels))
    .filter_labels("segmentations", F("label").is_in(labels))
)
```

查看过滤后的数据集
过滤后剩余 3,099 张样本图片，过滤掉了约1000张图片

```
session = fo.launch_app(view)
```

导出为新的数据集

```
view.export(
    export_dir="/Users/lu/Code/dataset/CarDD_filtered",
    dataset_type=fo.types.COCODetectionDataset,
    label_field="segmentations"
)
```


### 3.重新拆分数据集

过滤后剩余 3,099 张样本图片，当然按照 train,test,val 70%, 20%, 10% 的比例进行拆分
训练集图片数: 2169
验证集图片数: 310
测试集图片数: 620

具体代码在 [split_dataset.py](split_dataset.py) 中  
最终得到的目录结构同原目录结构相同，只是数据已经经过了过滤。



