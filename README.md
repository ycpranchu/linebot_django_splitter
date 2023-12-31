Linebot + Django 分帳小工具 Splitter 實作
===

- targets：Linebot + Django framework, Splitter tool implementation.

Splitter 指令
---

1. 查詢指令：ss

2. 新增：sscreate/ssc {item} {name1} {cost1} {name2} {cost2}...

3. 列出：sslist/ssl

4. 修改：ssupdate/ssu {index} {item} {name1} {cost1} {name2} {cost2}...

5. 刪除：ssdelete/ssd {index}

6. 統計：sstotal/sst

7. 清空：ssclearclearclear

資料庫規劃
---

#### Main_Database

data_id | item_field | name_field | cost_field | time_field
| --- | --- | --- | --- | --- |
| Primary Key | CharField | CharField | CharField | DateTimeField |

#### Order_Data

group_id | order_id | Main_Database
| --- | --- | --- |
| CharField | IntegerField | Foreign Key |

### Foreign Key

Link `Order_Data.order_id` to `Main_Database.data_id`

```python3
class Main_Database(models.Model):
    data_id = models.AutoField(primary_key=True)
    item_field = models.CharField(max_length=200, blank=True, null=False)
    name_field = models.CharField(max_length=200, blank=True, null=False)
    cost_field = models.CharField(max_length=200, blank=True, null=False)
    time_field = models.DateTimeField(auto_now_add=True)

class Order_Data(models.Model):
    order_id = models.IntegerField(blank=True, null=False)
    Main_Database = models.ForeignKey(Main_Database, on_delete=models.CASCADE)
```