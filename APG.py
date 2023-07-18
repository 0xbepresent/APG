import argparse
from C4Audits import C4Audits
from SherlockAudits import SherlockAudits

argParser = argparse.ArgumentParser()
argParser.add_argument("-c4", "--c4user", help="Your Code4rena handler")
argParser.add_argument("-sh", "--sherlockuser", help="Your Sherlock handler")
args = argParser.parse_args()


def main():
    if args.c4user:
        c4 = C4Audits()
        c4.createC4(args.c4user)
    if args.sherlockuser:
        sh = SherlockAudits()
        sh.createSh(args.sherlockuser)


if __name__ == "__main__":
    main()
