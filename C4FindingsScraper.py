import json

import requests


class C4FindingsScraper:
    website_reports_url = (
        "https://code4rena.com/api/functions/get-profile-intensive?wardenHandle=0xbepresent"
    )

    def __init__(self, github_access_token):
        self.github_access_token = github_access_token

    def getAllReportsDownloadUrl(self):
        reports = json.loads(
            requests.post(
                self.website_reports_url,).text)
        return reports['auditHistory']

    def getUserFindings(self, user):
        auditHistory = self.getAllReportsDownloadUrl()
        findings = []
        if not auditHistory:
            return findings
        print(f"[+] Searching findings by {user} on Code4rena")
        for audit in auditHistory:
            result = self.getUserFindingsForReport(user, audit)
            if result:
                findings.append(result)
        return sorted(findings, key=lambda d: d["date"])

    def getUserFindingsForReport(self, user, audit):
        findings = None
        slug = "'"
        if (
            "auditTitle" in audit.keys()
            and "link" in audit.keys()
        ):
            findings = {}
            findings["date"] = audit["date"]
            findings["link"] = audit["link"]
            findings["name"] = audit["link"].split("-findings")[0].split("code-423n4/")[1]
        return findings
