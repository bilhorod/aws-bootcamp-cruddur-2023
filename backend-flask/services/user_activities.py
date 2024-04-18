from datetime import datetime, timedelta, timezone
from aws_xray_sdk.core import xray_recorder 

class UserActivities:
    def run(self, user_handle):
        try:
            model = {
                'errors': None,
                'data': None
            }

            now = datetime.now(timezone.utc).astimezone()

            if user_handle is None or len(user_handle) < 1:
                model['errors'] = ['blank_user_handle']
            else:
                now = datetime.now()
                results = [{
                    'uuid': '248959df-3079-4947-b847-9e0892d1bab4',
                    'handle': 'Andrew Brown',
                    'message': 'Cloud is very fun!',
                    'created_at': (now - timedelta(days=1)).isoformat(),
                    'expires_at': (now + timedelta(days=31)).isoformat()
                }]
                model['data'] = results

            subsegment = xray_recorder.begin_subsegment('mock-data')
            
            # XRAY
            metadata_dict = {
                "now": now.isoformat(),
                "results-size": len(model['data'])
            }
            subsegment.put_metadata('key', metadata_dict, "namespace")
            xray_recorder.end_subsegment()
            
        finally:
            # close the segment
            xray_recorder.end_subsegment()

        return model
