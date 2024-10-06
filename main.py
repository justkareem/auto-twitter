import click
from core.dm_sender import send_dm
from core.scraper import scrape_followers
from core.commenter import comment_on_tweet


@click.group()
def cli():
    """Twitter Automation CLI"""
    pass


@cli.command()
@click.option('--user', required=True, help='Twitter username to send a DM to.')
@click.option('--message', required=True, help='Message to send in the DM.')
def send_dm_command(user, message):
    """Send a direct message to a user"""
    try:
        send_dm(user, message)
        click.echo(f"DM sent to {user}: {message}")
    except Exception as e:
        click.echo(f"Error sending DM: {e}")


@cli.command()
@click.option('--username', help='User\'s followers to scrape.')
@click.option('--output', default='tweets.csv', help='File to save scraped followers.')
def scrape_command(username, output):
    """Scrape users based on a profile's followers"""
    try:
        scrape_followers(username, output)
        click.echo(f"Followers scraped and saved to {output}")
    except Exception as e:
        click.echo(f"Error scraping followers: {e}")


@cli.command()
@click.option('--tweet_id', required=True, help='ID of the tweet to comment on.')
@click.option('--message', required=True, help='Comment message to post.')
def comment_command(tweet_id, message):
    """Comment on a specific tweet"""
    try:
        comment_on_tweet(tweet_id, message)
        click.echo(f"Commented on tweet {tweet_id}: {message}")
    except Exception as e:
        click.echo(f"Error commenting on tweet: {e}")


if __name__ == '__main__':
    cli()
