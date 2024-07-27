import unittest
from unittest.mock import patch

import pytest

from services.currency import FXRateService, FXRateServiceException


class TestFXRateService(unittest.TestCase):
    def setUp(self):
        self.fx_response = {
            "success": True,
            "terms": "https://currencylayer.com/terms",
            "privacy": "https://currencylayer.com/privacy",
            "query": {
                "from": "USD",
                "to": "GBP",
                "amount": 10
            },
            "info": {
                "timestamp": 1430068515,
                "quote": 0.658443
            },
            "result": 1.5
        }

    @patch("services.currency.requests.get")
    def test_current_gets_value(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.fx_response
        fx_rate_service = FXRateService(access_key="access_key")
        assert fx_rate_service.current("EUR", "USD") == 1.5
        assert mock_get.assert_called_once

    @patch("services.currency.requests.get")
    def test_historical_gets_value(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.fx_response
        fx_rate_service = FXRateService(access_key="access_key")
        date = "2024-01-10"
        assert fx_rate_service.historical("EUR", "USD", date) == 1.5
        assert mock_get.assert_called_once

    @patch("services.currency.requests.get")
    def test_raises_exception_success_false(self, mock_get):
        mock_get.return_value.status_code = 200
        fx_response = self.fx_response.copy()
        fx_response["success"] = False
        fx_response["error"] = {
            "info": "Some random error"
        }
        mock_get.return_value.json.return_value = fx_response
        fx_rate_service = FXRateService(access_key="access_key")
        date = "2024-01-10"

        with pytest.raises(FXRateServiceException):
            fx_rate_service.current("USD", "EUR")

        with pytest.raises(FXRateServiceException):
            fx_rate_service.historical("USD", "EUR", date)

    @patch("services.currency.requests.get")
    def test_raises_exception_status_code_not_200(self, mock_get):
        mock_get.return_value.status_code = 400
        mock_get.return_value.json.return_value = self.fx_response
        fx_rate_service = FXRateService(access_key="access_key")
        date = "2024-01-10"

        with pytest.raises(FXRateServiceException):
            fx_rate_service.current("USD", "EUR")

        with pytest.raises(FXRateServiceException):
            fx_rate_service.historical("USD", "EUR", date)


if __name__ == '__main__':
    unittest.main()
