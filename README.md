# APG (Auditor Profile Generator)

Welcome!

This tool will scrape web3 audit platforms according to supplied handles and generate a profile of findings.

### Use-cases
1. Gather all your findings in one place as a resume/profile to present to your clients.
2. Research others by supplying their handles and learning from their patterns.

### Dependencies
1. Python3
2. `$ pip3 install -r requirements.txt`

### Github access token
It would recommended to add a [Github personal access token](https://docs.github.com/en/rest/overview/authenticating-to-the-rest-api?apiVersion=2022-11-28) in order to avoid `rate limit errors`. The token should be in the `.env` file:

`$ cp .env.example .env`

### Execution

`python3 APG.py -c4 <C4 Handle> -sh <Sherlock Handle>`

The output will be under `audits/c4` and `audits/sherlock`. You can create your custom `README.md` on the root folder.

### Notes
Currently the tool only support Code4rena and Sherlock.

Developed by 0xdeadbeef and modified by 0xbepresent.

