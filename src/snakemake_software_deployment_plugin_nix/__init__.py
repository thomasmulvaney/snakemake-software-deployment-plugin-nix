from typing import Iterable, Tuple, Optional
import subprocess as sp
from snakemake_interface_software_deployment_plugins import (
    EnvBase,
    EnvSpecBase,
    EnvSpecSourceFile,
    SoftwareReport,
)
from snakemake_interface_common.exceptions import WorkflowError
from snakemake_interface_software_deployment_plugins.settings import CommonSettings

from pathlib import Path

from dataclasses import dataclass, field

common_settings = CommonSettings(provides="nix")


@dataclass
class EnvSpec(EnvSpecBase):
    flake_dir: Optional[Path] = None
    name: Optional[str] = None

    def __post_init__(self):
        print("Check directory contains flake:", self.flake_dir)

    def identity_attributes(self) -> Iterable[str]:
        # The identity of the env spec is given by the names of the modules.
        yield "flake_dir"

    def source_path_attributes(self) -> Iterable[str]:
        # no paths involved here
        return ()


class Env(EnvBase):
    def __post_init__(self):
        # Check if the module command is available
        self.check()

    @EnvBase.once
    def check(self) -> None:
        if self.run_cmd("type nix", stdout=sp.PIPE, stderr=sp.PIPE).returncode != 0:
            raise WorkflowError(
                "The 'nix' command is not available. "
                "Please make sure that nix is available on your system."
            )

    def decorate_shellcmd(self, cmd: str) -> str:
        # Decorate given shell command such that it runs within the environment.
        return f"nix develop {self.spec.flake_dir} --command {cmd}"

    def record_hash(self, hash_object) -> None:
        # We just use the contents of the flake.lock file as our unique identifier.
        # This doesn't seem to get called in tests currently..
        with open(self.spec.flake_dir / "flake.lock") as flake_lock:
            hash_object.update(flake_lock.read())

    def report_software(self) -> Iterable[SoftwareReport]:
        # An environment module is just a name, so we cannot report any software here?
        # TODO, maybe there is some way to get software from the module?
        return ()
