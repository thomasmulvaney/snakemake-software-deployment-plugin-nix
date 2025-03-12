# Snakemake Software Deployment Plugin Nix

## Example Snakemake file

In the following example, two rules have their own `flake.nix` files.
These environments have been organised using the `nix/<tool>/flake.nix`
structure.

```snakemake

rule frobnicate:
   input="data.txt"
   output"frobnicated_data.txt"
   nix:
     flakefile="nix/frobnicate/flake.nix"
   shell="frobicate {input} {output}"
   
rule tweaker:
   input="data.txt"
   output"tweaked_data.txt"
   nix:
     flakefile="nix/tweaker/flake.nix"
   shell: 
      "tweaker {input} {output}"

```