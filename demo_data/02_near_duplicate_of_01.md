# FNO Surrogate Model for Beam Transient Response

This work develops a Fourier Neural Operator surrogate for predicting transient displacement in Euler-Bernoulli beams subject to moving loads. Compared to explicit Newmark time integration, our approach achieves roughly 40 times faster inference with L2 error below 2% on held-out velocity conditions.

Main results:
- Combined physics-informed and data-driven training objective
- Generalizes to load speeds not seen during training
- Suitable for real-time structural health monitoring on edge devices

We evaluate on a 12 metre simply supported steel I-beam using 500 training and 100 validation load trajectories with speeds from 5 to 25 metres per second.
