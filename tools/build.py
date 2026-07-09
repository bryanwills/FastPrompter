import os
import shutil
import subprocess
import sys


def build_with_nuitka():
    # Ensure we are in the project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    os.chdir(project_root)

    print("Starting Nuitka build for FastPrompter...")

    # Check for UPX (saves ~50-60% on binary size)
    upx_bin = shutil.which("upx")

    cmd = [
        sys.executable,
        "-m",
        "nuitka",
        "--onefile",
        "--enable-plugin=pyqt6",
        "--windows-disable-console",
        "--output-dir=build",
        "--assume-yes-for-downloads",
        # Size optimization flags
        "--no-docstrings",  # Remove docstrings from compiled modules
        "--no-asserts",  # Remove assert statements
        # Prune unused Qt plugins (PyQt6 bundles ~150MB of unused WebEngine/QML/etc.)
        "--include-qt-plugins=platforms,styles,imageformats",
        # QtMultimedia pulls in ~100MB of FFmpeg DLLs just for WAV clicks;
        # SoundManager falls back to stdlib winsound when it's missing.
        "--nofollow-import-to=PyQt6.QtMultimedia",
        # WARNING: if app crashes at runtime, remove this flag first
        "--noinclude-custom-import-hooks",  # Don't bundle unused import hooks
        # Use the correct entry point (FastPrompter.pyw sets up paths)
        "FastPrompter.pyw",
    ]

    if upx_bin:
        cmd.append("--plugin-enable=upx")
        cmd.append(f"--upx-binary={upx_bin}")
        print("UPX compression enabled for smaller executable size.")
    else:
        print("UPX not found. Install UPX (https://upx.github.io/) for 50-60% size reduction.")
        print("Then add upx to PATH and re-run.")

    print("Running command:", " ".join(cmd))

    try:
        subprocess.run(cmd, check=True)
        print("\n[SUCCESS] Build complete! Executable is located in the 'build' directory.")
        # Show build output size
        build_dir = os.path.join(project_root, "build")
        if os.path.exists(build_dir):
            for f in os.listdir(build_dir):
                fpath = os.path.join(build_dir, f)
                if os.path.isfile(fpath):
                    size_mb = os.path.getsize(fpath) / (1024 * 1024)
                    print(f"  {f}: {size_mb:.1f} MB")
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Build failed with exit code {e.returncode}")
        sys.exit(e.returncode)


if __name__ == "__main__":
    build_with_nuitka()
