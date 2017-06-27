import dateutil.parser
import json

from datetime import datetime


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return {"val": o.timestamp(), "_spec_type": "datetime"}

        return super().default(self, o)

class DateTimeDecoder:
    @staticmethod
    def decode(obj):
        date_recorded = obj.get('date_recorded')

        if not date_recorded:
            return obj

        if 'date_recorded' in obj.keys():
            obj['date_recorded'] = datetime.fromtimestamp(obj['date_recorded'])
        else:
            raise Exception('Unknown {}'.format(date_recorded))

        return obj
