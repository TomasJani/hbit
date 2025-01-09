import datetime
import typing

from pydantic import BaseModel

if typing.TYPE_CHECKING:
    from hbit_api.domain import models


#########
# CAPEC #
#########


class AttackStepDto(BaseModel):
    step: int
    phase: str
    description: str
    techniques: list[str] = []

    def to_readable_str(self) -> str:
        return f"{self.step}. {self.phase}: {self.description} ({', '.join(self.techniques)})\n"


class SkillDto(BaseModel):
    level: str
    description: str

    def to_readable_str(self) -> str:
        return f"{self.level}: {self.description}\n"


class CAPECDto(BaseModel):
    capec_id: int
    description: str
    extended_description: str
    likelihood_of_attack: str
    severity: str
    execution_flow: list[AttackStepDto] = []
    prerequisites: list[str] = []
    skills_required: list[SkillDto] = []
    resources_required: list[str] = []
    consequences: list[str] = []

    @classmethod
    def from_capec(cls, capec: "models.CAPEC") -> typing.Self:
        return cls(
            capec_id=capec.capec_id,
            description=capec.description,
            extended_description=capec.extended_description,
            likelihood_of_attack=capec.likelihood_of_attack,
            severity=capec.severity,
            execution_flow=capec.execution_flow,  # type: ignore
            prerequisites=capec.prerequisites,
            skills_required=capec.skills_required,  # type: ignore
            resources_required=capec.resources_required,
            consequences=capec.consequences,
        )

    def to_readable_str(self) -> str:
        execution_flow_str = "\n".join(
            [step.to_readable_str() for step in self.execution_flow]
        )
        skills_required_str = "\n".join(
            [skill.to_readable_str() for skill in self.skills_required]
        )
        prerequisites_str = ", ".join(self.prerequisites)
        resources_required_str = ", ".join(self.resources_required)
        consequences_str = ", ".join(self.consequences)

        return (
            f"CAPEC ID: {self.capec_id}\n"
            f"Description: {self.description}\n"
            f"Extended Description: {self.extended_description}\n"
            f"Likelihood of Attack: {self.likelihood_of_attack}\n"
            f"Severity: {self.severity}\n"
            f"Execution Flow:\n{execution_flow_str}\n"
            f"Prerequisites: {prerequisites_str}\n"
            f"Skills Required:\n{skills_required_str}\n"
            f"Resources Required: {resources_required_str}\n"
            f"Consequences: {consequences_str}\n"
        )


#######
# CWE #
#######


class MitigationDto(BaseModel):
    description: str
    effectiveness: str
    effectiveness_notes: str

    def to_readable_str(self) -> str:
        return f"{self.description} ({self.effectiveness})\n"


class DetectionMethodDto(BaseModel):
    method: str
    description: str
    effectiveness: str

    def to_readable_str(self) -> str:
        return f"{self.method}: {self.description} ({self.effectiveness})\n"


class CweDto(BaseModel):
    cwe_id: int
    name: str
    description: str
    extended_description: str
    likelihood_of_exploit: str
    background_details: list[str] = []
    potential_mitigations: list[MitigationDto] = []
    detection_methods: list[DetectionMethodDto] = []
    capecs: list[CAPECDto] = []

    @classmethod
    def from_cwe(cls, cwe: "models.CWE") -> typing.Self:
        return cls(
            cwe_id=cwe.cwe_id,
            name=cwe.name,
            description=cwe.description,
            extended_description=cwe.extended_description,
            likelihood_of_exploit=cwe.likelihood_of_exploit,
            background_details=cwe.background_details,
            potential_mitigations=cwe.potential_mitigations,  # type: ignore
            detection_methods=cwe.detection_methods,  # type: ignore
            capecs=[CAPECDto.from_capec(capec) for capec in cwe.capecs],
        )

    def to_readable_str(self) -> str:
        potential_mitigations_str = "\n".join(
            [mitigation.to_readable_str() for mitigation in self.potential_mitigations]
        )
        detection_methods_str = "\n".join(
            [method.to_readable_str() for method in self.detection_methods]
        )
        capecs_str = "\n".join([capec.to_readable_str() for capec in self.capecs])

        return (
            f"CWE ID: {self.cwe_id}\n"
            f"Name: {self.name}\n"
            f"Description: {self.description}\n"
            f"Extended Description: {self.extended_description}\n"
            f"Likelihood of Exploit: {self.likelihood_of_exploit}\n"
            f"Background Details: {', '.join(self.background_details)}\n"
            f"Potential Mitigations:\n{potential_mitigations_str}\n"
            f"Detection Methods:\n{detection_methods_str}\n"
            f"CAPECs:\n{capecs_str}\n"
        )


#################
# Vulnerability #
#################


class VulnerabilityDto(BaseModel):
    cve_id: str
    description: str
    score: float
    cwes: list[CweDto] = []

    @classmethod
    def from_cve(cls, cve: "models.CVE") -> typing.Self:
        return cls(
            cve_id=cve.cve_id,
            description=cve.description,
            score=cve.cvss["score"],
            cwes=[CweDto.from_cwe(cwe) for cwe in cve.cwes],
        )

    def to_readable_str(self) -> str:
        cwes_str = "\n".join([cwe.to_readable_str() for cwe in self.cwes])

        return (
            f"Vulnerability: {self.cve_id}\n"
            f"Description: {self.description}\n"
            f"Score: {self.score}\n"
            f"CWEs:\n{cwes_str}\n"
        )


class PatchEvaluationDto(BaseModel):
    build: str
    os: str
    name: str

    @classmethod
    def from_patch(cls, patch: "models.Patch") -> typing.Self:
        return cls(
            build=patch.build,
            os=patch.os,
            name=patch.name,
        )

    def to_readable_str(self) -> str:
        return f"Patch: {self.name} ({self.build}) for {self.os}\n"


class DeviceDto(BaseModel):
    manufacturer: str
    name: str
    identifier: str
    models: list[str] = []
    released: datetime.date | None
    discontinued: datetime.date | None

    @classmethod
    def from_device(cls, device: "models.Device") -> typing.Self:
        return cls(
            manufacturer=device.manufacturer.name,
            name=device.name,
            identifier=device.identifier,
            models=device.models,
            released=device.released,
            discontinued=device.discontinued,
        )

    def to_readable_str(self) -> str:
        return (
            f"{self.manufacturer} {self.name}\n"
            f"Identifier: {self.identifier}\n"
            f"Models: {', '.join(self.models)}\n"
            f"Released: {self.released}\n"
            f"Discontinued: {self.discontinued}\n"
        )


class EvaluationDto(BaseModel):
    device: DeviceDto
    patch: PatchEvaluationDto
    vulnerabilities: list[VulnerabilityDto] = []

    @classmethod
    def from_device_and_patch(
        cls, device: "models.Device", patch: "models.Patch"
    ) -> typing.Self:
        return cls(
            device=DeviceDto.from_device(device),
            patch=PatchEvaluationDto.from_patch(patch),
            # include only cves with high score
            vulnerabilities=[
                VulnerabilityDto.from_cve(cve)
                for cve in patch.cves
                if cve.cvss["score"] > 7.0
            ],
        )

    def to_readable_str(self) -> str:
        device_str = self.device.to_readable_str()
        patch_str = self.patch.to_readable_str()
        vulnerabilities_str = "\n".join(
            [v.to_readable_str() for v in self.vulnerabilities]
        )

        return device_str + patch_str + vulnerabilities_str
