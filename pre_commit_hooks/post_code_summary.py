
import os
from typing import Sequence
import argparse

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filenames', nargs='*',
        help='Filenames pre-commit believes are changed.',
    )
    args = parser.parse_args(argv)
    print(args.filenames)
    try:
        from git import Repo
        repo = Repo('.')
        head_commit = repo.head.commit
        diff_input = repo.git.diff(head_commit.parents[0], head_commit, unified=5)
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        raise
    print("test",diff_input)
    from pre_commit_hooks.ui import display_artifact
    from pre_commit_hooks.client import App
    client = App(api_key=os.getenv('GOOGLE_API_KEY') or "")
    artifact = client.run(diff_input)
    print(artifact.model_dump_json())
    display_artifact(artifact)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
