
import os
def main():

    import subprocess
    diff_input = subprocess.run(['git', 'diff', '-U5'], capture_output=True, text=True).stdout

    from pre_commit_hooks.ui import display_artifact
    from pre_commit_hooks.client import App
    client = App(api_key=os.getenv('GOOGLE_API_KEY') or "")
    artifact = client.run(diff_input)
    display_artifact(artifact)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
