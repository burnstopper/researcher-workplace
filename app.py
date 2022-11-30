from argparse import ArgumentParser
from enum import Enum
import os
import sys
from typing import List

from loader import load_result, append_to_db, StorageError


class Result(Enum):
    SUCCESS               = 0
    BAD_ARGUMENTS         = 1
    GENERIC_ERROR         = 2


def main():
    parser = ArgumentParser("python data-loader-xlsx.py", description="Console application for passing data from xlsx book to sqlite database")
    parser.add_argument("-f" , "--file")
    parser.add_argument("-d", "--dir")
    parser.add_argument("-o", "--outdir", default="./")
    ns = parser.parse_args(sys.argv[1:])

    if (ns.file is not None) and (ns.dir is not None):
        print(f"Cannot run if both of arguments -f and -d at the same time")
        return Result.BAD_ARGUMENTS
    
    if (ns.file is None) and (ns.dir is None):
        print(f"Cannot run if no arguments specified")
        return Result.BAD_ARGUMENTS

    if ns.file is not None:
        srcfile = os.path.abspath(ns.file)
        srcdir = None
    
    if ns.dir is not None:
        srcfile = None
        srcdir = os.path.abspath(ns.dir)

    database = os.path.join(os.path.abspath(ns.outdir), "results.sqlite")
    
    if srcfile is not None:
        if not os.path.exists(srcfile):
            print(f"Respondent file {srcfile} does not exist")
            return Result.BAD_ARGUMENTS
        if not os.path.isfile(srcfile):
            print(f"'{srcfile}' is not a file")
            return Result.BAD_ARGUMENTS
    
    if srcdir is not None:
        if not os.path.exists(srcdir):
            print(f"Respondent dir {srcdir} does not exist")
            return Result.BAD_ARGUMENTS
        if not os.path.isdir(srcdir):
            print(f"'{srcdir}' is not a directory")
            return Result.BAD_ARGUMENTS

    for respondent_file in get_respondents_files(filepath=srcfile, dirpath=srcdir):
        respondent_id = extract_respondent_id(respondent_file)
        interview_result = load_result(respondent_file, respondent_id=respondent_id)
        try:
            append_to_db(database, interview_result)
        except StorageError as e:
            print(f"Failed to add interview result due to storage error: {e}")
            return Result.GENERIC_ERROR
    
    return Result.SUCCESS


def get_respondents_files(filepath: str = None, dirpath: str = None) -> List[str]:
    assert (filepath is not None) or (dirpath is not None)
    if filepath is not None:
        return [filepath]
    return list(
        map(lambda p: os.path.join(dirpath, p),
            os.listdir(
                dirpath
            )
        )
    )


def extract_respondent_id(filepath: str) -> str:
    basename = os.path.basename(filepath)
    return os.path.splitext(basename)[0]


if __name__ == "__main__":
    sys.exit(main().value)
else:
    sys.exit(1)
