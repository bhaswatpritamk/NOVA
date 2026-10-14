#!/usr/bin/env python3
"""Nova-Fit Environment Diagnostics Report.

Collects and displays system hardware, runtime environment, disk storage,
and deep learning framework capabilities (PyTorch & CUDA).
"""

from __future__ import annotations

import json
import os
import platform
import shutil
import sys
from typing import Any, Dict


def get_available_ram_bytes() -> tuple[int | None, int | None]:
    """Retrieve total and available RAM in bytes with graceful fallbacks.

    Returns:
        tuple of (total_ram_bytes, available_ram_bytes). Elements may be None
        if measurable memory cannot be determined.
    """
    try:
        import psutil  # type: ignore

        mem = psutil.virtual_memory()
        return mem.total, mem.available
    except Exception:
        pass

    # Windows fallback using ctypes
    if platform.system() == "Windows":
        try:
            import ctypes
            from ctypes import wintypes

            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", wintypes.DWORD),
                    ("dwMemoryLoad", wintypes.DWORD),
                    ("ullTotalPhys", ctypes.c_uint64),
                    ("ullAvailPhys", ctypes.c_uint64),
                    ("ullTotalPageFile", ctypes.c_uint64),
                    ("ullAvailPageFile", ctypes.c_uint64),
                    ("ullTotalVirtual", ctypes.c_uint64),
                    ("ullAvailVirtual", ctypes.c_uint64),
                    ("ullAvailExtendedVirtual", ctypes.c_uint64),
                ]

            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
                return stat.ullTotalPhys, stat.ullAvailPhys
        except Exception:
            pass

    return None, None


def format_bytes(num_bytes: int | None) -> str:
    """Format bytes into a human-readable string (GiB/MiB)."""
    if num_bytes is None:
        return "Not measurable"
    gib = num_bytes / (1024**3)
    if gib >= 1.0:
        return f"{gib:.2f} GiB ({num_bytes:,} bytes)"
    mib = num_bytes / (1024**2)
    return f"{mib:.2f} MiB ({num_bytes:,} bytes)"


def collect_environment_report() -> Dict[str, Any]:
    """Collect runtime environment metadata and hardware specifications."""
    report: Dict[str, Any] = {}

    # Python runtime
    report["python_version"] = platform.python_version()
    report["python_full_version"] = sys.version.replace("\n", " ")
    report["executable_path"] = sys.executable

    # Operating system
    report["os_system"] = platform.system()
    report["os_release"] = platform.release()
    report["os_version"] = platform.version()
    report["os_architecture"] = platform.machine()
    report["os_platform"] = platform.platform()

    # CPU specifications
    cpu_logical = os.cpu_count()
    cpu_physical = None
    try:
        import psutil  # type: ignore

        cpu_physical = psutil.cpu_count(logical=False)
    except Exception:
        pass

    report["cpu_count_logical"] = cpu_logical
    report["cpu_count_physical"] = cpu_physical

    # RAM specifications
    total_ram, avail_ram = get_available_ram_bytes()
    report["ram_total_bytes"] = total_ram
    report["ram_available_bytes"] = avail_ram
    report["ram_total_human"] = format_bytes(total_ram)
    report["ram_available_human"] = format_bytes(avail_ram)

    # Disk specifications for current workspace
    try:
        usage = shutil.disk_usage(os.getcwd())
        report["disk_total_bytes"] = usage.total
        report["disk_used_bytes"] = usage.used
        report["disk_free_bytes"] = usage.free
        report["disk_total_human"] = format_bytes(usage.total)
        report["disk_free_human"] = format_bytes(usage.free)
    except Exception as e:
        report["disk_error"] = str(e)
        report["disk_total_human"] = "Not measurable"
        report["disk_free_human"] = "Not measurable"

    # PyTorch and acceleration framework
    try:
        import torch  # type: ignore

        report["pytorch_installed"] = True
        report["pytorch_version"] = torch.__version__
        report["cuda_available"] = bool(torch.cuda.is_available())
        if report["cuda_available"]:
            report["cuda_device_count"] = torch.cuda.device_count()
            report["cuda_device_names"] = [
                torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())
            ]
            report["cuda_runtime_version"] = torch.version.cuda
        else:
            report["cuda_device_count"] = 0
            report["cuda_device_names"] = []
            report["cuda_runtime_version"] = getattr(torch.version, "cuda", None)

        # Check MPS (macOS) if relevant
        report["mps_available"] = bool(
            hasattr(torch.backends, "mps") and torch.backends.mps.is_available()
        )
    except ImportError:
        report["pytorch_installed"] = False
        report["pytorch_version"] = "Not installed"
        report["cuda_available"] = False
        report["cuda_device_count"] = 0
        report["cuda_device_names"] = []
        report["cuda_runtime_version"] = None
        report["mps_available"] = False

    return report


def print_environment_report(report: Dict[str, Any] | None = None) -> None:
    """Print a clean, structured environment report to stdout."""
    if report is None:
        report = collect_environment_report()

    header = "=" * 64
    print(header)
    print(" PROJECT NOVA-FIT : ENVIRONMENT & HARDWARE DIAGNOSTICS")
    print(header)

    print("\n[Python Runtime]")
    print(f"  Version         : {report.get('python_version')}")
    print(f"  Executable Path : {report.get('executable_path')}")

    print("\n[Operating System]")
    print(f"  OS System       : {report.get('os_system')} ({report.get('os_architecture')})")
    print(f"  OS Release      : {report.get('os_release')}")
    print(f"  OS Platform     : {report.get('os_platform')}")

    print("\n[CPU & Compute]")
    phys = report.get("cpu_count_physical")
    phys_str = f" ({phys} physical)" if phys else ""
    print(f"  CPU Cores       : {report.get('cpu_count_logical')} logical{phys_str}")

    print("\n[Memory (RAM)]")
    print(f"  Total RAM       : {report.get('ram_total_human')}")
    print(f"  Available RAM   : {report.get('ram_available_human')}")

    print("\n[Disk Storage (Workspace)]")
    print(f"  Total Space     : {report.get('disk_total_human')}")
    print(f"  Free Space      : {report.get('disk_free_human')}")

    print("\n[PyTorch & Hardware Acceleration]")
    print(f"  PyTorch Version : {report.get('pytorch_version')}")
    cuda_status = "Available" if report.get("cuda_available") else "Not Available (CPU mode)"
    print(f"  CUDA Status     : {cuda_status}")
    if report.get("cuda_available"):
        print(f"  CUDA Devices    : {report.get('cuda_device_count')}")
        for i, name in enumerate(report.get("cuda_device_names", [])):
            print(f"    - Device {i}   : {name}")
        print(f"  CUDA Version    : {report.get('cuda_runtime_version')}")
    else:
        print("  CUDA Notes      : Expected for local workstation (CPU development).")

    print(header)


def main() -> None:
    if "--json" in sys.argv:
        report = collect_environment_report()
        print(json.dumps(report, indent=2))
    else:
        print_environment_report()


if __name__ == "__main__":
    main()
