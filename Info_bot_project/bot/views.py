from rest_framework.views import APIView
import os
from django.http import JsonResponse
from telegram.ext import Updater, Dispatcher
from telegram import *
from .handlers import conversation_handler
from django.conf import settings


class BotView(APIView):

    def get(self, request, *args, **options):
        try:
            PORT = int(os.environ.get('PORT', '8000'))
            bot = Bot(token=settings.TOKEN)
            updater = Updater(bot=bot, use_context=True)

            bot.setWebhook(settings.URL + 'info_bot/')
            updater.start_webhook(
                listen='0.0.0.0',
                port=PORT,
                url_path=settings.TOKEN,
                webhook_url=(settings.URL+'info_bot/')
            )
            return JsonResponse({"ok": "Webhook set successfully"})
        except:
            return JsonResponse({"err": "Webhook was not set, something went wrong"}) 

    def post(self, request, *args, **options):
        try:
            bot = Bot(token=settings.TOKEN)
            dispatcher = Dispatcher(bot, None, workers=8)
            dispatcher.add_handler(conversation_handler)
            dispatcher.process_update(Update.de_json(request.data, bot))
            return JsonResponse({"ok": "POST request processed"})
        except:
            raise JsonResponse({"err": "Something went wrong, request was not proceed "}) 

# go to http://127.0.0.1:8000/info_bot/ in order to set webhook
