
from mock import patch, MagicMock

from main import find_registration_date


def test_api_call():
    with patch('requests.get') as requests_get_mock:
        response_mock = MagicMock()
        requests_get_mock.return_value = response_mock
        data = {
            'data': [
                { 'created_time': "2016-12-31T07:46:39+0000" },
                { 'created_time': "2016-12-30T07:46:39+0000" },
            ]
        }
        response_mock.json.return_value = data
        result_date = find_registration_date('mytoken')
        # check result date
        # check that request_get_mock was called with required url argument


def test_api_call_noresult():
    # similar test but check that no records for user is still handled properly
    pass
