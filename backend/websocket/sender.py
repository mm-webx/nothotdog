import json

from channels import Group
from django.core.serializers.json import DjangoJSONEncoder


class WebSocketSender(object):

    def __init__(self, group):
        self.group = group

    def send(self, action, data):
        json_data = dict(
            action=action,
            data=data
        )

        Group(self.group).send({
            'text': json.dumps(json_data, cls=DjangoJSONEncoder),
        })
