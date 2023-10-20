# <img src="panda-patrol.png" alt="Panda Patrol" width="50"/> Panda Patrol
![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Python](https://img.shields.io/badge/python-3.8-blue.svg) 

Add dashboards, alerting, and silencing to your data tests with <ins> **less than 5 lines of code.** </ins>

**Questions and feedback** 

Email: ivanzhangofficial@gmail.com

Call: https://calendly.com/aivanzhang/chat

**See [Airflow](examples/airflow#add-panda-patrols-to-your-airflow-data-tests)** on how to add panda patrols into your Airflow-based data pipelines.

**See [Dagster](examples/dagster#add-panda-patrols-to-your-dagster-data-tests)** on how to add panda patrols into your Dagster-based data pipelines.

## Overview
Wrap your existing data tests to automatically generate dashboards, alerting, and silencing. Currently this library does not deal with the orchestration of these data tests. However this may be added in the future depending on demand.


## Getting Started (Demo)
This is a short tutorial that creates a patrol around a data test and then displays this patrol on a **publicly accessible** dashboard here: https://panda-patrol.vercel.app/dashboard. This tutorial uses [dagster](https://docs.dagster.io/) to run the data tests. However, you can use whatever Python-based data pipeline.


### 1) Installation
Install the latest version of panda-patrol using pip:
```bash
pip install panda-patrol
```
### 2) Setup the environment variables
In an existing or new `.env` file, set the following environment variables:
```bash
PANDA_PATROL_URL=https://panda-patrol.vercel.app/dashboard
PANDA_PATROL_ENV=production
```
See [`.env.example`](https://github.com/aivanzhang/panda_patrol/blob/main/.env.example) for more information about how to set these and other environment variables. See [Environment Variables](https://github.com/aivanzhang/panda_patrol/wiki/Environment-Variables) for more information about each environment variable.
### 3) Wrap your existing data tests
Spin up a new data test dashboard by wrapping your existing data tests with `patrol_group` and `@patrol`. The following example shows how to wrap a data test in a dagster pipeline. However, you can use whatever Python-based data pipeline.

At a high level, you do the following:
1. Import `patrol_group`
2. Group several data tests with `patrol_group`
3. Wrap each individual existing data test with `@patrol`
```python
from panda_patrol.patrols import patrol_group
...
with patrol_group(PATROL_GROUP_NAME) as patrol:
    @patrol(PATROL_NAME)
    def DATA_TEST_NAME(patrol_id):
        ...
```
Here is a more detailed example of how to wrap a data test in a dagster pipeline. Before (`hello-dagster.py` from https://docs.dagster.io/getting-started/hello-dagster):
```python
def hackernews_top_stories(context: AssetExecutionContext):
    """Get items based on story ids from the HackerNews items endpoint."""
    with open("hackernews_top_story_ids.json", "r") as f:
        hackernews_top_story_ids = json.load(f)

    results = []
    # Get information about each item including the url
    for item_id in hackernews_top_story_ids:
        item = requests.get(
            f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
        ).json()
        results.append(item)

        # DATA TEST: Make sure that the item's URL is a valid URL
        for item in results:
            print(item["url"])
            get_item_response = requests.get(item["url"])
            assert get_item_response.status_code == 200
    ...
```
After:
```diff
+ from panda_patrol.patrols import patrol_group
...
def hackernews_top_stories(context: AssetExecutionContext):
    """Get items based on story ids from the HackerNews items endpoint."""
    with open("hackernews_top_story_ids.json", "r") as f:
        hackernews_top_story_ids = json.load(f)

    results = []
    # Get information about each item including the url
    for item_id in hackernews_top_story_ids:
        item = requests.get(
            f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
        ).json()
        results.append(item)

    # DATA TEST: Make sure that the item's URL is a valid URL
+   with patrol_group("Hackernews Items are Valid") as patrol:
+	@patrol("URLs work")
+	def urls_work(patrol_id):
		"""URLs for stories should work."""
		for item in results:
			print(item["url"])
			get_item_response = requests.get(item["url"])
			assert get_item_response.status_code == 200
		
		return len(results)
    ...
```
>❗IMPORTANT\
> Note that each data test method (i.e. `urls_work`) should have only one parameter `patrol_id`. This parameter will be useful when defining parameters for your data tests in the [Parameters](https://github.com/aivanzhang/panda_patrol/wiki/Parameters).

### 4) Run your data pipeline
Start your data pipelines as you normally would. Then run the step in the pipeline with the test. Here we use dagster to run the data tests. However, you can use whatever Python-based data pipeline.
```bash
dagster dev -f hello-dagster.py
```

### 5) View the results
Go to https://panda-patrol.vercel.app/dashboard to view the results of your data tests. Note you may see other people's data tests on this dashboard as well. This is because this dashboard is publicly accessible.

:tada: Congrats! :tada: You have created your first data test dashboard! See the [documentation](https://github.com/aivanzhang/panda_patrol/wiki) for more information and [Quickstart](https://github.com/aivanzhang/panda_patrol/wiki/Quickstart) on how to spin up your own Panda Patrol server and other features like adjustable parameters, alerting, and silencing.
