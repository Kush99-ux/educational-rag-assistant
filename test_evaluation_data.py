import json

with open(
    "data/evaluation/evaluation_set.json",
    "r"
) as f:

    samples = json.load(f)

print(
    f"Loaded {len(samples)} samples"
)

print(
    samples[0]
)