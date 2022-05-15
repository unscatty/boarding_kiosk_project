from video_indexer import VideoIndexer
from env import ENV

__vi_config = ENV.azure.video_indexer

video_indexer_client = VideoIndexer(vi_subscription_key=__vi_config.subscription_key,
                             vi_location=__vi_config.location, vi_account_id=__vi_config.account_id)

video_indexer_client.check_access_token()