import json
import os
import time

import requests


def get_jira_issue(issue_key, email, api_token):
    url = f"https://rubinobs.atlassian.net/rest/api/latest/issue/DM-{issue_key}"
    auth = requests.auth.HTTPBasicAuth(email, api_token)
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, auth=auth, headers=headers)
    if response.status_code == 200:
        issue_data = response.json()

        return issue_data


def extract_reviewer_from_customfield(jira_data):
    # Extract reviewer information from customfield_10048 if available
    reviewers = jira_data["fields"].get("customfield_10048", [])
    if reviewers:
        # Extract the display name(s) of the reviewer(s) into a list
        return [
            reviewer.get("displayName", "Reviewer not found") for reviewer in reviewers
        ]
    return ["No reviewer assigned"]


def extract_related_issues(jira_data):
    related_issues = []
    issue_links = jira_data["fields"].get("issuelinks", [])

    for link in issue_links:
        issue_relation = {}
        if "inwardIssue" in link:
            issue_relation = {
                "key": link["inwardIssue"].get("key", ""),
                "summary": link["inwardIssue"]["fields"].get("summary", "No summary"),
                "status": link["inwardIssue"]["fields"]["status"].get(
                    "name", "Unknown status"
                ),
                "relationship": link["type"].get("outward", "Unknown relation"),
            }
        elif "outwardIssue" in link:
            issue_relation = {
                "key": link["outwardIssue"].get("key", ""),
                "summary": link["outwardIssue"]["fields"].get("summary", "No summary"),
                "status": link["outwardIssue"]["fields"]["status"].get(
                    "name", "Unknown status"
                ),
                "relationship": link["type"].get("outward", "Unknown relation"),
            }
        related_issues.append(issue_relation)

    return related_issues


def extract_components(jira_data):
    components = jira_data["fields"].get("components", [])
    return [component.get("name", "No component") for component in components]


def extract_comments(jira_data):
    comments = jira_data["fields"].get("comment", {}).get("comments", [])
    return [
        {
            "author": comment["author"].get("displayName", "Unknown author"),
            "body": comment.get("body", "No comment body"),
        }
        for comment in comments
    ]


def extract_parent_issue(jira_data):
    parent_issue = jira_data["fields"].get("parent", None)
    if parent_issue:
        return {
            "key": parent_issue.get("key", ""),
            "summary": parent_issue["fields"].get("summary", "No summary"),
            "status": parent_issue["fields"]["status"].get("name", "Unknown status"),
        }
    return None


def reformat_jira_data(jira_data):
    # Extract main fields from the original Jira data structure
    simplified_data = {
        "key": jira_data.get("key", ""),
        "summary": jira_data["fields"].get("summary", ""),
        "description": jira_data["fields"].get("description", ""),
        "status": jira_data["fields"]["status"].get("name", "Unknown"),
        "assignee": jira_data["fields"]
        .get("assignee", {})
        .get("displayName", "Unassigned"),
        "reviewers": extract_reviewer_from_customfield(jira_data),
        "reporter": jira_data["fields"]
        .get("reporter", {})
        .get("displayName", "Unknown"),
        "created": jira_data["fields"].get("created", ""),
        "updated": jira_data["fields"].get("updated", ""),
        "resolution": jira_data["fields"]
        .get("resolution", {})
        .get("name", "Unresolved"),
        "labels": jira_data["fields"].get("labels", []),
        "attachments": [
            {
                "filename": attachment.get("filename", ""),
                "url": attachment.get("content", ""),
            }
            for attachment in jira_data["fields"].get("attachment", [])
        ],
        "comments": extract_comments(jira_data),
        "parent_issue": extract_parent_issue(jira_data),  # Parent issue extraction
        "related_issues": extract_related_issues(
            jira_data
        ),  # Related issues extraction
        "components": extract_components(jira_data),  # Extract components
        "team": jira_data["fields"]
        .get("customfield_10056", {})
        .get("value", "No team"),  # Extract team
        "project": jira_data["fields"]
        .get("project", {})
        .get("name", "No project"),  # Extract project name
    }

    return simplified_data


def write_to_file(results, folder="JIRA tickets"):
    # Ensure the folder exists
    if not os.path.exists(folder):
        os.makedirs(folder)

    ticket_key = results["key"]  # Assuming 'key' is the Jira ticket key
    file_path = os.path.join(folder, f"{ticket_key}.json")  # Create the JSON file path

    # Write the individual result to a JSON file
    with open(file_path, "w") as f:
        json.dump(results, f, indent=4)  # Writing with indentation for readability


def fetch_ticket(ticket, email, api_token):
    jira_data = get_jira_issue(ticket, email, api_token)
    return reformat_jira_data(jira_data)


def retry_fetch_ticket(ticket, email, api_token, max_retries):
    """Fetch the ticket with retry logic."""
    for attempt in range(max_retries):
        try:
            result = fetch_ticket(ticket, email, api_token)
            return result
        except Exception:
            # print(f"Error fetching ticket {ticket}: {exc}")
            if attempt + 1 == max_retries:
                raise  # Raise the error if max retries reached
            time.sleep(2**attempt + 2)  # Exponential backoff
