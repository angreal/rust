import angreal
import subprocess
import os

cwd = os.path.join(angreal.get_root(), '..')
test = angreal.command_group(name="test", about="commands for running tests")


def get_crates():
    """Discover crates in the workspace."""
    crates_dir = os.path.join(cwd, 'crates')
    if not os.path.isdir(crates_dir):
        return []
    return [d for d in os.listdir(crates_dir)
            if os.path.isfile(os.path.join(crates_dir, d, 'Cargo.toml'))]


@test()
@angreal.command(name="unit", about="run unit tests")
@angreal.argument(name="crate_name", required=False, help="specific crate to test (default: all)")
@angreal.argument(name="filter", long="filter", short="f", required=False, help="filter for specific tests")
def unit_tests(crate_name="", filter=""):
    cmd = ["cargo", "test", "--lib", "-v"]
    if crate_name:
        cmd.extend(["-p", crate_name])
    cmd.extend(["--", "--test-threads=1"])
    if filter:
        cmd.append(filter)
    result = subprocess.run(cmd, cwd=cwd)
    raise SystemExit(result.returncode)


@test()
@angreal.command(name="integration", about="run integration tests")
@angreal.argument(name="crate_name", required=False, help="specific crate to test (default: all)")
@angreal.argument(name="filter", long="filter", short="f", required=False, help="filter for specific tests")
def integration_tests(crate_name="", filter=""):
    cmd = ["cargo", "test", "--test", "integration"]
    if crate_name:
        cmd.extend(["-p", crate_name])
    cmd.extend(["--", "--test-threads=1", "--nocapture"])
    if filter:
        cmd.append(filter)
    result = subprocess.run(cmd, cwd=cwd)
    raise SystemExit(result.returncode)


@test()
@angreal.command(name="all", about="run all tests (unit and integration)")
@angreal.argument(name="crate_name", required=False, help="specific crate to test (default: all)")
def all_tests(crate_name=""):
    cmd = ["cargo", "test", "-v"]
    if crate_name:
        cmd.extend(["-p", crate_name])
    cmd.extend(["--", "--test-threads=1"])
    result = subprocess.run(cmd, cwd=cwd)
    raise SystemExit(result.returncode)


@test()
@angreal.command(name="coverage", about="generate code coverage report")
@angreal.argument(name="open", long="open", short="o", takes_value=False, help="open HTML report in browser")
def coverage(open=False):
    import webbrowser

    output_dir = os.path.join(cwd, "coverage")

    # Generate coverage
    cmds = [
        ["cargo", "llvm-cov", "--workspace", "--no-report", "--", "--test-threads=1"],
        ["cargo", "llvm-cov", "report", "--workspace", "--html", "--output-dir", output_dir],
        ["cargo", "llvm-cov", "report", "--workspace", "--lcov", "--output-path", os.path.join(output_dir, "lcov.info")],
        ["cargo", "llvm-cov", "report", "--workspace"],
    ]

    for cmd in cmds:
        result = subprocess.run(cmd, cwd=cwd)
        if result.returncode != 0:
            raise SystemExit(result.returncode)

    if open:
        report = os.path.join(output_dir, "html", "index.html")
        webbrowser.open(f"file://{os.path.realpath(report)}")
