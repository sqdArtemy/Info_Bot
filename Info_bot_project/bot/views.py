from rest_framework.views import APIView
import os
from django.http import JsonResponse
from Info_bot_project.settings import TOKEN, URL
from telegram.ext import Updater, Dispatcher
from telegram import *
from telegram.ext import *
from bot.bot import conversation_handler
import pytz


class BotView(APIView):
    def get(self, request, *args, **options):
        try:
            PORT = int(os.environ.get('PORT', '8000'))
            bot = Bot(token=TOKEN)
            defaults = Defaults(parse_mode=ParseMode.MARKDOWN, tzinfo=pytz.timezone('Asia/Tashkent'))
            updater = Updater(bot=bot, use_context=True, defaults=defaults)

            bot.setWebhook(URL + 'info_bot/')
            updater.start_webhook(listen='0.0.0.0',
                            port=PORT,
                            url_path=TOKEN,
                            webhook_url=(URL+'info_bot/')
            )
            return JsonResponse({"ok": "Webhook set successfully"})
        except:
            return JsonResponse({"err": "Webhook was not set, something went wrong"}) 

    def post(self, request, *args, **options):
        try:
            bot = Bot(token=TOKEN)
            dispatcher = Dispatcher(bot, None, workers=8)
            dispatcher.add_handler(conversation_handler)
            dispatcher.process_update(Update.de_json(request.data, bot))
            return JsonResponse({"ok": "POST request processed"})
        except:
            raise JsonResponse({"err": "Something went wrong, request was not proceed "}) 

# go to http://127.0.0.1:8000/info_bot/ in order to set webhook
