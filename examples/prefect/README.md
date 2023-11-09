# Integrate Panda Patrols with Prefect
This example shows how Panda Patrols can be integrated with your Prefect flows. It creates a basic Prefect flow with two tasks `fetch_data` and `transform_data` (which depends on the previous one). See [titanic_flow.py](titanic_flow.py) for the code. `hackernews_top_stories` pulls details about top stories and has data tests with respect to each story's link. Patrols are already setup for these test. Furthermore it profiles these urls and stores it in Panda Patrol.

## Setup
1. Install the requirements. This installs the necessary dependencies for prefect, panda patrol, and the ydata profiling library package.
    ```bash
    pip install -r requirements.txt
    ```
2. Start the Prefect server.
    ```bash
    prefect server start
    ```
3. Serve the flow.
    ```bash
    python titanic.py
    ```
4. Run the flow.
    ```
    prefect deployment run 'Titanic/run_titanic_analysis'
    ```
5. After the asset finishes, you should see the following message in your logs
    ```bash 
    See your Panda Patrol dashboard here: https://panda-patrol.vercel.app/public/public-xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    ```
    Click on the link to see the following dashboard
    ![Panda Patrol UI](result.gif)

:tada: Congrats! :tada: You have now added Panda Patrols to Prefect! See the [documentation](https://github.com/aivanzhang/panda_patrol/wiki) for more information on other features like adjustable parameters, alerting, and silencing.