from google.cloud import secretmanager
import base64
import json
from slack_sdk.webhook import WebhookClient
import os

secret_id = f"projects/1049042308740/secrets/rickandmorty-slack-token/versions/2"
client = secretmanager.SecretManagerServiceClient()

response = client.access_secret_version(request={"name": secret_id})
slack_url = response.payload.data.decode("UTF-8")

webhook = WebhookClient(slack_url)


def slack_integration(data, context):
    cloud_build = json.loads(base64.b64decode(data["data"]))

    print(f"cloud_build!!: {cloud_build}")

    if cloud_build["status"] not in ["SUCCESS", "FAILURE"]:
        return

    slack_message = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Build Succeeded. :white_check_mark:"
                    if cloud_build["status"] == "SUCCESS"
                    else "Build Failed. :red_circle:",
                    "emoji": True,
                },
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": "*Project*: Todo App"},
                    {"type": "mrkdwn", "text": "*Branch*: main"},
                    {
                        "type": "mrkdwn",
                        "text": f"*Build*: \n*<{cloud_build['logUrl']}|{cloud_build['id'][:-10]}>*",
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"""
                        *Repo*: *<{cloud_build['substitutions']['REPO_NAME']}>*
                        *Branch*: *<{cloud_build['substitutions']['BRANCH_NAME']}>*
                        *Commit*: *<{cloud_build['substitutions']['SHORT_SHA']}>*
                        """,
                    },
                ],
            },
            {"type": "divider"},
        ]
    }
    webhook.send(**slack_message)
