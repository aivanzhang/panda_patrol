from pyod.models.ecod import ECOD
from panda_patrol.patrols import patrol_group


def basic_anomaly_detection(
    group_name,
    expected_data,
    actual_data,
    patrol_name="Basic Anomaly Detection",
    dbt_model_uri=None,
):
    """
    A basic anomaly detection patrol that uses the ECOD algorithm from the pyod library.
    Parameters
    ----------
    group_name: str - Name of the patrol group.
    expected_data - Input samples with numpy array of shape (n_samples, n_features)
    actual_data - The training input samples with numpy array of shape (n_samples, n_features)
    patrol_name: str (Default: "Basic Anomaly Detection") - The name of the patrol.
    dbt_model_uri=None: str (Default: None. For DBT use only) - The dbt model uri of the Python model that is being tested. For example models/base/first_model.py would be base/first_model. This is used to link the data tests to the dbt model so that Python code related to a DBT test is stored. If excluded, then the data test code will not be stored in the database.
    """
    with patrol_group(group_name, dbt_model_uri) as patrol:

        @patrol(patrol_name)
        def basic_anomaly_detection_patrol():
            ecod = ECOD()
            ecod.fit(expected_data)
            detected_anomalies = ecod.predict(actual_data)
            if detected_anomalies.any():
                raise Exception(
                    f"Anomalies detected: {actual_data[detected_anomalies == 1].tolist()}"
                )
