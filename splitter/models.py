from django.db import models

# Create your models here.
class Main_Database(models.Model):
    data_id = models.AutoField(primary_key=True)
    name_field = models.CharField(max_length=200, blank=True, null=False)
    cost_field = models.CharField(max_length=200, blank=True, null=False)
    time_field = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.data_id + " " + self.name_field + " " + self.cost_field + " " + self.time_field
    

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
    nameArr = item.name_field.split('/')
    costArr = item.cost_field.split('/')
    textMessage = str(item.data_id) + ". " + nameArr[0] + costArr[0]
    for i in range(1, len(nameArr)):
        textMessage += " " + nameArr[i] + costArr[i]
    return textMessage
