from janis_core import Array, Boolean, Int

from janis_bioinformatics.data_types import BamBai
from janis_bioinformatics.tools.bioinformaticstoolbase import BioinformaticsWorkflow
from janis_bioinformatics.tools.gatk4 import (
    Gatk4MergeSamFiles_4_0,
    Gatk4MarkDuplicates_4_0,
)


class MergeAndMarkBams_4_0(BioinformaticsWorkflow):
    def id(self):
        return "mergeAndMarkBams"

    def friendly_name(self):
        return "Merge and Mark Duplicates"

    def version(self):
        return "4.0.12"

    def tool_provider(self):
        return "common"

    def constructor(self):

        self.input("bams", Array(BamBai()))
        self.input("createIndex", Boolean, default=True)
        self.input("maxRecordsInRam", Int, default=5000000)

        self.step(
            "mergeSamFiles",
            Gatk4MergeSamFiles_4_0(
                bams=self.bams,
                useThreading=True,
                createIndex=self.createIndex,
                maxRecordsInRam=self.maxRecordsInRam,
                validationStringency="SILENT",
            ),
        )

        self.step(
            "markDuplicates",
            Gatk4MarkDuplicates_4_0(
                bam=self.mergeSamFiles.out,
                createIndex=self.createIndex,
                maxRecordsInRam=self.maxRecordsInRam,
            ),
        )
        self.output("out", source=self.markDuplicates.out)


if __name__ == "__main__":
    MergeAndMarkBams_4_0().translate("wdl")
