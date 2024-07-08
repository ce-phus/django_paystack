from django.conf import settings
import requests
import logging

class Paystack:
    PAYSTACK_SK = settings.PAYSTACK_SECRET_KEY
    base_url = "https://api.paystack.co/"

    def verify_payment(self, ref, *args, **kwargs):
        path = f'transaction{ref}'
        headers = {
            "Authorization": f"Bearer {self.PAYSTACK_SK}",
            "Content-Type": "application/json",
        }

        url = self.base_url + path
        response = requests.get(url, headers=headers)

        try:
            response_data = response.json()
            if response.status_code == 200:
                return response_data['status'], response_data['data']
            else:
                logging.error(f"Error from Paystack API: {response_data}")
            return False, response_data.get('message', 'Unknown error')
        except requests.exceptions.JSONDecodeError as e:
            logging.error(f"JSONDecodeError: {e}")
            return False, 'Invalid response from Paystack API'
