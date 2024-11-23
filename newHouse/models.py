from django.db import models

# Create your models here.

# 建立楼栋模型
from django.db import models

from django.db import models


class Building(models.Model):
    # 自动增长的主键，默认情况下 Django 会自动创建一个 id 字段
    # 如果你需要自定义主键，可以如下定义：
    # id = models.AutoField(primary_key=True)

    # 建筑物ID
    buildingid = models.CharField(max_length=24, help_text="建筑物的标识符")

    # 网签数
    online_signatures = models.IntegerField(default=0, help_text="网签的数量")

    # 认购数
    subscriptions = models.IntegerField(default=0, help_text="认购的数量")

    # 现房数
    ready_houses = models.IntegerField(default=0, help_text="现房的数量")

    # 期房数
    future_houses = models.IntegerField(default=0, help_text="期房的数量")

    # 抵押数
    mortgages = models.IntegerField(default=0, help_text="抵押的数量")

    # 不可售数
    unsold_units = models.IntegerField(default=0, help_text="不可售的数量")

    # 项目名称
    project_name = models.CharField(max_length=100, help_text="项目名称")

    # 创建日期
    date_added = models.DateField(auto_now_add=True, help_text="记录创建的日期")

    def __str__(self):
        return f"Building {self.buildingid}: Online Signatures={self.online_signatures}, Subscriptions={self.subscriptions}, Ready Houses={self.ready_houses}, Future Houses={self.future_houses}, Mortgages={self.mortgages}, Unsold Units={self.unsold_units}, Date Added={self.date_added}, Project Name={self.project_name} "
