import logging

from django.http import Http404, HttpResponse, JsonResponse
from django.template import loader
from markdown2 import markdown

from .models import Message, Response
from .utils.langchainGptApi import getResponseFromApi

log = logging.getLogger(__name__)


def index(request):
    latest_messages_list = Message.objects.order_by("pub_date")

    # Markdown for pretty text :3
    for message in latest_messages_list:
        message.message_text = markdown(message.message_text)

        mdResponses = []
        for response in message.responses.all():
            mdResponse = {
                "original_text": response.response_text,
                "markdown_text": markdown(response.response_text),
            }
            mdResponses.append(mdResponse)

        message.mdResponses = mdResponses

    template = loader.get_template("index.html")
    context = {
        "latest_messages_list": latest_messages_list,
    }
    return HttpResponse(template.render(context, request))


def sendMessage(request):
    # This is only for parsing the message the user sents in real-time
    return JsonResponse({"sucess": True, "markdown_text": markdown(request.POST["message"])})


def receiveResponse(request):
    if request.method == "POST":
        file = request.FILES.get("file")
        responseText = ""

        log.info(f'sent message: {request.POST['message']}')
        log.info(f'file sent? {'True' if file else 'False'}')

        if not request.POST["message"]:
            log.error("EMPTY MESSAGE!")
            raise Http404("EMPTY MESSAGE!")

        try:
            message = Message(
                message_text=request.POST["message"],
            )
            message.save()

            # reminder that this DOES NOT keep the context of the main conversation,
            # working on that later, as well Markdown linting support
            data = getResponseFromApi(request.POST["message"])
            responseText = data["response_text"]

            response = Response(
                question=message,
                response_text=data["response_text"],
                completion_tokens=data["completion_tokens"],
                prompt_tokens=data["prompt_tokens"],
                total_price=data["total_price"],
                attached_file=file,
            )
            response.save()

        except Exception as e:
            log.error(f"ERROR: {e}")

        return JsonResponse(
            {
                "sucess": True,
                "message_text": markdown(responseText),
            }
        )

    raise Http404("Error while sending the message.")
