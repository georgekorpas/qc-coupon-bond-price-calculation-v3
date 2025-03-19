# **Monte Carlo Coupon Bond Pricing Calculator v2 **

## Overview
This solver estimates bond prices using a **Monte Carlo simulation** for short-rate dynamics under a simplified [Heath-Jarrow-Morton (HJM) model](https://en.wikipedia.org/wiki/Heath%E2%80%93Jarrow%E2%80%93Morton_framework). It incorporates algorithmic improvements over v2 to enhance efficiency and accuracy while maintaining the same input-output structure.  
 
### Algorithmic Improvements  ###

**1. Antithetic Sampling for Variance Reduction**  
- Instead of generating `num_simulations` independent random paths, we generate **half** that amount.  
- For each Brownian motion path, we also simulate its **negated counterpart** \( -W_t \), ensuring a more balanced sample distribution.  
- This technique **reduces variance**, leading to **faster convergence** with fewer simulations.  

**2. NumPy Vectorization for Speed Optimization**  
- Eliminates slow **for-loops** by leveraging **NumPy matrix operations**.  
- Updates all short-rate paths in a **single step**, significantly improving execution speed.  
- Uses **cumulative summation (`np.cumsum()`)** for **faster integration** in discount factor computation.  

## Benefits of the optimized solver over v2
✅ Faster execution times → Vectorized computations reduce runtime.  
✅ Improved accuracy → Antithetic sampling lowers variance.  
✅ Better scalability → Efficient memory usage allows larger simulations.  

