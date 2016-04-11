---
layout: default
root: ../
title: 	Simulating structures proteus Geometry and floating structure tutorials
author: Tristan de Lataillade
level: intermediate
---

# Simulating structures: proteus.Geometry and floating structure tutorials

Tristan de Lataillade, [HR Wallingford](http://www.hrwallingford.com)

This tutorial will show how to set up two-phase flow test cases with floating
bodies using the moving mesh capabilities of
[Proteus](http://proteustoolkit.org). The full set up will be shown and two
main modules will be introduced: the proteus.mprans.SpatialTools module that is
used for building/importing, transforming and incorporating different
geometries into a larger domain, and the proteus.mpransBoundaryConditions
module that is used to enforce boundary conditions on segments/facets of the
geometries or on regions of the domain. Validation cases for free oscillation
(roll, pitch, and heave) of various floating caisson geometries in 2D and 3D
produced with Proteus will also be presented and compared with experimental
results and other numerical models.

<img src="/images/domain.png">