"""
GEE AutoLab — Environment Check
Verifies GEE connection and dependencies.
"""
import importlib
import sys
import os

REQUIRED = [
    "ee", "geemap", "numpy", "pandas", "matplotlib"
]

OPTIONAL = [
    "geopandas", "seaborn", "rasterio"
]

def check_gee_connection():
    """Check if GEE is initialized."""
    try:
        import ee
        project = os.environ.get("EE_PROJECT")
        if project:
            ee.Initialize(project=project)
            print(f"✅ GEE initialized (project: {project})")
        else:
            try:
                ee.Initialize()
                print("✅ GEE initialized (default project)")
            except Exception:
                print("❌ GEE not initialized. Run: earthengine authenticate")
                print("   Or set: $env:EE_PROJECT = 'your-project-id'")
    except ImportError:
        print("❌ earthengine-api not installed. Run: pip install earthengine-api")


def check_dependencies():
    """Check required and optional packages."""
    print("\n📦 Dependencies:")
    for pkg in REQUIRED:
        try:
            importlib.import_module(pkg)
            print(f"  ✅ {pkg} installed")
        except ImportError:
            print(f"  ❌ {pkg} NOT installed")
    
    print("\n📦 Optional:")
    for pkg in OPTIONAL:
        try:
            importlib.import_module(pkg)
            print(f"  ✅ {pkg} installed")
        except ImportError:
            print(f"  ❌ {pkg} NOT installed (recommended for full functionality)")


if __name__ == "__main__":
    print("=" * 50)
    print("GEE AutoLab — Environment Check")
    print("=" * 50)
    check_dependencies()
    check_gee_connection()
    print("=" * 50)
