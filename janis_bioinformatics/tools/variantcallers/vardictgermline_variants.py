from janis_core import File, String, Float
from janis_unix.tools import UncompressArchive

from janis_bioinformatics.data_types import FastaWithDict, BamBai, Bed
from janis_bioinformatics.tools import BioinformaticsWorkflow
from janis_bioinformatics.tools.bcftools import BcfToolsAnnotate_1_5
from janis_bioinformatics.tools.common import SplitMultiAllele
from janis_bioinformatics.tools.htslib import TabixLatest
from janis_bioinformatics.tools.vardict import VarDictGermline_1_6_0
from janis_bioinformatics.tools.pmac.trimiupac.versions import TrimIUPAC_0_0_5
from janis_bioinformatics.tools.vcftools import VcfToolsvcftoolsLatest


class VardictGermlineVariantCaller(BioinformaticsWorkflow):
    def id(self):
        return "vardictGermlineVariantCaller"

    def friendly_name(self):
        return "Vardict Germline Variant Caller"

    def tool_provider(self):
        return "Variant Callers"

    def version(self):
        return "v0.1.1"

    def constructor(self):

        self.input("bam", BamBai)
        self.input("intervals", Bed)

        self.input("sample_name", String)
        self.input("allele_freq_threshold", Float, default=0.5)
        self.input("header_lines", File)

        self.input("reference", FastaWithDict)

        self.step(
            "vardict",
            VarDictGermline_1_6_0(
                intervals=self.intervals,
                bam=self.bam,
                reference=self.reference,
                sampleName=self.sample_name,
                var2vcfSampleName=self.sample_name,
                alleleFreqThreshold=self.allele_freq_threshold,
                var2vcfAlleleFreqThreshold=self.allele_freq_threshold,
                chromNamesAreNumbers=True,
                vcfFormat=True,
                chromColumn=1,
                regStartCol=2,
                geneEndCol=3,
            ),
        )
        self.step(
            "annotate",
            BcfToolsAnnotate_1_5(vcf=self.vardict.out, headerLines=self.header_lines),
        )
        self.step("tabixvcf", TabixLatest(inp=self.annotate.out))

        self.step("uncompressvcf", UncompressArchive(file=self.annotate.out))
        self.step(
            "splitnormalisevcf",
            SplitMultiAllele(vcf=self.uncompressvcf.out, reference=self.reference),
        )
        self.step("trim", TrimIUPAC_0_0_5(vcf=self.splitnormalisevcf.out))
        self.step(
            "filterpass",
            VcfToolsvcftoolsLatest(
                vcf=self.trim.out,
                removeFileteredAll=True,
                recode=True,
                recodeINFOAll=True,
            ),
        )

        self.output("variants", source=self.tabixvcf.out)
        self.output("out", source=self.filterpass.out)


if __name__ == "__main__":
    v = VardictGermlineVariantCaller()
    v.translate("wdl", with_resource_overrides=False)
    # print(v.generate_resources_file("wdl", { "CaptureType": "targeted" }))
