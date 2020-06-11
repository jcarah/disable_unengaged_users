import looker_sdk
from looker_sdk import models
import json
import csv
import argparse
from time import strftime, localtime
from pprint import pprint as pp

sdk = looker_sdk.init31()


def get_unengaged_users(day_threshold: int):
    """Fetch a list of unengaged users based on suppplied day threshold"""
    unengaged_users_query = models.WriteQuery(
        view="user",
        fields=[
            "user.id",
            "user.name",
            "user.email",
            "user.created_date",
            "user_facts.last_ui_login_date",
            "history.most_recent_query_date"
        ],
        filters={
            "user.created_date": f"before {day_threshold} days ago",
            "user_facts.is_looker_employee": "No",
            "user_facts.last_api_login_date": f"before {day_threshold} days ago,NULL",
            "user_facts.last_ui_login_date": f"before {day_threshold} days ago,NULL",
            "user.is_disabled": "No",
            "user_facts.is_admin": "No"
        },
        sorts=["user_facts.last_ui_login_date"],
        model="system__activity"
    )
    unengaged_users = json.loads(sdk.run_inline_query(
        result_format="json", body=unengaged_users_query))
    for i in unengaged_users:
        ran_at = strftime("%Y-%m-%d %H:%M:%S", localtime())
        i["ran_at"] = ran_at
    return unengaged_users


def write_unengaged_users(unengaged_users: list, output_csv_name: str):
    """Output list of users to be disabled to a csv"""
    try:
        with open(output_csv_name, "a") as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=list(unengaged_users[0].keys())
            )
            writer.writeheader()
            for data in unengaged_users:
                writer.writerow(data)
    except IOError:
        print("I/O error")


def disable_user(user_id: int):
    user = models.WriteUser(is_disabled=True)
    sdk.update_user(user_id, body=user)


def main():
    parser = argparse.ArgumentParser(
        description="Find and disable unengaged Looker users.")
    parser.add_argument("--days", "-d", type=int,required=True,
                        help="The number of days of inactivity required to be disabled (e.g. 90 days).")
    parser.add_argument("--test", "-t",dest="test", action="store_true", required=False,
                        help="Use this flag to see unengaged users but not disable them.")
    args = parser.parse_args()
    unengaged_users = get_unengaged_users(args.days)
    if args.test:
        print("Running script in test mode. Unengaged users:")
        pp(unengaged_users)
    else:
        if len(unengaged_users) > 0:
            for user in unengaged_users:
                print(f"disabling user_id {user['user.id']}")
                disable_user(user["user.id"])
                csv_name = "disabled_users.csv"
                print(f"Disabled users outputted to {csv_name}.")
                write_unengaged_users(unengaged_users, csv_name)
        else:
            print("No unengaged users to disable.")

main()
