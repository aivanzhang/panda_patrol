import json

import pandas as pd
import requests
from panda_patrol.patrols import patrol_group
from panda_patrol.parameters import adjustable_parameter

from dagster import AssetExecutionContext, MetadataValue, asset


@asset
def hackernews_top_story_ids():
    """Get top stories from the HackerNews top stories endpoint.

    API Docs: https://github.com/HackerNews/API#new-top-and-best-stories.
    """
    top_story_ids = requests.get(
        "https://hacker-news.firebaseio.com/v0/topstories.json"
    ).json()

    with open("hackernews_top_story_ids.json", "w") as f:
        json.dump(top_story_ids[:10], f)


# asset dependencies can be inferred from parameter names
@asset(deps=[hackernews_top_story_ids])
def hackernews_top_stories(context: AssetExecutionContext):
    """Get items based on story ids from the HackerNews items endpoint."""
    with open("hackernews_top_story_ids.json", "r") as f:
        hackernews_top_story_ids = json.load(f)

    results = []
    for item_id in hackernews_top_story_ids:
        item = requests.get(
            f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
        ).json()
        results.append(item)

    # for item in results:
    #     print(item["url"])
    #     get_item_response = requests.get(item["url"])
    #     assert get_item_response.status_code == 200

    # TEST: Make sure that the item's URL is a valid URL
    with patrol_group("Hackernews URLs are Valid") as patrol:

        @patrol("URLs work")
        def urls_work(patrol_id):
            """URLs for stories should work."""
            for item in results:
                print(item["url"])
                get_item_response = requests.get(item["url"])
                assert get_item_response.status_code == 200

            return len(results)

        @patrol("Expected Number of URLs found")
        def expected_number_of_urls_found(patrol_id):
            """We should find the expected number of URLs."""
            expected_number_urls = int(
                adjustable_parameter("expected_urls", patrol_id, 5)
            )
            assert (
                len(results) >= expected_number_urls
            ), f"Expected {expected_number_urls} URLs, found {len(results)}"

            return len(results)

    df = pd.DataFrame(results)
    df.to_csv("hackernews_top_stories.csv")

    # recorded metadata can be customized
    metadata = {
        "num_records": len(df),
        "preview": MetadataValue.md(df[["title", "by", "url"]].to_markdown()),
    }

    context.add_output_metadata(metadata=metadata)
