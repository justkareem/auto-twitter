from core.utils import get_user_id, make_api_request, handle_dm_rate_limit
import logging

# Setup logging
logger = logging.getLogger(__name__)


def send_dm(username, message):
    """
    Send a direct message to a Twitter user.

    Args:
        username (str): The Twitter username of the recipient.
        message (str): The message to be sent.

    Returns:
        bool: True if the DM was sent successfully, False otherwise.
    """
    try:
        # Get the user ID of the recipient
        user_id = get_user_id(username)
        if not user_id:
            logger.error(f"User not found: {username}")
            return False

        # Endpoint for sending a direct message
        url = "https://x.com/i/api/1.1/dm/new2.json"
        params = {
            "include_ext_alt_text": "true",
            "include_ext_limited_action_results": "true",
            "include_reply_count": "1",
            "tweet_mode": "extended",
            "include_ext_views": "true",
            "include_groups": "true",
            "include_inbox_timelines": "true",
            "include_ext_media_color": "true",
            "supports_reactions": "true"
        }
        headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs=1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "content-type": "application/json",
            "cookie": 'lang=en; guest_id=v1:171371941877117841; twid=u=1358100288180215809; auth_token=6bd3443f047a6caa31927874d7eaa86ec8f2b91c; guest_id_ads=v1:171371941877117841; guest_id_marketing=v1:171371941877117841; lang=en; ct0=70a34f7aa63a411803e86a946c3e02325aa222d072bcb2617606c0ebb125b17d57bdc65b5f68758f7bd7b4912f0c963d42de5f1eb83f1b4e095a8203faf8e5371a255572ca31413ec5a343e7ea366353; _ga=GA1.2.1042874475.1716177174; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCIFYTDCQAToMY3NyZl9p%250AZCIlNWQzYzdjMzVmMTM2YzFkZTcyZGI0ZmYzMDc4YWExMzQ6B2lkIiVhYjlk%250AODE4OGM4NWE5YWRkZDgyODYyYzBiNzY3NWNlMQ%253D%253D--352fcf836da806395c452be51cc6857d908454b8; external_referer=KAn9PNL%2B4nbrCBC7vKfBRFpTKLuDKzwXPCGTA4VOvXHHeQgzJLZm1Q%3D%3D|0|8e8t2xd8A2w%3D; personalization_id="v1_T1QAdUmYAUesOfzaZNWXHw=="',
            "origin": "https://x.com",
            "referer": f"https://x.com/messages/1358100288180215809-{user_id}",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
            "x-csrf-token": "70a34f7aa63a411803e86a946c3e02325aa222d072bcb2617606c0ebb125b17d57bdc65b5f68758f7bd7b4912f0c963d42de5f1eb83f1b4e095a8203faf8e5371a255572ca31413ec5a343e7ea366353",
            "x-twitter-active-user": "yes",
            "x-twitter-auth-type": "OAuth2Session",
            "x-twitter-client-language": "en"
        }

        data = {
            "conversation_id": f"1358100288180215809-{user_id}",
            "text": message,
            "cards_platform": "Web-12",
            "include_cards": 1,
            "include_quote_count": True
        }

        # Send the DM
        response = make_api_request(url, method="POST", data=data, headers=headers)

        # Check for rate limits and retry if necessary
        if handle_dm_rate_limit(response):
            response = make_api_request(url, method="POST", data=data, headers=headers)

        if response.status_code == 200:
            logger.info(f"DM sent to {username}: {message}")
            return True
        else:
            logger.error(f"Failed to send DM to {username}")
            return False

    except Exception as e:
        logger.error(f"Error sending DM to {username}: {e}")
        return False

