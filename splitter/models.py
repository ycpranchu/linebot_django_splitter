from django.db import models

# Create your models here.
class Main_Database(models.Model):
    data_id = models.AutoField(primary_key=True)
    name_field = models.CharField(max_length=200, blank=True, null=False)
    cost_field = models.CharField(max_length=200, blank=True, null=False)
    time_field = models.DateTimeField(auto_now_add=True)


class Order_Data(models.Model):
    order_id = models.IntegerField(blank=True, null=False)
    Main_Database = models.ForeignKey(Main_Database, on_delete=models.CASCADE)


def makeList(textArray, startIndex):
    nameString, costString = "", ""
    for i in range(startIndex, len(textArray)):
        if i % 2 == startIndex % 2:
            if nameString == "":
                nameString += textArray[i]
            else:
                nameString += "/" + textArray[i]
        else:
            if costString == "":
                costString += textArray[i]
            else:
                costString += "/" + textArray[i]
    return nameString, costString


def splitList(item):
    nameArr = item.Main_Database.name_field.split('/')
    costArr = item.Main_Database.cost_field.split('/')
    textMessage = str(item.order_id) + ".\t" + nameArr[0] + costArr[0]
    for i in range(1, len(nameArr)):
        textMessage += " " + nameArr[i] + costArr[i]
    return textMessage
