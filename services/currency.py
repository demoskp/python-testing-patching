import requests
from requests import Response


class FXRateServiceException(Exception):
    pass


class FXRateService:
    BASE_URL = "https://api.currencylayer.com"

    def __init__(self, access_key):
        self._response = None
        self._access_key = access_key

    def historical(self, from_fx, to_fx, date):
        params = {"access_key": self._access_key, "source": from_fx, "currencies": to_fx, "date": date}
        response = requests.get(self.BASE_URL + "/convert", params=params)
        return self.extract_fx_rate_from_response(response)

    def current(self, from_fx, to_fx):
        params = {"access_key": self._access_key, "from": from_fx, "to": to_fx}
        response = requests.get(self.BASE_URL + "/convert", params=params)
        return self.extract_fx_rate_from_response(response)

    @staticmethod
    def extract_fx_rate_from_response(response: Response):
        if response.status_code != 200:
            raise FXRateServiceException("Request to fetch fx rate failed")

        data = response.json()
        success = data.get("success")

        if not success:
            error_info = data.get('error').get('info')
            raise FXRateServiceException(f"There was an error fetching the fx rate, {error_info}")

        return data.get("result")
