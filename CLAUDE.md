# CLAUDE.md

## Hive Ecosystem Fork Boundary

This checkout is `Dhenz14/parallax`, a Hive operator fork of GradientHQ
Parallax. Treat upstream GradientHQ docs, badges, Docker images, and public
installer links as upstream product provenance unless a Hive-specific note says
otherwise.

In the Hive ecosystem, this repo is a dependency/product-adjacent inference
engine used by Hive-AI, HivePoA, NeuraChain, and IDE workers for distributed
pipeline-parallel serving experiments. It is not itself the canonical Hive IDE
or Hive capability registry source of truth. Hive feature and capability claims
belong in the consuming Hive repos; Parallax changes should stay focused on
serving behavior, operator compatibility, fork provenance, and integration
receipts.

When changing install or deployment docs, preserve upstream instructions for
ordinary Parallax users and add Hive-operator notes separately.
