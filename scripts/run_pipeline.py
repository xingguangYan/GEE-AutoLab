#!/usr/bin/env python3
"""
GEE AutoLab 閳?Pipeline Orchestrator
Unified entry point: parse 閳?resolve ROI 閳?select data 閳?preprocess 閳?analyze 閳?export 閳?report
"""
import os, sys, json, argparse
from datetime import datetime

from task_parser import parse_task, print_parsed
from generate_gee import save_script, generate_gee_script_v2
from generate_report import generate_report


def run_pipeline(user_input: str, project_id: str = None, output_dir: str = "outputs", verbose: bool = True):
    """Execute the full 7-step GEE AutoLab pipeline."""

    print("=" * 60)
    print("  GEE AutoLab 閳?Pipeline Execution")
    print("=" * 60)

    # Step 1: Parse input
    print("\n[Step 1/7] Parsing input...")
    params = parse_task(user_input)
    if verbose:
        print_parsed(params)

    # Step 2: Resolve ROI (annotation only 閳?actual ROI is set in generated script)
    print(f"\n[Step 2/7] ROI: {params.get('location', 'to be determined')}")

    # Step 3: Select data source
    datasets = params.get("datasets", [])
    print(f"\n[Step 3/7] Data sources: {', '.join(datasets)}")

    # Step 4: Preprocess (handled in generated GEE script)
    print(f"\n[Step 4/7] Preprocessing: cloud mask ({params['params']['cloud_threshold']}%), clip, composite")

    # Step 5: Generate & display analysis plan
    tasks = params.get("tasks", [])
    print(f"\n[Step 5/7] Analysis plan: {', '.join(tasks)}")

    # Step 6: Generate GEE script + export instructions
    print(f"\n[Step 6/7] Generating GEE script...")
    script = generate_gee_script_v2(params, project_id=project_id)
    script_path = save_script(script, output_dir=output_dir)
    print(f"  Script saved: {script_path}")

    # Step 7: Generate report
    print(f"\n[Step 7/7] Generating experiment report...")
    report_path = generate_report(params, {}, output_dir=output_dir)
    print(f"  Report saved: {report_path}")

    print("\n" + "=" * 60)
    print("  Pipeline complete!")
    print(f"  Script : {script_path}")
    print(f"  Report : {report_path}")
    print("=" * 60)

    return {
        "params": params,
        "script_path": script_path,
        "report_path": report_path,
        "timestamp": datetime.now().isoformat()
    }


def main():
    parser = argparse.ArgumentParser(description="GEE AutoLab 閳?Automated Remote Sensing Pipeline")
    parser.add_argument("query", nargs="*", help="Natural language query (time + location + task)")
    parser.add_argument("--project", "-p", help="GEE Cloud Project ID")
    parser.add_argument("--output", "-o", default="outputs", help="Output directory")
    parser.add_argument("--quiet", "-q", action="store_true", help="Minimal output")
    args = parser.parse_args()

    query = " ".join(args.query) if args.query else None
    if not query:
        print("GEE AutoLab Interactive Mode")
        print("Enter your query (or 'quit' to exit):")
        while True:
            query = input("> ").strip()
            if query.lower() in ("quit", "exit", "q"):
                break
            if query:
                project = args.project or os.environ.get("EE_PROJECT")
                run_pipeline(query, project_id=project, output_dir=args.output, verbose=not args.quiet)
                print()
    else:
        project = args.project or os.environ.get("EE_PROJECT")
        result = run_pipeline(query, project_id=project, output_dir=args.output, verbose=not args.quiet)
        print(json.dumps({"status": "ok", "outputs": result}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
