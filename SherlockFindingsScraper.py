import json
import requests


class SherlockFindingsScraper:
    def getUserFindings(self, user):
        url = f"https://api.github.com/search/issues?q=is:issue+label:Reward+{user}%20in:title%20org:sherlock-audit"
        reports = json.loads(requests.get(url).text)
        print(f"[+] Searching findings by {user}")
        repositories = {}
        for report in reports["items"]:
            name = report["repository_url"].split("sherlock-audit/")[1]
            if name in repositories:
                repositories[name]["count"] += 1
            else:
                repositories[name] = {}
                repositories[name]["contest_name"] = name
                repositories[name]["reports"] = []
                repositories[name]["count"] = 1
                repositories[name]["highs"] = 0
                repositories[name]["mediums"] = 0
                repositories[name]["date"] = ""
            severity = ""
            for label in report["labels"]:
                if label["name"] == "Medium":
                    severity = "Medium"
                    repositories[name]["mediums"] += 1
                    break
                if label["name"] == "High":
                    severity = "High"
                    repositories[name]["highs"] += 1
                    break
            repositories[name]["reports"].append(
                {
                    "title": report["title"],
                    "body": report["body"],
                    "updated_at": report["updated_at"],
                    "html_url": report["html_url"],
                    "severity": severity,
                }
            )
            repositories[name]["date"] = report["updated_at"]
        for key in repositories.keys():
            print(
                "    [-] Found {} findings in {}".format(
                    repositories[key]["count"], key
                )
            )
        return repositories
