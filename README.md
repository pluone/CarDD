### CarDD 数据集介绍

该数据集主要用于进行车损评估。

损伤类型：dent, scratch, crack, glass shatter, tire flat, and lamp broken
凹陷、划痕、裂纹、玻璃破碎、轮胎、大灯损坏

目录结构
```
CarDD_COCO
	annotations
		instances_test2017.json
		instances_train2017.json
		instances_val2017.json
	train2017 包含2816张图片
	test2017 包含374张图片
	val2017 包含810张图片
```

总计 4000张图片，810/4000=20% 2816/4000=70%  
训练集、测试集、验证集的比例是7:1:2

### 将CarDD数据集的6个类别减少为3个类别

6个类别分别是  
('dent', 'scratch', 'crack', 'glass shatter', 'lamp broken', 'tire flat')  
分表代表 凹陷、划痕、开裂、玻璃碎裂、灯泡损坏、轮胎压坏  
由于这里只关心前3个类别，因此只保留前3个类别，分别是  
('dent', 'scratch', 'crack')  

具体做法参考 [数据集减少类别](dataset_process.md)

### 基础环境安装

参考 [安装环境](env_setup.md)

