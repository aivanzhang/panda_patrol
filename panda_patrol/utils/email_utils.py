import os
import smtplib
from email.message import Message


def send_email(subject, body, to_email):
    PATROL_EMAIL = os.environ.get("PATROL_EMAIL")
    SMTP_USER = os.environ.get("SMTP_USER")
    SMTP_PASS = os.environ.get("SMTP_PASS")
    SMTP_SERVER = os.environ.get("SMTP_SERVER")
    SMTP_PORT = os.environ.get("SMTP_PORT")
    if (
        not SMTP_USER
        or not SMTP_PASS
        or not SMTP_SERVER
        or not SMTP_PORT
        or not PATROL_EMAIL
    ):
        print(
            "SMTP_USER, SMTP_PASS, SMTP_SERVER, and SMTP_PORT must be set in the environment in order to send emails."
        )
        return

    msg = Message()
    msg["From"] = PATROL_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.add_header("Content-Type", "text/html")
    msg.set_payload(body)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(PATROL_EMAIL, [to_email], msg.as_string())


def send_failure_email(name, email, patrolInfo):
    message = f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                h2 {{ color: red; }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                }}
                table, th, td {{
                    border: 1px solid black;
                    padding: 8px;
                    text-align: left;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
            </style>
        </head>
        <body>
            <p>Hi {name},</p>
            <h2>Your panda patrol failed.</h2>
            <table>
                <tr>
                    <th>Attribute</th>
                    <th>Details</th>
                </tr>
                <tr>
                    <td>Patrol Group</td>
                    <td>{patrolInfo["patrol_group"]}</td>
                </tr>
                <tr>
                    <td>Patrol</td>
                    <td>{patrolInfo["patrol"]}</td>
                </tr>
                <tr>
                    <td>Severity</td>
                    <td>{patrolInfo["severity"]}</td>
                </tr>
                <tr>
                    <td>Status</td>
                    <td>{patrolInfo["status"]}</td>
                </tr>
                <tr>
                    <td>Logs</td>
                    <td>{patrolInfo["logs"]}</td>
                </tr>
                <tr>
                    <td>Return Value</td>
                    <td>{patrolInfo["return_value"]}</td>
                </tr>
                <tr>
                    <td>Start Time</td>
                    <td>{patrolInfo["start_time"]}</td>
                </tr>
                <tr>
                    <td>End Time</td>
                    <td>{patrolInfo["end_time"]}</td>
                </tr>
                <tr>
                    <td>Exception</td>
                    <td>{patrolInfo["exception"]}</td>
                </tr>
            </table>
        </body>
    </html>
    """
    send_email("Panda Patrol Failure", message, email)
