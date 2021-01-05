from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.conf import settings
import logging
import json

import minecraft.controllers.aws_interface as aws_interface
from django.views.decorators.csrf import csrf_exempt

CONFIG = settings.CONFIG
logger = logging.getLogger(__name__)
isServerRunning = False
serverInfo = {}
password = CONFIG['password']

def startServer(request):
    if request.method == 'POST':

        global isServerRunning
        global serverInfo
        try:
            request_body = json.loads(request.body)
            if 'password' not in request_body or request_body['password'] != password:
                return JsonResponse({"success" : False,
                                        "message" : "Passowrd is incorrect"})
        except:
            return JsonResponse({"success" : False,
                                    "message" : "Internal server error. Please contact admin.",
                                    "received-body" : request_body})
        logging.debug(isServerRunning)
        serverInfo = aws_interface.startServer(request_body["server_id"])
        # handle server not found
        print(serverInfo)
        isServerRunning = True
        return JsonResponse({"success" : True,
                                "message" : "Server is starting. Hang tight..."})
    return JsonResponse({"success" : False,
                                "message" : "API recieved GET call to start-server."})

def stopServer(request):
    global isServerRunning
    isServerRunning = False
    if not serverInfo["publicIp"] == "Success": # Assumes publicIp is set
        aws_interface.stopServer(serverInfo)

    return JsonResponse({"success" : True,
                                "message" : "Server is shutting down..."})

def getServerStatus(request):
    data = {
        "isRunning" : isServerRunning
    }
    if isServerRunning:
        data['ipAdress'] = serverInfo['publicIp']

    return JsonResponse(data)

def getServerList(request):
    servers = aws_interface.getServerList()
    return JsonResponse( {"servers" : servers} )

@csrf_exempt
def qa_startServer(request):
    if request.method == 'POST':

        global isServerRunning
        global serverInfo
        try:
            request_body = json.loads(request.body)
            if 'password' not in request_body or request_body['password'] != password:
                return JsonResponse({"success" : False,
                                        "message" : "Passowrd is incorrect"})
        except:
            return JsonResponse({"success" : False,
                                    "message" : "Internal server error. Please contact admin.",
                                    "received-body" : request_body})
        logging.debug(isServerRunning)
        serverInfo = aws_interface.startServer(request_body["server_id"], True)
        # handle server not found
        print(serverInfo)
        isServerRunning = True
        return JsonResponse({"success" : True,
                                "message" : "Server is starting. Hang tight..."})
    return JsonResponse({"success" : False,
                                "message" : "API recieved GET call to start-server."})