from Pipeline.bioinformatics.tools.samtools.samtoolslatest import SamToolsLatest
from Pipeline.bioinformatics.tools.samtools.sort.sortbase import SamToolsSortBase


class SamToolsSortLatest(SamToolsLatest, SamToolsSortBase):
    pass


if __name__ == "__main__":
    print(SamToolsSortLatest().help())