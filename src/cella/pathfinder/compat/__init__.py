"""Legacy prototype behavior behind the typed package facade.

The frozen implementation lives at cella._legacy_pathfinder (its relative
imports require the package root).  This module is the compatibility
boundary: characterization and MCP gates close through these three symbols.
"""

from ..._legacy_pathfinder import pathfinder_compare, rewrite_candidates, route_plan

__all__ = ["pathfinder_compare", "rewrite_candidates", "route_plan"]
