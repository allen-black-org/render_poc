# analytics/retention_model.py
import numpy as np

def compute_retention_slopes(retention_json):
    results = []
    for name, values in retention_json.items():
        try:
            x = np.array([60, 90, 120])
            y = np.array([values[str(k)] for k in x])
        except KeyError:
            print(f"Skipping {name}: keys = {list(values.keys())}")


        slope, intercept = np.polyfit(x, y, 1)
        results.append({"wholesaler": name, "slope": slope, "r120": y[-1]})

    slopes = np.array([r["slope"] for r in results])
    q1, q3 = np.percentile(slopes, [25, 75])
    iqr = q3 - q1
    outlier_threshold = q1 - 1.5 * iqr

    for r in results:
        r["is_outlier"] = bool(r["slope"] < outlier_threshold)

    return results