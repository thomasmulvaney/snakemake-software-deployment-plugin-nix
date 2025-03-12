from typing import Iterable, Optional
import subprocess as sp
from snakemake_interface_software_deployment_plugins import (
    EnvBase,
    EnvSpecBase,
    SoftwareReport,
)
from snakemake_interface_common.exceptions import WorkflowError
from snakemake_interface_software_deployment_plugins.settings import CommonSettings

from pathlib import Path

from dataclasses import dataclass

common_settings = CommonSettings(provides="nix")


@dataclass
class EnvSpec(EnvSpecBase):
    flake_file: Optional[Path] = None

    # Check there is indeed a flake.nix file in the directory
    def __post_init__(self):
        if self.flake_file.name != "flake.nix":
            raise WorkflowError("Flake file must be called flake.nix")
        if not self.flake_file.is_file():
            raise WorkflowError(
                f"The specified flake file {self.flake_file} does not exist"
            )

    def identity_attributes(self) -> Iterable[str]:
        return ["flake_file"]

    def source_path_attributes(self) -> Iterable[str]:
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

    def flake_dir(self):
        return self.spec.flake_file.parent

    def decorate_shellcmd(self, cmd: str) -> str:
        # Decorate given shell command such that it runs within the environment.

        # The `nix develop` command wants the directory of the flake file rather
        # than the flake file itself.  Passing the flake file prints a warning.
        return f"nix develop {self.flake_dir()} --command {cmd}"

    def record_hash(self, hash_object) -> None:
        # We just use the contents of the flake.lock file as our unique identifier.
        # It doesn't look like this method is being called in tests currently
        with open(self.flake_dir() / "flake.lock") as flake_lock:
            hash_object.update(flake_lock.read())

    def report_software(self) -> Iterable[SoftwareReport]:
        # An environment module is just a name, so we cannot report any software here?
        # TODO, maybe there is some way to get software from the module?
        return ()
