# Add Panda Patrols to your Airflow Data Tests
This example shows how Panda Patrols can be added to data tests inside your Airflow DAGs. It creates a basic Airflow DAG with a single task `get_values_task` task that has a list of values (that it has gotten from somewhere) and runs a few tests on that list of values. Patrols are already setup for the tests. 

## Setup
1. Run the install script. This configures Airflow and then installs the Airflow and Panda Patrol packages.
    ```bash
    chmod +x install.sh
    ./install.sh
    ```
2. Run the start script. This starts the Airflow server using the dags found in the current directory.
    ```bash
    chmod +x start.sh
    ./start.sh
    ```
3. Modify the `.env`. Note that the `SMTP_*` and `PATROL_EMAIL` values are dummy values. You will need to replace them with your own values. 
4. Start the Panda Patrol server. This is needed to run the patrols.
    ```bash
    python -m panda_patrol
    ```
5. Open the Airflow UI at http://localhost:8080/ and login with the default username and password.
6. Turn on the `get_values_dag` DAG and trigger it. You may need to refresh the page to see the DAG. You should see the patrols running in the logs.
7. After the DAG finishes, you should see the results of the patrols in the Panda Patrol UI at http://localhost:8000. It should look like
    ![Panda Patrol UI](result.png)

:tada: Congrats! :tada: You have now added Panda Patrols to Airflow! See the [documentation](https://github.com/aivanzhang/panda_patrol/wiki) for more information on other features like adjustable parameters, alerting, and silencing.
