import math
import numpy as np

def color_similarity(c1, c2):
    c1 = np.array(c1, dtype=np.float32)
    c2 = np.array(c2, dtype=np.float32)
    dist = np.linalg.norm(c1 - c2)
    max_dist = math.sqrt(255**2 * 3)
    sim = 1.0 - (dist / max_dist)
    return max(0.0, min(1.0, sim))