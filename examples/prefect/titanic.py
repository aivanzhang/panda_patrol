import requests
import pandas as pd
from io import StringIO
from datetime import timedelta
from prefect import flow, task
from ydata_profiling import ProfileReport
from panda_patrol.patrols import patrol_group
from panda_patrol.parameters import adjustable_parameter
from panda_patrol.profilers import save_report


@task(retries=3)
def fetch_data():
    """
    Fetch the Titanic dataset using requests.
    """
    url = (
        "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    )
    response = requests.get(url)
    data = pd.read_csv(StringIO(response.text))

    with patrol_group("Titanic Dataset") as patrol:

        @patrol("Age")
        def age_checks(patrol_id):
            assert data["Age"].notnull().all(), "Missing values in age column"
            assert data["Age"].min() >= 0, "Negative values in age column"
            assert data["Age"].max() <= 100, "Age values above 100"
            expected_median = int(
                adjustable_parameter("expected_median_age", patrol_id, 40)
            )
            assert (
                data["Age"].median() <= expected_median
            ), f"Median age above {expected_median}"

        @patrol("Sex")
        def sex_checks(patrol_id):
            assert set(data["Sex"]) == {
                "male",
                "female",
            }, "Unexpected values in sex column"

        @patrol("Fare")
        def fare_checks(patrol_id):
            assert (data["Fare"] >= 0).all(), "Negative values in fare column"
            assert data["Fare"].notnull().all(), "Missing values in fare column"
            expected_median = int(
                adjustable_parameter("expected_median_fare", patrol_id, 30)
            )
            assert (
                data["Fare"].median() <= expected_median
            ), f"Median fare above {expected_median}"
            expected_max = int(
                adjustable_parameter("expected_max_fare", patrol_id, 100)
            )
            assert data["Fare"].max() <= expected_max, f"Max fare above {expected_max}"

    report = ProfileReport(data, title="Titanic Dataset")
    # Save the report to Panda Patrol
    save_report(report.to_html(), "Titanic Dataset", "Profiling Report", "html")

    return data


@task
def transform_data(data):
    """
    Transform the Titanic dataset.
    """
    data["Age"].fillna(data["Age"].median(), inplace=True)
    data["Sex"] = data["Sex"].map({"male": 1, "female": 0})
    data.drop(columns=["Name", "Ticket"], inplace=True)

    report = ProfileReport(data, title="Titanic Dataset")
    # Save the report to Panda Patrol
    save_report(
        report.to_html(), "Titanic Dataset", "Transformed Data Profiling Report", "html"
    )

    return data


@flow(name="Titanic", log_prints=True)
def run_titanic_analysis():
    """
    Fetch and transform the Titanic dataset.
    """
    data = fetch_data()
    transform_data(data)


if __name__ == "__main__":
    # create your first deployment
    run_titanic_analysis.serve(name="run_titanic_analysis")
