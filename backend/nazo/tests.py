from collections import defaultdict
from datetime import datetime
import json
import os
import time
from types import ModuleType

from nazo import Nazo
import nazo.configs as configs
from nazo.utils import get_audio_files

FAIL_RECORD_THREHOLD = 3  # i.e. when label is not in top 3, record FAIL

def benchmark(nz: Nazo, query_dirname, output_dirname="../results_qbh", remarks=None, verbose=False):
    s = time.time()
    now = datetime.now(tz=None).strftime("%d_%m_%Y_%H:%M")
    query_files = get_audio_files(query_dirname)
    num_query_files = len(query_files)
    score = 0
    hits = defaultdict(lambda: 0)
    fails = []
    exceptions = []
    for idx, (file_path, file_name, file_ext) in enumerate(query_files):
        try:
            label = file_name
            rank = nz.query(file_path)
            # Find the rank of label in predictions, None if not in top n
            label_index = next((idx for (idx, d) in enumerate(rank) if d[0] == label), None) if rank else None
            pred_label = rank[0][0]
            if verbose:
                print(f"({idx}/{num_query_files}) ({round(hits[0] / (idx + 1), 3)}) Result for {file_name} ({pred_label == label}): {pred_label}")
            if label_index is None or label_index > FAIL_RECORD_THREHOLD:
                fails.append({
                    "query": f"{file_name}{file_ext}",
                    "predict": pred_label,
                    "label": label,
                })
            else:
                hits[label_index] += 1
        except Exception as e:
            print(e)
            exceptions.append(e)
            pred_label = None
    for k, v in hits.items():
        score += v * (FAIL_RECORD_THREHOLD - k)  # i.e. 3 for first, 2 for sec, ...
    summary = {
        "accurracy": round(hits[0] / num_query_files, 8),
        "hits": dict(sorted(hits.items())),
        "score": score,
        "total": num_query_files,
        "duration": round(time.time() - s, 5),
        "configs": _configs_to_json(configs),
        "remarks": remarks,
    }
    with open(os.path.join(output_dirname, f"summary-{now}.json"), 'w') as f:
        json.dump(summary, f, indent=2)
    with open(os.path.join(output_dirname, f"fails-{now}.json"), 'w') as f:
        json.dump(fails, f, indent=4, sort_keys=True)
    return summary

def _configs_to_json(configs_module: ModuleType) -> dict:
    configs = {}
    for k in dir(configs_module):
        if not k.startswith('__'):
            v = getattr(configs_module, k)
            configs[k] = list(v) if isinstance(v, set) else v
    return configs
