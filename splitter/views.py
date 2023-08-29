from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from splitter.models import *

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
import datetime

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                text = event.message.text
                uid = event.source.user_id
                textArray = text.split(' ')
                
                if len(textArray) <= 0 or textArray[0][0:2] != "ss":
                    return HttpResponse("do nothing")

                message = []
                if len(textArray) >= 1 and textArray[0] in ("ss"): # 所有指令
                    message.append(TextSendMessage(text='新增: sscreate/ssc {item} {name1} {cost1} {name2} {cost2}...\n \
                                                    列出: sslist/ssl\n \
	                                                修改: ssupdate/ssu {index} {item} {name1} {cost1} {name2} {cost2}...\n \
                                                    刪除: ssdelete/ssd {index}\n \
                                                    統計: sstotal/sst\n \
                                                    清空: ssclearclearclear'))

                elif len(textArray) >= 4 and textArray[0] in ("sscreate", "ssc"): # 新增
                    sig = True
                    for i in range(3, len(textArray)):
                        if i % 2 == 1:
                            try: int(textArray[i])
                            except:
                                message.append(TextSendMessage(text='指令錯誤，輸入 ss 查詢指令'))
                                sig = False
                                break
                    
                    if sig:
                        nameString, costString = makeList(textArray, 2)
                        d = Main_Database.objects.create(item_field=textArray[1], name_field=nameString, cost_field=costString)
                        dataArray = Order_Data.objects.all()
                        Order_Data.objects.create(order_id=len(dataArray)+1, Main_Database=d)
                        message.append(TextSendMessage(text='分帳資料新增完成'))
                    
                elif len(textArray) >= 1 and textArray[0] in ("sslist", "ssl"): # 列出
                    dataArray = Order_Data.objects.all()
                    textMessage = ""
                    for item in dataArray:
                        if textMessage == "":
                            textMessage += splitList(item)
                        else:
                            textMessage += '\n' + splitList(item)
                    message.append(TextSendMessage(text=textMessage))

                elif len(textArray) >= 5 and textArray[0] in ("ssupdate", "ssu"): # 修改
                    sig = True
                    for i in range(4, len(textArray)):
                        if i % 2 == 0:
                            try: int(textArray[i])
                            except:
                                message.append(TextSendMessage(text='指令錯誤，輸入 ss 查詢指令'))
                                sig = False
                                break
                    
                    if sig:
                        nameString, costString = makeList(textArray, 3)
                        data = Order_Data.objects.get(order_id=int(textArray[1]))
                        Main_Database.objects.filter(data_id=data.Main_Database.data_id).update(item_field=textArray[2], name_field=nameString, cost_field=costString)
                        message.append(TextSendMessage(text='分帳資料修改完成'))

                elif len(textArray) >= 2 and textArray[0] in ("ssdelete", "ssd"): # 刪除
                    data = Order_Data.objects.get(order_id=int(textArray[1]))
                    Main_Database.objects.filter(data_id=data.Main_Database.data_id).delete()
                    dataArray = Order_Data.objects.all()
                    
                    for item in dataArray:
                        if item.order_id > int(textArray[1]):
                            item.order_id -= 1
                            item.save()
                    message.append(TextSendMessage(text='第' + textArray[1] + '筆資料已刪除'))

                elif textArray[0] in ("sstotal", "sst"): # 統計
                    dataArray = Order_Data.objects.all()
                    if len(textArray) >= 3:
                        a, b = int(textArray[1]), int(textArray[2])
                        resultString = totalList(dataArray, a, b)
                    elif len(textArray) >= 2:
                        a = int(textArray[1])
                        resultString = totalList(dataArray, a)
                    else:
                        resultString = totalList(dataArray)
                    message.append(TextSendMessage(text='統計結果: \n\n' + resultString))

                elif len(textArray) >= 1 and textArray[0] in ("ssclearclearclear"): # 清空
                    Main_Database.objects.all().delete()
                    message.append(TextSendMessage(text='所有分帳資料已刪除'))
                    
                else:
                    message.append(TextSendMessage(text='指令錯誤，輸入 ss 查詢指令'))

                line_bot_api.reply_message(event.reply_token, message)

        return HttpResponse("success")
    else:
        return HttpResponseBadRequest()