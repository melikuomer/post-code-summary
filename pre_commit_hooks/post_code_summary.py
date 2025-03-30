
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

    import subprocess
    diff_input = subprocess.run(('git', 'diff', '-U5'),
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            encoding='utf-8',
            check=True,
            input='\0'.join(args.filenames),
        ).stdout

    from pre_commit_hooks.ui import display_artifact
    from pre_commit_hooks.client import App
    client = App(api_key=os.getenv('GOOGLE_API_KEY') or "")
    artifact = client.run(diff_input)
    print(artifact.model_dump_json())
    display_artifact(artifact)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
