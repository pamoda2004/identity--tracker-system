class FeatureExtractor:
    def _mean_color(self, img):
        if img is None or img.size == 0:
            return [0.0, 0.0, 0.0]
        return img.mean(axis=(0, 1)).tolist()

    def extract(self, crop, bbox):
        if crop is None or crop.size == 0:
            return {
                "upper_color": [0.0, 0.0, 0.0],
                "lower_color": [0.0, 0.0, 0.0],
                "aspect_ratio": 0.0,
                "height": 0.0,
            }

        h, w = crop.shape[:2]
        upper = crop[: h // 2, :]
        lower = crop[h // 2 :, :]
        aspect_ratio = float(w / h) if h > 0 else 0.0

        return {
            "upper_color": self._mean_color(upper),
            "lower_color": self._mean_color(lower),
            "aspect_ratio": aspect_ratio,
            "height": float(h),
        }