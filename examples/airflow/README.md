# Integrate Panda Patrols with Airflow
This example shows how Panda Patrols integrated with your Airflow DAGs. It creates a basic Airflow DAG with a single task `get_values_task` task that has a list of values (that it has gotten from somewhere) and runs a few tests on that list of values. Patrols are already setup for the tests. 

## Setup
1. Run the install script. This configures Airflow and then installs the Airflow and Panda Patrol packages. Finally it installs the ydata-profiling package.
    ```bash
    chmod +x install.sh
    ./install.sh
    pip install ydata-profiling
    ```
2. Run the start script. This starts the Airflow server using the dags found in the current directory.
    ```bash
    chmod +x start.sh
    ./start.sh
    ```
3. Open the Airflow UI at http://localhost:8080/ and login with the default username and password.
4. Turn on the `get_values_dag` DAG and trigger it. You may need to refresh the page to see the DAG. You should see the patrols running in the logs.
5. After the DAG finishes, you should see the following message in your logs
    ```bash 
    See your Panda Patrol dashboard here: https://panda-patrol.vercel.app/public/public-xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    ```
    Click on the link to see the following dashboard
    ![Panda Patrol UI](result.png)

:tada: Congrats! :tada: You have now added Panda Patrols to Airflow! See the [documentation](https://github.com/aivanzhang/panda_patrol/wiki) for more information on other features like adjustable parameters, alerting, and silencing.
