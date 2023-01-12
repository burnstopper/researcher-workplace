from argparse import ArgumentParser
from enum import Enum
import os
import sys
from typing import List

from loader import(
    append_to_db,
    InterviewResult,
    load_gform_results,
    load_xls_result,
    StorageError
)


class Result(Enum):
    SUCCESS               = 0
    BAD_ARGUMENTS         = 1
    GENERIC_ERROR         = 2


def main():
    parser = ArgumentParser("python data-loader-xlsx.py",
                            description="Console application for passing data from xlsx book to sqlite database")
    parser.add_argument("-f" , "--file")
    parser.add_argument("-d", "--dir")
    parser.add_argument("-o", "--outdir", default="./")
    parser.add_argument("-k", "--key", help="Key of the source", type=str, dest="key", required=True)
    parser.add_argument("--gform", help="Parse result as google form", dest="gform", action='store_true')
    parser.add_argument("--xls", help="Parse result as xls", dest="xls", action='store_true')
    ns = parser.parse_args(sys.argv[1:])
    source_key = ns.key

    if (ns.file is not None) and (ns.dir is not None):
        print(f"Cannot run if both of arguments -f and -d at the same time")
        return Result.BAD_ARGUMENTS
    
    if (ns.file is None) and (ns.dir is None):
        print(f"Cannot run if arguments -f and -d are missing")
        return Result.BAD_ARGUMENTS

    if ns.file is not None:
        srcfile = os.path.abspath(ns.file)
        srcdir = None
    
    if ns.dir is not None:
        srcfile = None
        srcdir = os.path.abspath(ns.dir)

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

    if ns.gform:
        if srcfile is None:
            print("srcfile need to specified for loading from gform")
            return Result.BAD_ARGUMENTS
        results = load_from_gform(source_key, srcfile)
    elif ns.xls:
        results = load_from_xls(source_key, srcfile, srcdir)
    else:
        print("Please select type of source table: it is `--xls` or `--gform`")
        return Result.BAD_ARGUMENTS

    try:
        dump_to_db(results, ns.outdir)
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


def load_from_gform(srckey: str, srcfile: str) -> List[InterviewResult]:
    return load_gform_results(srcfile, srckey)


def load_from_xls(srckey: str, srcfile: str = None, srcdir: str = None) -> List[InterviewResult]:
    def extract_respondent_id(filepath: str) -> str:
        basename = os.path.basename(filepath)
        return os.path.splitext(basename)[0]

    resp_files = get_respondents_files(srcfile, srcdir)
    loaded_results = []
    for f in resp_files:
        resp_id = extract_respondent_id(f)
        interview_result = load_xls_result(f, key=srckey, respondent_id=resp_id)
        loaded_results.append(interview_result)
    return loaded_results


def dump_to_db(res: List[InterviewResult], output_dir: str):
    database_file = os.path.join(os.path.abspath(output_dir), "results.sqlite")
    for r in res:
        append_to_db(database_file, r)


if __name__ == "__main__":
    sys.exit(main().value)
else:
    sys.exit(1)
