---
layout: default
root: ../
title: Adaptive Unstructured Approaches for Problems with Fluid-Structure and Multiphase Interactions at Extreme Scale
author: Onkar Sahni
level: intermediate
---

# Adaptive unstructured approaches for problems with fluid-structure and multiphase interactions at extreme scale

Onkar Sahni and Mark Shephard, RPI

Reliable simulation of fluid flow problems with fluid-structure and
multiphase interactions are challenging because of the inherent
difficulty in keeping track of the evolving interfaces. The two basic
options for tracking evolving interfaces are to either explicitly or
implicitly represent them. Both options offer specific advantages and
disadvantages and method of choice depends on the specific problem of
interest. In this talk we will cover adaptive unstructured approaches
that address the needs of both explicit and implicit methods for
tracking interfaces. We will focus on local mesh modifications that
support a wide range of needs including evolving interfaces,
discontinuous fields at the interface, moving and deforming geometries
involving mesh motion, and high anisotropy together with layered
elements. We will also cover parallelization aspects related to
partitioning and mesh modifications to be effective at both the intra-
and inter-nodal levels on current and upcoming supercomputers.
