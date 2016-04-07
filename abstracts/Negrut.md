---
layout: default
root: ../
title: Chrono An Open-Source Physics Engine
author: Dan Negrut
level: intermediate
---

# Chrono: An Open-Source Physics Engine

Dan Negrut, University of Wisconsin

This talk provides an overview of the modeling and numerical solution
foundation of Chrono, an open source physics engine. To this end, we summarize
(a) Chrono’s rigid and flexible body dynamics formulation and the associated
numerical solution infrastructure, (b) the fledgling support for the fluid
dynamics component, and (c) strategies for coupling of the solid and fluid
phases. On the solid dynamics side, we rely on the Newton-Euler equations of
motion to capture the time evolution of systems with millions of rigid and/or
flexible bodies that interact mutually through impact/contact/friction. On the
fluid side, Chrono solves the Navier-Stokes equations using a smoothed particle
hydrodynamics (SPH) methodology. The presentation will outline the structure of
Chrono, its reliance on parallel computing, and its use in a broad spectrum of
problems – from additive manufacturing to ground vehicle fording
scenarios. Chrono is an open source software infrastructure released under a
permissive BSD3 license
