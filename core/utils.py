import os
import requests
from dotenv import load_dotenv
import logging
import time

# Load environment variables from a .env file
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Twitter API credentials loaded from environment variables
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")


def authenticate():
    """Authenticate to the Twitter API using Bearer Token."""
    if not BEARER_TOKEN:
        raise ValueError("Twitter Bearer Token is not set in environment variables.")
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "origin": "https://x.com",
        "authorization": f"Bearer {BEARER_TOKEN}",
        "content-Type": "application/json",
        "x-twitter-active-user": "yes",
        "x-twitter-auth-type": "OAuth2Session",
        "x-twitter-client-language": "en",
    }
    return headers


def make_api_request(url, method="GET", params=None, data=None, headers=None):
    """Make a request to the Twitter API."""
    if headers is None:
        headers = authenticate()

    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        else:
            raise ValueError(f"Unsupported method: {method}")

        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logger.error(f"An error occurred: {err}")
    return None


def handle_rate_limit(response):
    """Handle Twitter API rate limits."""
    if response.status_code == 429:
        reset_time = int(response.headers.get('x-rate-limit-reset', 0))
        sleep_time = max(reset_time - time.time(), 0)
        logger.warning(f"Rate limit exceeded. Sleeping for {sleep_time} seconds.")
        time.sleep(sleep_time)
        return True
    return False


def handle_dm_rate_limit(response):
    """Handle Twitter DM rate limits."""
    if response.status_code == 403:
        if response.json()['errors'][0]['code'] == 226:
            time.sleep(600)
            logger.warning(f"Rate limit exceeded. Sleeping for 10 minutes.")
            return True
    return False


def get_user_id(username):
    """Get the user ID for a given username."""
    headers = {
        "accept": "*/*",
        "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "content-type": "application/json",
        "cookie": (
            "lang=en; guest_id=v1%3A171371941877117841; twid=u%3D1358100288180215809; auth_token=6bd3443f047a6caa31927874d7eaa86ec8f2b91c;"
            "guest_id_ads=v1%3A171371941877117841; guest_id_marketing=v1%3A171371941877117841; lang=en; ct0=70a34f7aa63a411803e86a946c3e02325aa222d072bcb2617606c0ebb125b17d57bdc65b5f68758f7bd7b4912f0c963d42de5f1eb83f1b4e095a8203faf8e5371a255572ca31413ec5a343e7ea366353;"
            "_ga=GA1.2.1042874475.1716177174; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCIFYTDCQAToMY3NyZl9p%250AZCIlNWQzYzdjMzVmMTM2YzFkZTcyZGI0ZmYzMDc4YWExMzQ6B2lkIiVhYjlk%250AODE4OGM4NWE5YWRkZDgyODYyYzBiNzY3NWNlMQ%253D%253D--352fcf836da806395c452be51cc6857d908454b8;"
            "external_referer=KAn9PNL%2B4nbrCBC7vKfBRFpTKLuDKzwXPCGTA4VOvXHHeQgzJLZm1Q%3D%3D|0|8e8t2xd8A2w%3D; personalization_id=\"v1_2LO6aX6D7updZBgz9WX+lQ==\""),
        "user-agent": "TwitterAndroid/9.86.0-release.0 (23680000-r-0) (Android 10; Google Pixel 3; Build/QP1A.190711.020; wv)",
        "x-csrf-token": "70a34f7aa63a411803e86a946c3e02325aa222d072bcb2617606c0ebb125b17d57bdc65b5f68758f7bd7b4912f0c963d42de5f1eb83f1b4e095a8203faf8e5371a255572ca31413ec5a343e7ea366353",
        "x-twitter-auth-type": "OAuth2Session",
        "x-twitter-client-language": "en",
        "x-twitter-active-user": "yes",
        "x-client-uuid": "5d84308f-f921-427e-84f2-cef40689a750",
        "referer": "https://x.com/",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty"
    }
    url = ("https://x.com/i/api/graphql/xmU6X_CKVnQ5lSrCbAmJsg/UserByScreenName?"
           f"variables=%7B%22screen_name%22%3A%22{username}%22%2C%22withSafetyModeUserFields%22%3Atrue%7D"
           "&features=%7B%22hidden_profile_subscriptions_enabled%22%3Atrue%2C%22rweb_tipjar_consumption_enabled%22%3Atrue"
           "%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse"
           "%2C%22subscriptions_verification_info_is_identity_verified_enabled%22%3Atrue%2C%22subscriptions_verification_info_verified_since_enabled%22%3Atrue"
           "%2C%22highlights_tweets_tab_ui_enabled%22%3Atrue%2C%22responsive_web_twitter_article_notes_tab_enabled%22%3Atrue"
           "%2C%22subscriptions_feature_can_gift_premium%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue"
           "%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%7D"
           "&fieldToggles=%7B%22withAuxiliaryUserLabels%22%3Afalse%7D")
    response = make_api_request(url=url, headers=headers)
    if response:
        return response.json()['data']['user']['result']['rest_id']
    return None


def post_tweet(message):
    """Post a tweet on your timeline."""
    url = "https://x.com/i/api/graphql/xT36w0XM3A8jDynpkram2A/CreateTweet"

    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": f"Bearer {BEARER_TOKEN}",
        "content-type": "application/json",
        "cookie": (
            "lang=en; guest_id=v1%3A171371941877117841; twid=u%3D1358100288180215809; auth_token=6bd3443f047a6caa31927874d7eaa86ec8f2b91c;"
            "guest_id_ads=v1%3A171371941877117841; guest_id_marketing=v1%3A171371941877117841; lang=en; ct0=70a34f7aa63a411803e86a946c3e02325aa222d072bcb2617606c0ebb125b17d57bdc65b5f68758f7bd7b4912f0c963d42de5f1eb83f1b4e095a8203faf8e5371a255572ca31413ec5a343e7ea366353;"
            "_ga=GA1.2.1042874475.1716177174; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCIFYTDCQAToMY3NyZl9p%250AZCIlNWQzYzdjMzVmMTM2YzFkZTcyZGI0ZmYzMDc4YWExMzQ6B2lkIiVhYjlk%250AODE4OGM4NWE5YWRkZDgyODYyYzBiNzY3NWNlMQ%253D%253D--352fcf836da806395c452be51cc6857d908454b8;"
            "external_referer=KAn9PNL%2B4nbrCBC7vKfBRFpTKLuDKzwXPCGTA4VOvXHHeQgzJLZm1Q%3D%3D|0|8e8t2xd8A2w%3D; personalization_id=\"v1_2LO6aX6D7updZBgz9WX+lQ==\""),
        "origin": "https://x.com",
        "priority": "u=1, i",
        "referer": "https://x.com/compose/post",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Microsoft Edge\";v=\"127\", \"Chromium\";v=\"127\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0",
        "x-client-transaction-id": "ToidDUOy08ANmN9rO8vuULyjhJxRYkF939oRAoVOWL4qkewspQfZ9yy6tkH06C9tjeChJ0zSxIda70nuYn430f2rYrRFTQ",
        "x-csrf-token": "70a34f7aa63a411803e86a946c3e02325aa222d072bcb2617606c0ebb125b17d57bdc65b5f68758f7bd7b4912f0c963d42de5f1eb83f1b4e095a8203faf8e5371a255572ca31413ec5a343e7ea366353",
        "x-twitter-active-user": "yes",
        "x-twitter-auth-type": "OAuth2Session",
        "x-twitter-client-language": "en"
    }

    data = {
        "variables": {
            "tweet_text": message,
            "dark_request": False,
            "media": {
                "media_entities": [],
                "possibly_sensitive": False
            },
            "semantic_annotation_ids": [],
            "disallowed_reply_options": None
        },
        "features": {
            "communities_web_enable_tweet_community_results_fetch": True,
            "c9s_tweet_anatomy_moderator_badge_enabled": True,
            "responsive_web_edit_tweet_api_enabled": True,
            "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
            "view_counts_everywhere_api_enabled": True,
            "longform_notetweets_consumption_enabled": True,
            "responsive_web_twitter_article_tweet_consumption_enabled": True,
            "tweet_awards_web_tipping_enabled": False,
            "creator_subscriptions_quote_tweet_preview_enabled": False,
            "longform_notetweets_rich_text_read_enabled": True,
            "longform_notetweets_inline_media_enabled": True,
            "articles_preview_enabled": True,
            "rweb_video_timestamps_enabled": True,
            "rweb_tipjar_consumption_enabled": True,
            "responsive_web_graphql_exclude_directive_enabled": True,
            "verified_phone_label_enabled": False,
            "freedom_of_speech_not_reach_fetch_enabled": True,
            "standardized_nudges_misinfo": True,
            "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
            "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
            "responsive_web_graphql_timeline_navigation_enabled": True,
            "responsive_web_enhance_cards_enabled": False
        },
        "queryId": "xT36w0XM3A8jDynpkram2A"
    }

    response = make_api_request(url, method="POST", data=data, headers=headers)
    if response:
        return response
    return None
