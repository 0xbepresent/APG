import json
import os

from dotenv import load_dotenv
import requests

from C4FindingsScraper import C4FindingsScraper

load_dotenv()


class C4Audits:
    def __init__(self):
        self.main_dir = "audits"
        self.base_dir = f"{self.main_dir}/c4"
        self.org = "code-423n4"
        self.user = ""
        self.api_url_template = (
            "https://api.github.com/repos/##ORG##/##REPO##/issues/##ISSUE##"
        )
        self.raw_url_template = "https://raw.githubusercontent.com/code-423n4/##REPO##/main/data/##USER##-##TYPE##.md"
        self.createDirIfNotExists(self.base_dir)
        self.github_access_token = os.getenv('GITHUB_ACCESS_TOKEN')

    def createDirIfNotExists(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def processContests(self, all_findings):
        results = []
        for contest_data in all_findings:
            results.append(self.processContest(contest_data))
        return results

    def processQAGas(self, repo, name, issue, issue_text):
        type = "G"
        folder_name = "GAS"
        if issue_text.endswith("Q.md"):
            type = "Q"
            folder_name = "QA"
        url = (
            self.raw_url_template.replace("##REPO##", repo)
            .replace("##USER##", self.user)
            .replace("##TYPE##", type)
        )
        md = requests.get(url).text
        file_name = "README.md"
        path = os.path.join(self.base_dir, name, folder_name)
        self.createDirIfNotExists(path)
        additional = f"# Original link\n{issue}\n\n"
        with open(os.path.join(path, file_name), "w") as newFile:
            newFile.write(additional + md)
        return (f"[[{folder_name}]]({os.path.join(folder_name, file_name)})", 0)

    def getSeverityFromLables(self, data):
        severity = ""
        for label in data["labels"]:
            if label["name"].startswith("3"):
                severity = "[HIGH]"
            elif label["name"].startswith("2"):
                severity = "[MEDIUM]"
            elif label["name"].startswith("QA"):
                severity = "[QA]"
        return severity

    def processHighMid(self, repo, name, issueNum, issue):
        url = (
            self.api_url_template.replace("##ORG##", self.org)
            .replace("##REPO##", repo)
            .replace("##ISSUE##", issueNum)
        )
        print(url)
        data = json.loads(
            requests.get(
                url,
                headers={"Authorization": "Bearer {}".format(self.github_access_token)} if self.github_access_token else {}).text)
        md = ""
        try:
            md = data["body"]
        except KeyError:
            print(f"Error while downloading reports, please see the Github rate limits...")
            return("", "")
        if md is None: return ('', '')
        if f"{self.user}-Q" in md:
            return self.processQAGas(repo, name, issue, f"{self.user}-Q.md")
        elif f"{self.user}-G" in md:
            return self.processQAGas(repo, name, issue, f"{self.user}-G.md")
        original_title = data["title"]
        severity = self.getSeverityFromLables(data)
        folder_name = severity + "-" + str(data["id"])
        path = os.path.join(self.base_dir, name, folder_name)
        self.createDirIfNotExists(path)
        additional = f"# Original link\n{issue}\n"
        rel_link = os.path.join(folder_name, "README.md")
        with open(os.path.join(path, "README.md"), "w") as newFile:
            newFile.write(additional + md)
        return (f"[{severity}]({rel_link}) - {original_title}", severity)

    def processIssues(self, issues, name):
        results = []
        repo = f"{name}-findings"
        highs = 0
        meds = 0
        issueNum = issues['link'].split("issues/")[-1]
        if issueNum.endswith("md"):
            result = self.processQAGas(repo, name, issues['link'], issueNum)
        else:
            result = self.processHighMid(repo, name, issueNum, issues['link'])
            if result[1] == "[HIGH]":
                highs += 1
            if result[1] == "[MEDIUM]":
                meds += 1
        results.append(result[0])
        return [results, highs, meds]

    def createContestREADME(self, name):
        str = f"# Findings for {name} \n\n"
        with open(os.path.join(self.base_dir, name, "README.md"), "w") as f:
            f.write(str)

    def processContest(self, contest_data):
        self.createDirIfNotExists(os.path.join(self.base_dir, contest_data['name']))
        results = self.processIssues(contest_data, contest_data['name'])
        self.createContestREADME(contest_data['name'])
        return (contest_data['name'], len(results[0]), results[1], results[2])

    def createC4(self, user):
        self.user = user
        crawler = C4FindingsScraper(self.github_access_token)
        all_findings = crawler.getUserFindings(user)
        results = self.processContests(all_findings)
