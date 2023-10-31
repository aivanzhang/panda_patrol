import requests
import os
from panda_patrol.constants import DEFAULT_PANDA_PATROL_URL
from panda_patrol.headers.get_headers import get_headers


def generate_data_tests(
    columns: list, data_preview: str, context: str, output_file: str
):
    """
    Generate data tests given the column titles, a preview of the data and the additional and optional context around these data tests.
    Note this only works if you have an account at https://panda-patrol.vercel.app/.

    :param columns: The columns titles of the data
    :param data_preview: The preview of the data
    :param context: The context of the data
    :param output_file: The output file to save the generated data tests to

    """

    patrol_url = os.environ.get("PANDA_PATROL_URL")
    secret_key = os.environ.get("PANDA_PATROL_SECRET_KEY")

    if patrol_url == DEFAULT_PANDA_PATROL_URL and not secret_key.startswith("public-"):
        if os.path.isfile(output_file):
            print(
                f"The file {output_file} already exists. Please delete the file or change the output file name to regenerate data tests."
            )
            return

        payload = {
            "columns": ",".join(columns),
            "data_preview": f"{data_preview}",
            "context": context,
        }
        response = requests.post(
            f"{patrol_url}/generate_tests", json=payload, headers=get_headers()
        )
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(e)

        generated_tests_str = response.json()["generated_tests"]

        with open(output_file, "w+") as f:
            f.write(generated_tests_str)
    else:
        print(
            "You are not using the default panda patrol url or you are using a public key. You will not be able to generate data tests. Create an account at https://panda-patrol.vercel.app/ to generate data tests."
        )
