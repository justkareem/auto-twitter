from core.utils import make_api_request, handle_rate_limit
import logging
import random

# Setup logging
logger = logging.getLogger(__name__)


def comment_on_tweet(tweet_id, comment):
    try:
        url = "https://x.com/i/api/graphql/oB-5XsHNAbjvARJEc8CZFw/CreateTweet"
        headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "content-type": "application/json",
            "cookie": "lang=en; guest_id=v1%3A171371941877117841; twid=u%3D1358100288180215809; auth_token=6bd3443f047a6caa31927874d7eaa86ec8f2b91c; guest_id_ads=v1%3A171371941877117841; guest_id_marketing=v1%3A171371941877117841; lang=en; ct0=70a34f7aa63a411803e86a946c3e02325aa222d072bcb2617606c0ebb125b17d57bdc65b5f68758f7bd7b4912f0c963d42de5f1eb83f1b4e095a8203faf8e5371a255572ca31413ec5a343e7ea366353; _ga=GA1.2.1042874475.1716177174; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCIFYTDCQAToMY3NyZl9p%250AZCIlNWQzYzdjMzVmMTM2YzFkZTcyZGI0ZmYzMDc4YWExMzQ6B2lkIiVhYjlk%250AODE4OGM4NWE5YWRkZDgyODYyYzBiNzY3NWNlMQ%253D%253D--352fcf836da806395c452be51cc6857d908454b8; external_referer=KAn9PNL%2B4nbrCBC7vKfBRFpTKLuDKzwXPCGTA4VOvXHHeQgzJLZm1Q%3D%3D|0|8e8t2xd8A2w%3D; personalization_id=\"v1_Tuzdt1ImY4bvhpiF8C6XzA==\"",
            "origin": "https://x.com",
            "priority": "u=1, i",
            "referer": "https://x.com/compose/post",
            "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Microsoft Edge\";v=\"126\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
            "x-csrf-token": "70a34f7aa63a411803e86a946c3e02325aa222d072bcb2617606c0ebb125b17d57bdc65b5f68758f7bd7b4912f0c963d42de5f1eb83f1b4e095a8203faf8e5371a255572ca31413ec5a343e7ea366353",
            "x-twitter-active-user": "yes",
            "x-twitter-auth-type": "OAuth2Session",
            "x-twitter-client-language": "en"
        }
        payload = {
            "variables": {
                "tweet_text": comment,
                "reply": {
                    "in_reply_to_tweet_id": str(tweet_id),
                    "exclude_reply_user_ids": []
                },
                "dark_request": False,
                "media": {
                    "media_entities": [],
                    "possibly_sensitive": False
                },
                "semantic_annotation_ids": []
            },
            "features": {
                "communities_web_enable_tweet_community_results_fetch": True,
                "c9s_tweet_anatomy_moderator_badge_enabled": True,
                "tweetypie_unmention_optimization_enabled": True,
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
            "queryId": "oB-5XsHNAbjvARJEc8CZFw"
        }
        # Make the API request
        response = make_api_request(url, headers=headers, method='POST', data=payload)

        # Handle rate limits and retry if necessary
        if response and handle_rate_limit(response):
            response = make_api_request(url, headers=headers, method='POST', data=payload)

        if response and response.status_code == 200:
            logger.info("Successful commented on tweet")

        else:
            logger.error(f"Failed to comment on tweet")

    except Exception as e:
        logger.error(f"Error commenting on tweet: {e}")

