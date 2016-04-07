---
layout: default
root: ../
title: Numerical modeling of wet particulate media in various limits
author: Ken Kamrin
level: intermediate
---

# Numerical modeling of wet particulate media in various limits

Ken Kamrin, MIT

Modeling of wet granular media adds a number of challenges on top of those
already present in the dry case.  For dry grains, continuum models are now at a
relatively high level of predictive accuracy, with recent advances in granular
rheology and corresponding improvements in computational methodology.  Soil
mechanics models can be used for wet granular systems, but the same level of
precision is not yet attainable.  A key tool in the development of wet grain
modeling at the large (i.e. continuum) scale is the development of accurate
micro-scale simulation tools, which properly simulate the grain-grain and
grain-fluid interactions.  Such small-scale simulations can be homogenized
spatially to provide key continuum-scale data, which can be used for model
validation.  We will discuss several particle-level techniques currently being
customized within our group to model the various regimes of wet granular media.

For partially-saturated granular media, in the so-called "pendular state" where
fluid forms capillary bridges, we have constructed a fluid-augmented discrete
element code, which tracks each grain and dynamically tracks the fluid in the
system.  The fluid can pass between occupying a capillary bridge or the thin
coating surrounding a grain.  Homogenizing reveals a novel constitutive
behavior for partially-wet granular systems as a function of liquid-fraction,
surface tension, and grain properties.  As liquid fraction increases, the media
enters a fully-saturated, or "slurry state".  Here, we have customized a
Lattice-Boltzmann/Discrete-Element simulation method that can solve
simultaneously for fluid dynamics between the grains, grain-grain contact
interactions, as well as interactions of the fluid and grains with soft
deformable structures.  This has proven useful in application for calculating
the dynamics of slurries and rubber valves, for example.  As particle
properties become more obscure and we leave the hard-particle limit, we have
also developed a method for arbitrarily shaped particles of arbitrary
constitutive behavior saturated within a fluid phase.  This technique utilizes
a novel fluid-structure interaction technique based entirely in Eulerian frame.
