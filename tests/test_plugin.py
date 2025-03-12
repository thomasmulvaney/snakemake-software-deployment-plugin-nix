import os
from pathlib import Path
from typing import Optional, Type
from snakemake_interface_software_deployment_plugins import EnvBase
from snakemake_interface_software_deployment_plugins.tests import (
    TestSoftwareDeploymentBase,
)

from snakemake_interface_software_deployment_plugins.settings import (
    SoftwareDeploymentSettingsBase,
)

from snakemake_software_deployment_plugin_nix import Env, EnvSpec, EnvSpecBase

class TestSoftwareDeployment(TestSoftwareDeploymentBase):
    __test__ = True  # activate automatic testing

    def get_env_spec(self) -> EnvSpecBase:
        # Our nix flake is defined in `./test/nix`.
        return EnvSpec(
            flake_dir=Path(__file__).parent / "nix"
        )

    def get_software_deployment_provider_settings(
        self,
    ) -> Optional[SoftwareDeploymentSettingsBase]:
        return None

    def get_env_cls(self) -> Type[EnvBase]:
        return Env

    def get_test_cmd(self) -> str:
        # Return a command that should be executable without error in the environment
        return "hello"
