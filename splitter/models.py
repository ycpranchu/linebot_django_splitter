from django.db import models

# Create your models here.
class Main_Database(models.Model):
    data_id = models.AutoField(primary_key=True)
    item_field = models.CharField(max_length=200, blank=True, null=False)
    name_field = models.CharField(max_length=200, blank=True, null=False)
    cost_field = models.CharField(max_length=200, blank=True, null=False)
    time_field = models.DateTimeField(auto_now_add=True)


class Order_Data(models.Model):
    user_id = models.CharField(max_length=200, blank=True, null=False)
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
    nameArray = item.Main_Database.name_field.split('/')
    costArray = item.Main_Database.cost_field.split('/')
    textMessage = str(item.order_id) + ".\t" + item.Main_Database.item_field + " " + nameArray[0] + costArray[0]
    for i in range(1, len(nameArray)):
        textMessage += " " + nameArray[i] + costArray[i]
    return textMessage


def totalList(dataArray, a=1, b=-1):
    totalNameArray = []
    totalCostArray = []

    if b == -1: b = len(dataArray)
    for item in dataArray:
        if item.order_id >= a and item.order_id <= b:
            nameArray = item.Main_Database.name_field.split('/')
            costArray = item.Main_Database.cost_field.split('/')

            for i in range(0, len(nameArray)):
                if not nameArray[i] in totalNameArray:
                    totalNameArray.append(nameArray[i])
                    totalCostArray.append(int(costArray[i]))
                else:
                    k = totalNameArray.index(nameArray[i])
                    totalCostArray[k] += int(costArray[i])

    resultString = totalNameArray[0] + str(totalCostArray[0])
    for i in range(1, len(totalNameArray)):
        resultString += '\n' + totalNameArray[i] + str(totalCostArray[i])
    return resultString