import os
import shlex
import subprocess


def _get_git_version(path):
    # Check if we are a git clone.
    if not os.path.isdir(os.path.join(path, ".git")):
        return None

    # Base the version off the "git describe --tags".
    command = shlex.split(f"git -C {path} describe --tags --long")
    try:
        describe = subprocess.check_output(command, universal_newlines=True).strip()
    except subprocess.CalledProcessError:
        # Most likely this was a clone without tags
        return None
    version, commit_since, git_hash = describe.rsplit("-", 3)

    # If we are not a release, we are a "post"; locally we can also be a
    # "dev", but as it is locally, it doesn't really matter. The hash will
    # change anyway, showing it is a different version.
    if commit_since != "0":
        return f"{version}.post{commit_since}+{git_hash}"

    return version


def get_version():
    path = os.path.dirname(os.path.realpath(__file__))
    version_file = os.path.join(path, "VERSION")

    # Load the version from disk if possible.
    if os.path.isfile(version_file):
        with open(version_file, "r") as f:
            disk_version = f.read()
    else:
        disk_version = None

    # Check if we have a git version.
    git_version = _get_git_version(path)

    # If we don't have a git version, return the disk version.
    if not git_version:
        return disk_version

    # IF the git version and disk version differ, write a new disk version.
    if git_version != disk_version:
        with open(version_file, "w") as f:
            f.write(git_version)

    return git_version
