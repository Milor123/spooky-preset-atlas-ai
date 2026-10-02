"""Publish a locally built index to a Hugging Face dataset repo.

Use this if you want to share a database you built from your own copy of
Spooky2. You need your own Hugging Face account and a dataset repo created
once:

    hf repo create <user>/<dataset-name> --repo-type dataset

Then point this at your own paths and run it.

Before you do: the index contains your vendor's and the preset authors' content
— preset names, their descriptions, their frequency lines. That content is not
covered by this project's MIT license, and publishing it redistributes their
work. Publishing your own build is your decision to make with your own copy,
but the underlying material is not yours to license. Building locally and
sharing only the tooling is the safer default.
"""

from __future__ import annotations

import os
import sys

from huggingface_hub import HfApi

LOCAL_PATH = "preset-db/build/spooky.db"
PATH_IN_REPO = "preset-db/build/spooky.db"
REPO_ID = "Milor123/spooky-preset-atlas-db"  # change to your own repo
REPO_TYPE = "dataset"


def main() -> int:
    # Force the legacy HTTP path instead of Xet by uncommenting, before the
    # HfApi import happens in a normal run:
    # os.environ["HF_HUB_DISABLE_XET"] = "1"

    if not os.path.isfile(LOCAL_PATH):
        print(f"  {LOCAL_PATH} not found. Build it first:")
        print("    python preset-db/tools/build_db.py --full")
        return 1

    size = os.path.getsize(LOCAL_PATH)
    print(f"  uploading {LOCAL_PATH} ({size:,} bytes) to {REPO_ID}")
    print("  this is ~1 GB and takes a while. Ctrl+C is safe to retry.")

    api = HfApi()
    api.upload_file(
        path_or_fileobj=LOCAL_PATH,
        path_in_repo=PATH_IN_REPO,
        repo_id=REPO_ID,
        repo_type=REPO_TYPE,
    )
    print(f"  done: https://huggingface.co/datasets/{REPO_ID}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
