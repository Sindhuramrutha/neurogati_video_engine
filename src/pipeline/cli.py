"""Command-line entry point.

The CLI and the web app are two clients of the same core — neither owns pipeline
logic. v1 split this badly: `workflow.py` built a LangGraph pipeline that
`run_chapter.py` then bypassed with a reimplementation, so the two drifted and only
one was ever exercised. Not repeated here.
"""

from __future__ import annotations

import argparse


def _serve(args: argparse.Namespace) -> int:
    import uvicorn

    # ASCII only: the Windows console defaults to cp1252, which cannot encode
    # arrows/box-drawing and raises UnicodeEncodeError before the server starts.
    print(f"serving on http://{args.host}:{args.port}")
    uvicorn.run(
        "pipeline.web.app:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="warning",
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="pipeline", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_serve = sub.add_parser("serve", help="run the web app")
    p_serve.add_argument("--host", default="127.0.0.1")
    p_serve.add_argument("--port", type=int, default=8000)
    p_serve.add_argument("--reload", action="store_true")
    p_serve.set_defaults(fn=_serve)

    args = parser.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
