import json

from core.utils import make_api_request, handle_rate_limit, get_user_id
import logging
import csv

# Setup logging
logger = logging.getLogger(__name__)


def scrape_followers(username, output='followers.csv'):
    """
    Scrape the followers of a Twitter profile and save them to a CSV file.

    Args:
        username (str): The Twitter username whose followers are to be scraped.
        output (str): The file to save the scraped followers.

    Returns:
        bool: True if followers were scraped successfully, False otherwise.
    """
    try:
        headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs=1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "content-type": "application/json",
            "cookie": (
                'lang=en; guest_id=v1:171371941877117841; twid=u=1358100288180215809; auth_token=6bd3443f047a6caa31927874d7eaa86ec8f2b91c; guest_id_ads=v1:171371941877117841; guest_id_marketing=v1:171371941877117841; lang=en; '
                'ct0=70a34f7aa63a411803e86a946c3e02325aa222d072bcb2617606c0ebb125b17d57bdc65b5f68758f7bd7b4912f0c963d42de5f1eb83f1b4e095a8203faf8e5371a255572ca31413ec5a343e7ea366353; _ga=GA1.2.1042874475.1716177174; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCIFYTDCQAToMY3NyZl9p%250AZCIlNWQzYzdjMzVmMTM2YzFkZTcyZGI0ZmYzMDc4YWExMzQ6B2lkIiVhYjlk%250AODE4OGM4NWE5YWRkZDgyODYyYzBiNzY3NWNlMQ%253D%253D--352fcf836da806395c452be51cc6857d908454b8; external_referer=KAn9PNL%2B4nbrCBC7vKfBRFpTKLuDKzwXPCGTA4VOvXHHeQgzJLZm1Q%3D%3D|0|8e8t2xd8A2w%3D; personalization_id="v1_T1QAdUmYAUesOfzaZNWXHw=="'),
            "origin": "https://x.com",
            "referer": f"https://x.com/{username}/followers",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
            "x-client-transaction-id": "7rtf3q1yD8YX7xUpyzEKOs1E4goNaVKgwn8WV+5+V2OE2NkTmOe+BhWQzh7B15GLXEPBvOyTzgvc7YxuMtjZGLXrPI6q7Q",
            "x-csrf-token": "70a34f7aa63a411803e86a946c3e02325aa222d072bcb2617606c0ebb125b17d57bdc65b5f68758f7bd7b4912f0c963d42de5f1eb83f1b4e095a8203faf8e5371a255572ca31413ec5a343e7ea366353",
            "x-twitter-active-user": "no",
            "x-twitter-auth-type": "OAuth2Session",
            "x-twitter-client-language": "en"
        }
        cursor = None
        # Get the user ID of the profile
        user_id = get_user_id(username)
        if not user_id:
            logger.error(f"User not found: {username}")
            return False

        # Endpoint for getting followers
        url = "https://x.com/i/api/graphql/lFNlN3CqiVsiNo-KOSUmJA/Followers"
        followers = []
        while True:
            variables = {"userId": user_id, "count": 20, "includePromotedContent": False, "cursor": cursor}
            variables = json.dumps(variables)
            params = {
                "variables": variables,
                "features": "{\"rweb_tipjar_consumption_enabled\":true,\"responsive_web_graphql_exclude_directive_enabled\":true,\"verified_phone_label_enabled\":false,\"creator_subscriptions_tweet_preview_api_enabled\":true,\"responsive_web_graphql_timeline_navigation_enabled\":true,\"responsive_web_graphql_skip_user_profile_image_extensions_enabled\":false,\"communities_web_enable_tweet_community_results_fetch\":true,\"c9s_tweet_anatomy_moderator_badge_enabled\":true,\"articles_preview_enabled\":true,\"tweetypie_unmention_optimization_enabled\":true,\"responsive_web_edit_tweet_api_enabled\":true,\"graphql_is_translatable_rweb_tweet_is_translatable_enabled\":true,\"view_counts_everywhere_api_enabled\":true,\"longform_notetweets_consumption_enabled\":true,\"responsive_web_twitter_article_tweet_consumption_enabled\":true,\"tweet_awards_web_tipping_enabled\":false,\"creator_subscriptions_quote_tweet_preview_enabled\":false,\"freedom_of_speech_not_reach_fetch_enabled\":true,\"standardized_nudges_misinfo\":true,\"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled\":true,\"rweb_video_timestamps_enabled\":true,\"longform_notetweets_rich_text_read_enabled\":true,\"longform_notetweets_inline_media_enabled\":true,\"responsive_web_enhance_cards_enabled\":false}"
            }
            # Make the API request
            response = make_api_request(url, params=params, headers=headers)

            # Handle rate limits and retry if necessary
            if response and handle_rate_limit(response):
                response = make_api_request(url, params=params)

            if response and response.status_code == 200:
                data = response.json()
                instructions = data['data']['user']['result']['timeline']['timeline']['instructions']
                for instruction in instructions:
                    if instruction['type'] == 'TimelineAddEntries':
                        for entry in instruction['entries']:
                            if entry['content']['entryType'] == 'TimelineTimelineItem':
                                user_details = {}
                                try:
                                    user = entry['content']['itemContent']['user_results']['result']
                                    user_details['username'] = user['legacy']['screen_name']
                                    user_details['name'] = user['legacy']['name']
                                    user_details['user_id'] = user['rest_id']
                                    user_details['can_dm'] = user['legacy']['can_dm']
                                    user_details['bio'] = user['legacy']['description']
                                    followers.append(user_details)
                                except KeyError:
                                    pass
                try:
                    cursor = instructions[-1]['entries'][-2]['content']['value']
                except (KeyError, IndexError):
                    cursor = None
                if cursor[0] == '0':
                    break
                logger.info(f"Scraped {len(followers)} followers of {username}")
        # Save the followers to a CSV file
        save_to_csv(followers, output)
        logger.info(f"Scraped {len(followers)} followers of {username} and saved to {output}")
        return True

    except Exception as e:
        logger.error(f"Error scraping followers: {e}")
        return False


def save_to_csv(followers, output):
    """
    Save the scraped followers to a CSV file.

    Args:
        followers (list): A list of follower data dictionaries.
        output (str): The file to save the followers.
    """
    try:
        # Define the CSV columns
        fields = ['user_id', 'name', 'username', 'bio', 'can_dm']

        # Write to the CSV file
        with open(output, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            writer.writerows(followers)

        logger.info(f"Followers successfully saved to {output}")

    except Exception as e:
        logger.error(f"Error saving followers to CSV: {e}")

