import sys
import os
from pathlib import Path
from datetime import datetime


allowed_names = {'download_TROPOMI', 'download_blended_TROPOMI'}
buckets = {'download_TROPOMI': "meeo-s5p",
           'download_blended_TROPOMI': "blended-tropomi-gosat-methane"}


def check_download(datadir, fn_script, start, end):
    """
    Check whether the required TROPOMI files need to be downloaded for the inversion.

    Arguments
        datadir  [str | Path] : the local directory where the TROPOMI files are stored.
        fn_script       [str] : the name of the download script to use
                               {download_TROPOMI, download_blended_TROPOMI}
        start      [datetime] : start date of data download (%Y%m%d)
        end        [datetime] : end date of data download (%Y%m%d)

    Returns
        needs_download [bool] : False if all files are present in the folder; True otherwise.
    """
    assert fn_script in allowed_names, f"{fn_script} is not a recognized sub-module"

    if download_script in allowed_names:
        mod = __import__(download_script)

    paths = mod.get_s3_paths(start, end, buckets[fn_script])
    files = [os.path.basename(pn) for pn in paths]

    exists = [os.path.exists(Path(datadir, fn)) for fn in files]

    return all(exists)


if __name__ == "__main__":
    sys.path.append(os.path.join(os.environ['IMI_HOME'], 'src/utilities'))

    sat_datadir = sys.argv[1]
    download_script = os.path.basename(sys.argv[2]).split('.py')[0]

    start_date = datetime.strptime(sys.argv[3], "%Y%m%d")
    end_date = datetime.strptime(sys.argv[4], "%Y%m%d")

    downloaded = check_download(sat_datadir, download_script, start_date, end_date)
    sys.exit(not downloaded)
