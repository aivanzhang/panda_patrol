import os
from slack_sdk.webhook import WebhookClient


def send_slack_message(patrolInfo):
    SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK")
    if not SLACK_WEBHOOK:
        print(
            "SLACK_WEBHOOK must be set in the environment in order to send slack emails."
        )
        return

    webhook = WebhookClient(SLACK_WEBHOOK)

    try:
        webhook.send(
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{key.replace('_', ' ').title()}*: {value}",
                    },
                }
                for key, value in patrolInfo.items()
            ]
            + [{"type": "divider"}]
        )
    except Exception as e:
        print("Failed to send slack message.")
        return
