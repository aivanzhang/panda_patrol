from pyod.models.ecod import ECOD
from panda_patrol.patrols import patrol_group


def basic_anomaly_detection(
    group_name,
    expected_data,
    actual_data,
    patrol_name="Basic Anomaly Detection",
    dbt_model_uri=None,
):
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
