# <img src="panda-patrol.png" alt="Panda Patrol" width="50"/> Panda Patrol
![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Python](https://img.shields.io/badge/python-3.8-blue.svg) 

**Add dashboards, alerting, and silencing to your data tests with < 10  lines of code.**

**Questions and feedback** 

Email: ivanzhangofficial@gmail.com

Call: https://calendly.com/aivanzhang/chat

<!-- **See [Dagster]()** on how to add panda patrols into your Dagster-based data pipelines.

**See [Airflow]()** on how to add panda patrols into your Airflow-based data pipelines.

**See [DBT]()** on how to add panda patrols into your DBT-based data pipelines. -->

## Overview
Wrap your existing data tests to automatically generate dashboards, alerting, and silencing. Currently this library does not deal with the orchestration of these data tests. However this may be added in the future depending on demand.


## Quickstart
### 1) Installation
Install the latest version of panda-patrol using pip:
```bash
pip install panda-patrol
```
### 2) Setup the environment variables
In an existing or new `.env` file, set the following environment variables:
```bash
PANDA_PATROL_URL
PANDA_PATROL_ENV
PANDA_DATABASE_URL
SMTP_SERVER
SMTP_PORT
SMTP_USER
SMTP_PASS
PATROL_EMAIL
```
See [`.env.example`](https://github.com/aivanzhang/panda_patrol/blob/main/.env.example) for more information about how to set these environment variables. See [Environment Variables](https://github.com/aivanzhang/panda_patrol/wiki/Environment-Variables) for more information about each environment variable.
### 3) Start the panda-patrol server. This will spin up a website at `PANDA_PATROL_URL`.
```bash
python -m panda_patrol
```
### 4) Wrap your existing data tests
Spin up a new data test dashboard by wrapping your existing data tests with `patrol_group` and `@patrol`. The following example shows how to wrap a data test in a dagster pipeline. However, you can use whatever Python-based data pipeline.

At a high level, you do the following:
1. Import `patrol_group` and `@patrol`
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

### 5) Run your data pipeline
Start your data pipelines as you normally would. Then run the step in the pipeline with the test. Here we use dagster to run the data tests. However, you can use whatever Python-based data pipeline.
```bash
dagster dev -f hello-dagster.py
```

### 6) View the results
Go to `PANDA_PATROL_URL` to view the results of your data tests. You should see something like this:

**Dashboard**

![Panda Patrol Dashboard](dashboard.png)

**Run Details**
![Log](run.png)

:tada: Congrats! :tada: You have created your first data test dashboard! See the [documentation](https://github.com/aivanzhang/panda_patrol/wiki) for more information on other features like adjustable parameters, alerting, and silencing.
