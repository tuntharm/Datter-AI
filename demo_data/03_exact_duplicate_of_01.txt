# Neural Operator Surrogate for Beam Dynamics

We propose a Fourier neural operator (FNO) surrogate for transient Euler-Bernoulli beam response under moving loads. The model maps boundary conditions and forcing histories to displacement fields with 40x speedup over explicit Newmark integration at comparable L2 error (< 2% on held-out load speeds).

Key contributions:
- Physics-informed loss combining PDE residual and data fidelity
- Extrapolation to unseen load velocities without retraining
- Deployment on edge hardware for structural health monitoring

Experimental setup: 12m simply supported steel I-beam, 500 training trajectories, 100 validation trajectories spanning load speeds 5–25 m/s.
