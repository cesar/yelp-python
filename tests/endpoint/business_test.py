# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import mock
import pytest

import yelp.endpoint.business
from testing.util import read_json_file
from yelp.endpoint.business import BusinessEndpoints


@pytest.fixture
def business_endpoints(mock_client):
    return BusinessEndpoints(mock_client)


@pytest.fixture
def mock_business_response_cls():
    with mock.patch.object(
        yelp.endpoint.business, "Business"
    ) as mock_business_response_cls:
        yield mock_business_response_cls


class TestBusiness:
    def test_no_url_params(
        self, business_endpoints, mock_client, mock_business_response_cls
    ):
        business_endpoints.get_by_id("test-id")

        mock_client._make_request.assert_called_once_with(
            "/v3/businesses/test-id", url_params={}
        )
        assert mock_business_response_cls.called

    def test_with_url_params(
        self, business_endpoints, mock_client, mock_business_response_cls
    ):
        business_endpoints.get_by_id("test-id", locale="fr_FR")

        mock_client._make_request.assert_called_once_with(
            "/v3/businesses/test-id", url_params={"locale": "fr_FR"}
        )
        assert mock_business_response_cls.called

    def test_search_when_no_search_results(
        self, business_endpoints, mock_client, mock_business_response_cls
    ):
        mock_client._make_request.return_value = {"businesses": []}

        business_endpoints.search(term="brunch", location="SF")

        mock_client._make_request.assert_called_once_with(
            "/v3/businesses/search", url_params={"term": "brunch", "location": "SF"}
        )
        assert not mock_business_response_cls.called  # the businesses array is empty

    def test_search_when_results_available(
        self, business_endpoints, mock_client, mock_business_response_cls
    ):
        mocked_response_data = read_json_file("business_search_pizza_san_bruno.json")
        mock_client._make_request.return_value = mocked_response_data
        business_endpoints.search(term="pizza", location="San Bruno")
        mock_client._make_request.assert_called_once_with(
            "/v3/businesses/search",
            url_params={"term": "pizza", "location": "San Bruno"},
        )
        assert mock_business_response_cls.called
        assert mock_business_response_cls.call_count == len(
            mocked_response_data["businesses"]
        )
