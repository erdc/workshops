---
layout: default
root: ../
title: Using the HashDist tool to manage HPC software distributions
author: Chris Kees
level: intermediate
---

# Using the [HashDist](http://hashdist.github.io) tool to manage HPC software distributions

Chris Kees, CHL

Real world computational simulation requires the integration of many
capabilities, from mesh generation to algebraic solvers to
visualization. Reliably providing an integrated capability presents software
developers with a dilemma: 1) roll all the capabilities into a single code base
or 2) rely on outside packages for specific capabilities. Both approaches
result in a kind of "dependency hell" in which reproducing, maintaining, or
extending capabilities begins to require increasingly unacceptable amounts of
developer time. The [Proteus](http://proteustoolkit.org) team deliberately
chose to depend on other community tools (approach #2) to provide or enhance
certain capabilities, but the resulting dependency hell quickly became
apparent, particularly on HPC systems with a mixture of vendor library and
source code dependencies. To address this problem, we joined with other
scientific software developers to develop
[HashDist](http://hashdist.github.io), which is a tool for reproducing complex
software stacks across platforms. This short tutorial will show how to modify
and build the software stack for [Proteus](http://proteustoolkit.org).
