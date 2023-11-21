import os

from SherlockFindingsScraper import SherlockFindingsScraper


class SherlockAudits:
    def __init__(self):
        self.main_dir = "audits"
        self.base_dir = f"{self.main_dir}/sherlock"
        self.user = ""
        self.createDirIfNotExists(self.base_dir)

    def createDirIfNotExists(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def processContests(self, all_findings):
        for contest_data in all_findings:
            self.processContest(all_findings[contest_data])

    def processContest(self, contest_data):
        """
        Process every issue from every contest
        """
        self.createDirIfNotExists(
            os.path.join(self.base_dir, contest_data["contest_name"])
        )
        self.processIssues(contest_data["reports"], contest_data["contest_name"])

    def processIssues(self, reports, contest_name):
        """
        Create contest folder and write readmes
        """
        with open(
            os.path.join(self.base_dir, contest_name, "README.md"), "w"
        ) as contestFile:
            for report in reports:
                original_title = report["title"]
                title = (
                    original_title.replace(" ", "_")
                    .replace("/", "-")
                    .replace("`", "")
                    .replace("'", "")
                )
                severity = report["severity"]
                folder_name = severity + "-" + title
                path = os.path.join(self.base_dir, contest_name, folder_name)
                self.createDirIfNotExists(path)
                #
                # Write the folder issue readme
                issue_link = report["html_url"]
                additional = f"# Original link\n{issue_link}\n"
                rel_link = os.path.join(folder_name, "README.md")
                with open(os.path.join(path, "README.md"), "w") as newFile:
                    newFile.write(additional + report["body"])
                #
                # Write the contest readme
                contest_str = f"\n[{severity}]({rel_link}) - {original_title}\n"
                contestFile.write(contest_str)

    def createSherlockReadme(self, all_findings):
        """
        Create the Sherlock info
        """
        str = f"# Findings in Sherlock \n\n"
        highs = 0
        meds = 0
        for finding in sorted(all_findings):
            contest_name = (
                all_findings[finding]["contest_name"].split("-")[2].capitalize()
            )
            contest_path = all_findings[finding]["contest_name"]
            contest_date = all_findings[finding]["date"].split("-")
            str = (
                str
                + "- "
                + f"[{contest_name}](sherlock/{contest_path}/README.md) - {contest_date[0]}-{contest_date[1]}."
                + "\n"
            )
            highs += all_findings[finding]["highs"]
            meds += all_findings[finding]["mediums"]
        str = (
            str
            + f"\n{highs} Highs and {meds} Medium severity.\n\nI'm available for web3 security consulting and private audits."
        )
        with open(os.path.join(self.base_dir, "README.md"), "w") as f:
            f.write(str)

    def createSh(self, user):
        self.user = user
        crawler = SherlockFindingsScraper()
        all_findings = crawler.getUserFindings(user)
        self.processContests(all_findings)
        self.createSherlockReadme(all_findings)
