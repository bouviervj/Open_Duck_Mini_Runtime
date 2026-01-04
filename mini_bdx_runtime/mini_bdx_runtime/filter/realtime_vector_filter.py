import numpy as np
import collections

class RealTimeVectorFilter:
    def __init__(self, window_size=7, threshold_sigma=3.0):
        self.window_size = window_size
        self.threshold_sigma = threshold_sigma
        # Store 3D vectors as (N, 3) arrays in a deque
        self.buffer = collections.deque(maxlen=window_size)

    def filter(self, new_vector):
        """
        Expects new_vector as a np.array([x, y, z])
        """
        self.buffer.append(new_vector)

        if len(self.buffer) < self.window_size:
            return new_vector

        # Convert buffer to a numpy array for vectorized operations
        data_window = np.array(self.buffer) # Shape: (window_size, 3)

        # 1. Calculate L2 Norm (Magnitude) for each vector in the window
        norms = np.linalg.norm(data_window, axis=1) # Shape: (window_size,)

        # 2. Calculate Robust Statistics on the norms
        median_norm = np.median(norms)
        # Median Absolute Deviation (MAD) scaled by 1.4826 for normal distribution consistency
        mad = np.median(np.abs(norms - median_norm)) * 1.4826

        # 3. Detect Outlier based on the current (last added) vector
        current_norm = norms[-1]

        # Prevent division by zero if all values in window are identical
        if mad == 0:
            return new_vector

        # 4. Spike Rejection logic
        # If current magnitude is > threshold sigma from the median magnitude
        if np.abs(current_norm - median_norm) > self.threshold_sigma * mad:
            # Find the vector in the window that represents the 'median vector'
            # Note: We replace with the vector whose norm is closest to the median_norm
            median_idx = np.argmin(np.abs(norms - median_norm))
            return data_window[median_idx]

        return new_vector
