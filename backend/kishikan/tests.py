from collections import defaultdict
from datetime import datetime
import json
import os
from concurrent import futures
from kishikan import Kishikan
from kishikan.utils import get_audio_files

FAIL_RECORD_THREHOLD = 3  # i.e. when label is not in top 3, record FAIL

# E.g. blues.00000-snippet-10-10 -> (blues.00000, duration, offset)
def GTZAN_query_label_split(fname: str) -> str:
    fname, _, duration, offset = fname.split('-')
    return (fname, duration, offset)

def benchmark(ksk: Kishikan, query_dirname, output_dirname="../results", remarks=None, verbose=False):
    now = datetime.now(tz=None).strftime("%d_%m_%Y_%H:%M)")
    query_files = get_audio_files(query_dirname)
    num_query_files = len(query_files)
    score = 0
    hits = defaultdict(lambda: 0)
    fails = []
    for file_path, file_name, file_ext in query_files:
        label, duration, offset = GTZAN_query_label_split(file_name)
        rank = ksk.match(file_path)
        # Find the rank of label in predictions, None if not in top n
        label_index = next((idx for (idx, d) in enumerate(rank) if d["name"] == label), None)
        try:
            pred_label = rank[0]["name"]
        except IndexError:
            pred_label = None
        if verbose:
            print(f"Result for {file_name} ({pred_label == label}): {pred_label}")
        if label_index is None or label_index > FAIL_RECORD_THREHOLD:
            fails.append({
                "query": f"{file_name}{file_ext}",
                "predict": pred_label,
                "label": label,
                "duration": duration,
                "offset": offset,
            })
        else:
            hits[label_index] += 1
    for k, v in hits.items():
        score += v * (FAIL_RECORD_THREHOLD - k)  # i.e. 3 for first, 2 for sec, ...
    summary = {
        "accurracy": round(hits[0] / num_query_files, 8),
        "hits": dict(sorted(hits.items())),
        "score": score,
        "total": num_query_files,
        "date": now,
        "remarks": remarks,
    }
    with open(os.path.join(output_dirname, f"summary-{now}.json"), 'w') as f:
        json.dump(summary, f)
    with open(os.path.join(output_dirname, f"fails-{now}.json"), 'w') as f:
        json.dump(fails, f)
    return summary
