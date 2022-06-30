"""[summary]

[description]
"""
import hashlib
import json
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class BaseConsumer(AsyncJsonWebsocketConsumer):
    canal = ""
    grupo = ""
    modeloid = ""
    lastContents = {}

    @property
    def nome_do_grupo(self):
        return "%s-%s-%s" % (self.canal, self.grupo, self.modeloid)

    @property
    def groupID(self):
        return hashlib.md5(self.nome_do_grupo.encode("utf-8")).hexdigest()

    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            if "canal" in self.scope["url_route"]["kwargs"]:
                self.canal = self.scope["url_route"]["kwargs"]["canal"]

            if "grupo" in self.scope["url_route"]["kwargs"]:
                self.grupo = self.scope["url_route"]["kwargs"]["grupo"]

            if "modeloid" in self.scope["url_route"]["kwargs"]:
                self.modeloid = self.scope["url_route"]["kwargs"]["modeloid"]

            await self.channel_layer.group_add(self.nome_do_grupo, self.channel_name)
            if self.groupID in self.lastContents.keys():
                await self.channel_layer.group_send(
                    self.nome_do_grupo,
                    {"type": "group_message", "content": self.lastContents[self.groupID]},
                )            
            await self.accept()
        else:
            await self.close()
