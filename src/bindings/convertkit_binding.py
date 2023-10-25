import requests
from dateutil.parser import parse

BASE_API_URL = "https://api.convertkit.com/v3"

class ConvertKit:
    def __init__(self, api_secret, api_key):
        self.api_secret = api_secret
        self.api_key = api_key

    def fetch_tags(self):
        """Fetch all tags from ConvertKit."""
        url = f"{BASE_API_URL}/tags?api_key={self.api_key}"
        response = self._send_request(url)
        return response['tags']

    def fetch_tag_subscribers(self, tag_id, start_date=None, end_date=None):
        """Fetch subscribers of a given tag within a date range."""
        page = 1
        filtered_subscriptions = []

        while True:
            url = f"{BASE_API_URL}/tags/{tag_id}/subscriptions?api_secret={self.api_secret}&page={page}&sort_order=desc"
            data = self._send_request(url)
            subscriptions = data['subscriptions']

            if not subscriptions:
                break

            subscriptions_in_range, out_of_range = self._filter_subscriptions_by_date(subscriptions, start_date, end_date)
            filtered_subscriptions.extend(subscriptions_in_range)

            if out_of_range or data['page'] >= data['total_pages']:
                break

            page += 1

        return filtered_subscriptions

    def list_subscribers(self, page=1, from_date=None, to_date=None, 
                         updated_from=None, updated_to=None, sort_order=None, 
                         sort_field=None, email_address=None):
        """List subscribers based on the provided parameters."""
        params = {
            "api_secret": self.api_secret,
            "page": page,
            "from": from_date,
            "to": to_date,
            "updated_from": updated_from,
            "updated_to": updated_to,
            "sort_order": sort_order,
            "sort_field": sort_field,
            "email_address": email_address
        }
        response = self._send_request(f"{BASE_API_URL}/subscribers", params=params)
        return response['subscribers']

    def view_subscriber(self, subscriber_id):
        """View details of a single subscriber."""
        params = {
            "api_secret": self.api_secret
        }
        response = self._send_request(f"{BASE_API_URL}/subscribers/{subscriber_id}", params=params)
        return response['subscriber']

    def update_subscriber(self, subscriber_id, first_name=None, email_address=None, fields=None):
        """Update the details of a single subscriber."""
        data = {
            "api_secret": self.api_secret,
            "first_name": first_name,
            "email_address": email_address,
            "fields": fields
        }
        response = self._send_put_request(f"{BASE_API_URL}/subscribers/{subscriber_id}", json=data)
        return response['subscriber']

    def unsubscribe_subscriber(self, email):
        """Unsubscribe a subscriber by email."""
        data = {
            "api_secret": self.api_secret,
            "email": email
        }
        response = self._send_put_request(f"{BASE_API_URL}/unsubscribe", json=data)
        return response['subscriber']

    def list_tags_for_subscriber(self, subscriber_id):
        """List tags for a given subscriber."""
        params = {
            "api_key": self.api_key
        }
        response = self._send_request(f"{BASE_API_URL}/subscribers/{subscriber_id}/tags", params=params)
        return response['tags']

    def _send_request(self, url, params=None):
        """Send a GET request and return the JSON response."""
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def _send_put_request(self, url, json=None):
        """Send a PUT request and return the JSON response."""
        response = requests.put(url, json=json)
        response.raise_for_status()
        return response.json()

    def _filter_subscriptions_by_date(self, subscriptions, start_date, end_date):
        """Filter a list of subscriptions by a date range."""
        filtered = []
        out_of_range = True
        for subscription in subscriptions:
            subscription_date = parse(subscription['created_at']).replace(tzinfo=None)
            if (not start_date or start_date <= subscription_date) and (not end_date or subscription_date <= end_date):
                filtered.append(subscription)
                out_of_range = False
        return filtered, out_of_range


