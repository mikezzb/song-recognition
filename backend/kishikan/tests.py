from datetime import datetime
import json
import os
from kishikan import Kishikan
from kishikan.utils import get_audio_files

# E.g. blues.00000-snippet-10-10 -> (blues.00000, duration, offset)
def GTZAN_query_label_split(fname: str) -> str:
    fname, _, duration, offset = fname.split('-')
    return (fname, duration, offset)

def benchmark(ksk: Kishikan, query_dirname, output_dirname="../../results", remarks=None, verbose=False):
    now = datetime.now(tz=None).strftime("%d_%b_%Y_%H_%M)")
    query_files = get_audio_files(query_dirname)
    num_query_files = len(query_files)
    num_hits = 0
    fails = []
    for file_path, file_name, file_ext in query_files:
        label, duration, offset = GTZAN_query_label_split(file_name)
        rank = ksk.match(file_path)
        pred_label = rank[0]["name"]
        if verbose:
            print(f"Result for {file_name} ({pred_label == label}): {pred_label}")
        if pred_label == label:
            num_hits += 1
        else:
            fails.append({
                "query": f"{file_name}{file_ext}",
                "rank": rank,
                "label": label,
                "duration": duration,
                "offset": offset,
            })
    summary = {
        "accurracy": num_hits / num_query_files,
        "hits": num_hits,
        "total": num_query_files,
        "date": now,
        "remarks": remarks,
    }
    with open(os.path.join(output_dirname, f"summary-{now}"), 'w') as f:
        json.dump(summary, f)
    with open(os.path.join(output_dirname, f"fails-{now}"), 'w') as f:
        json.dump(fails, f)
    return summary
