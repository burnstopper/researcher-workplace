from argparse import ArgumentParser
import os
import sys

from loader import load_result, append_to_db, StorageError


def main():
    parser = ArgumentParser("python data-loader-xlsx.py", description="Console application for passing data from xlsx book to sqlite database")
    parser.add_argument("-s" , "--srcdir", default="./")
    parser.add_argument("-d", "--dstdir", default="./")
    parser.add_argument("respondent", help="integer respondent identifier", type=int)
    ns = parser.parse_args(sys.argv[1:])
    srcdir = os.path.realpath(os.path.abspath(ns.srcdir))
    dstdir = os.path.realpath(os.path.abspath(ns.dstdir))
    database = os.path.join(dstdir, "results.sqlite")
    respondent_index = ns.respondent
    respondent_id = f'Респондент_{respondent_index:03d}'
    respondent_file = os.path.join(srcdir, srcdir, f'{respondent_id}.xlsx')
    
    if not os.path.exists(respondent_file):
        print(f"Respondent file {respondent_file} does not exist")
        return 1
    
    if not os.path.isfile(respondent_file):
        print(f"{respondent_file} is not a file")
        return 1
    
    if not os.path.exists(dstdir):
        print(f"Directory {dstdir} does not exist")
        return 1
    
    if not os.path.isdir(dstdir):
        print(f"File {dstdir} is not a directory")
        return 1

    interview_result = load_result(respondent_file, respondent_id=respondent_id)
    try:
        append_to_db(database, interview_result)
    except StorageError as e:
        print("Failed to add interview result due to storage error: {e}")


if __name__ == "__main__":
    sys.exit(main())
else:
    sys.exit(1)
