# Add Panda Patrols to your DBT Data Tests
This example shows how Panda Patrols can be added to data tests inside your DBT pipeline. It creates several DBT models ([models](models)) and also a Python DBT model ([user_orders_products_view](models/user_orders_products_view.py)). This Python-based model is needed for our Python-based Panda Patrols. Patrols are set up for this Python model.

## Setup
1. Install the requirements. This installs the necessary dependencies for DBT and Panda Patrol. Note that we're using `dbt-postgres` as the adapter. You can use any adapter you want, but you will need to modify the `profiles.yml` accordingly. Furthermore, we're using [dbt-fal](https://github.com/fal-ai/dbt-fal) which provides further Python compatibility with DBT. 
    ```bash
    pip install -r requirements.txt
    ```
2. Make sure your `profiles.yml` is set up correctly. An example is provided in this directory [profiles.yml](profiles.yml). Note that in addition to the basic dbt options, we have added options needed for dbt-fal (see more details [here](https://github.com/fal-ai/dbt-fal/tree/main/projects/adapter#2-update-your-profilesyml-and-add-the-fal-adapter)).

3. Modify the `.env`. Note that the `SMTP_*` and `PATROL_EMAIL` values are dummy values. You will need to replace them with your own values if you want email alerts. `SLACK_WEBHOOK` is also a dummy value. You will need to replace it with your own value if you want slack alerts.
4. Start the Panda Patrol server. 
    ```bash
    python -m panda_patrol
    ```
5. Start monitoring the DBT test results. This stores all your dbt test results in Panda Patrol.
    ```bash
    python -m panda_patrol.dbt
    ```
6. Build your dbt models. Note that the `--write-json` flag is needed to write the test results to `target/` which Panda Patrol monitors.
    ```bash
    dbt build --write-json
    ```
6. After the assets finish, you should see the results of the patrols in the Panda Patrol UI at http://localhost:8000. It should look like
    ![Panda Patrol UI](result.gif)

:tada: Congrats! :tada: You have now added Panda Patrols to DBT! See the [documentation](https://github.com/aivanzhang/panda_patrol/wiki) for more information on other features like adjustable parameters, alerting, and silencing.

> [!NOTE]  
> If you get an error like `pydantic.errors.PydanticImportError` when running dbt, you may need to downgrade pydantic to version 1.10.13. Run the following command to do so: 
> ```bash 
> pip install pydantic==1.10.13
> ```