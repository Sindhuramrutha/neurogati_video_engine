"""Command-line entry point.

The CLI, the web app and the MCP server are three clients of the same core --
none of them owns pipeline logic. Every command below is a thin call into
`pipeline.operations`, so a rule enforced there holds for all three.

**Designed for an agent with a shell, not only for a person.** Everything prints
JSON to stdout by default, reads JSON from stdin where it needs a document, and
exits non-zero with a message on stderr when something is wrong. So a model that
can run commands can drive the whole pipeline without an HTTP client:

    pipeline projects create "Gradient Descent"
    pipeline plan add-section gradient-descent --title "What a gradient is" --seconds 90
    pipeline show gradient-descent plan | jq .warnings
    pipeline show gradient-descent plan > plan.json   # edit it
    pipeline set gradient-descent plan --file plan.json

`--pretty` turns on indentation for a human reading along.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from pipeline.config import use_work_dir
from pipeline.operations import (
    ARTIFACTS,
    OperationFailed,
    add_clip,
    add_plan_section,
    add_review_comment,
    check_readiness,
    create_project,
    describe_project,
    describe_stages,
    list_projects,
    read_artifact,
    seed_review_chapters,
    write_artifact,
    write_section_script,
)


def emit(value: Any, args: argparse.Namespace) -> int:
    """One output path for every command.

    `ensure_ascii` is deliberate: the Windows console defaults to cp1252 and
    raises UnicodeEncodeError on a bullet or an arrow, which would kill a command
    after it had already written the file -- the worst possible moment.
    """
    print(json.dumps(value, indent=2 if args.pretty else None, ensure_ascii=True))
    return 0


def read_document_argument(args: argparse.Namespace) -> dict[str, Any]:
    """Read a JSON document from `--file`, or from stdin when it is `-`/absent.

    Stdin is the default because that is what makes the CLI composable:
    `pipeline show A plan | edit | pipeline set B plan` needs no temp file.
    """
    if args.file and args.file != "-":
        with open(args.file, encoding="utf-8") as handle:
            text = handle.read()
    else:
        if sys.stdin.isatty():
            raise OperationFailed(
                "Expected a JSON document on stdin, or --file <path>. "
                "Nothing was piped in."
            )
        text = sys.stdin.read()

    try:
        document = json.loads(text)
    except json.JSONDecodeError as bad_json:
        raise OperationFailed(f"That is not valid JSON: {bad_json}") from bad_json

    if not isinstance(document, dict):
        raise OperationFailed(
            f"An artifact is a JSON object, not a {type(document).__name__}."
        )
    return document


# --- commands ---------------------------------------------------------------


def command_serve(args: argparse.Namespace) -> int:
    import uvicorn

    # ASCII only: see the note in `emit`.
    print(f"serving on http://{args.host}:{args.port}")
    uvicorn.run(
        "pipeline.web.app:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="warning",
    )
    return 0


def command_mcp(args: argparse.Namespace) -> int:
    """Run the MCP server on stdio, for an agent client to connect to."""
    from pipeline.mcp_server import run_stdio_server

    run_stdio_server()
    return 0


def command_stages(args: argparse.Namespace) -> int:
    return emit(describe_stages(), args)


def command_projects_list(args: argparse.Namespace) -> int:
    return emit(list_projects(), args)


def command_projects_create(args: argparse.Namespace) -> int:
    return emit(create_project(args.name), args)


def command_projects_show(args: argparse.Namespace) -> int:
    return emit(describe_project(args.project), args)


def command_show(args: argparse.Namespace) -> int:
    return emit(read_artifact(args.project, args.artifact), args)


def command_set(args: argparse.Namespace) -> int:
    return emit(write_artifact(args.project, args.artifact, read_document_argument(args)), args)


def command_plan_add_section(args: argparse.Namespace) -> int:
    return emit(
        add_plan_section(args.project, args.title, args.summary, args.seconds), args
    )


def command_plan_show(args: argparse.Namespace) -> int:
    from pipeline.plan_agent import read_planning

    return emit(read_planning(args.project), args)


def command_plan_say(args: argparse.Namespace) -> int:
    from pipeline.plan_agent import send_message

    return emit(send_message(args.project, args.message), args)


def command_plan_agree(args: argparse.Namespace) -> int:
    from pipeline.plan_agent import agree

    return emit(agree(args.project), args)


def command_plan_discard(args: argparse.Namespace) -> int:
    from pipeline.plan_agent import discard_proposal

    return emit(discard_proposal(args.project), args)


def command_script_write(args: argparse.Namespace) -> int:
    return emit(write_section_script(args.project, args.section, args.body), args)


def command_clip_add(args: argparse.Namespace) -> int:
    return emit(
        add_clip(args.project, args.track, args.kind, args.label,
                 args.start_ms, args.duration_ms, args.text),
        args,
    )


def command_review_comment(args: argparse.Namespace) -> int:
    return emit(
        add_review_comment(args.project, args.body, args.author, args.at_ms, args.route),
        args,
    )


def command_review_seed_chapters(args: argparse.Namespace) -> int:
    return emit(seed_review_chapters(args.project), args)


def command_agent_ask(args: argparse.Namespace) -> int:
    from pipeline.agent_runtime import ask_stage_agent

    return emit(ask_stage_agent(args.project, args.stage, args.question), args)


def command_agent_draft_unwritten(args: argparse.Namespace) -> int:
    from pipeline.script_drafting import draft_unwritten_sections

    return emit(draft_unwritten_sections(args.project, args.instruction), args)


def command_agent_draft_script(args: argparse.Namespace) -> int:
    from pipeline.agent_runtime import draft_section_script_with_agent

    return emit(
        draft_section_script_with_agent(args.project, args.section, args.instruction), args
    )


def command_voices(args: argparse.Namespace) -> int:
    from pipeline.operations import list_voice_providers

    return emit(list_voice_providers(), args)


def command_render(args: argparse.Namespace) -> int:
    from pipeline.operations import render_video

    return emit(render_video(args.project, args.voice_provider, args.voice), args)


def command_model_status(args: argparse.Namespace) -> int:
    from pipeline.llm import describe_model

    return emit(describe_model(), args)


def command_doctor(args: argparse.Namespace) -> int:
    found = check_readiness(args.deep)
    emit(found, args)
    return int(found["status"] == "fail")


# --- parser -----------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    # `--pretty` is accepted both before and after the subcommand, because
    # argparse otherwise only allows it before -- and everyone, model or human,
    # writes a trailing flag. SUPPRESS on the shared copy is what makes that
    # work: without it the subparser's default would overwrite a value already
    # set at the top level, so `pipeline --pretty show ...` would silently
    # produce dense JSON.
    shared_flags = argparse.ArgumentParser(add_help=False)
    shared_flags.add_argument(
        "--pretty", action="store_true", default=argparse.SUPPRESS,
        help="indent the JSON output",
    )

    parser = argparse.ArgumentParser(
        prog="pipeline",
        description="Explainer Pipeline. Every command prints JSON to stdout.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[shared_flags],
    )
    parser.set_defaults(pretty=False)
    sub = parser.add_subparsers(dest="command", required=True)

    def add_parser(group, name: str, **kwargs) -> argparse.ArgumentParser:
        """Every subcommand, at any depth, gets the shared flags."""
        return group.add_parser(name, parents=[shared_flags], **kwargs)

    p = add_parser(sub, "serve", help="run the web app")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8000)
    p.add_argument("--reload", action="store_true")
    p.set_defaults(fn=command_serve)

    p = add_parser(sub, "mcp", help="run the MCP server on stdio, for agent clients")
    p.set_defaults(fn=command_mcp)

    p = add_parser(sub, "stages", help="the six stages and what each produces")
    p.set_defaults(fn=command_stages)

    # --- projects ---
    projects = sub.add_parser("projects", help="list, create and inspect projects")
    projects_sub = projects.add_subparsers(dest="projects_command", required=True)

    p = add_parser(projects_sub, "list", help="every project")
    p.set_defaults(fn=command_projects_list)

    p = add_parser(projects_sub, "create", help="start a new project")
    p.add_argument("name")
    p.set_defaults(fn=command_projects_create)

    p = add_parser(projects_sub, "show", help="one project, with its stage status")
    p.add_argument("project")
    p.set_defaults(fn=command_projects_show)

    # --- generic artifact access ---
    artifact_names = sorted(ARTIFACTS)

    p = add_parser(sub, "show", help=f"print an artifact ({', '.join(artifact_names)})")
    p.add_argument("project")
    p.add_argument("artifact", choices=artifact_names)
    p.set_defaults(fn=command_show)

    p = add_parser(sub, "set", help="replace an artifact from JSON on stdin or --file")
    p.add_argument("project")
    p.add_argument("artifact", choices=artifact_names)
    p.add_argument("--file", help="path to a JSON file, or - for stdin (the default)")
    p.set_defaults(fn=command_set)

    # --- plan ---
    plan = sub.add_parser("plan", help="planning shortcuts")
    plan_sub = plan.add_subparsers(dest="plan_command", required=True)

    p = add_parser(plan_sub, "add-section", help="append a section to the plan")
    p.add_argument("project")
    p.add_argument("--title", required=True)
    p.add_argument("--summary", default="")
    p.add_argument("--seconds", type=int, default=60, help="estimated duration")
    p.set_defaults(fn=command_plan_add_section)

    p = add_parser(plan_sub, "show", help="the planning conversation and any proposed shape")
    p.add_argument("project")
    p.set_defaults(fn=command_plan_show)

    p = add_parser(plan_sub, "say",
                   help="tell the planning agent what you want; it proposes a shape (AI)")
    p.add_argument("project")
    p.add_argument("--message", required=True)
    p.set_defaults(fn=command_plan_say)

    p = add_parser(plan_sub, "agree",
                   help="agree to the proposed shape; its scenes are written (AI)")
    p.add_argument("project")
    p.set_defaults(fn=command_plan_agree)

    p = add_parser(plan_sub, "discard", help="throw away the proposed shape")
    p.add_argument("project")
    p.set_defaults(fn=command_plan_discard)

    # --- script ---
    script = sub.add_parser("script", help="scripting shortcuts")
    script_sub = script.add_subparsers(dest="script_command", required=True)

    p = add_parser(script_sub, "write", help="set the narration for one plan section")
    p.add_argument("project")
    p.add_argument("--section", required=True, help="a plan section id")
    p.add_argument("--body", required=True)
    p.set_defaults(fn=command_script_write)

    # --- studio ---
    studio = sub.add_parser("studio", help="composition shortcuts")
    studio_sub = studio.add_subparsers(dest="studio_command", required=True)

    p = add_parser(studio_sub, "add-clip", help="place a clip on a track")
    p.add_argument("project")
    p.add_argument("--track", required=True, help="a track id")
    p.add_argument("--kind", default="text",
                   choices=["video", "image", "text", "shape", "audio", "scene"])
    p.add_argument("--label", default="")
    p.add_argument("--start-ms", type=int, default=0, dest="start_ms")
    p.add_argument("--duration-ms", type=int, default=3000, dest="duration_ms")
    p.add_argument("--text", default="", help="on-screen text, for a text clip")
    p.set_defaults(fn=command_clip_add)

    # --- review ---
    review = sub.add_parser("review", help="reviewing shortcuts")
    review_sub = review.add_subparsers(dest="review_command", required=True)

    p = add_parser(review_sub, "comment", help="leave feedback, routed to a stage")
    p.add_argument("project")
    p.add_argument("--body", required=True)
    p.add_argument("--author", default="")
    p.add_argument("--at-ms", type=int, default=0, dest="at_ms")
    p.add_argument("--route", help="stage that should fix it",
                   choices=["extraction", "scene-plan", "script-staging", "studio"])
    p.set_defaults(fn=command_review_comment)

    p = add_parser(review_sub, "seed-chapters", help="rebuild chapters from the plan")
    p.add_argument("project")
    p.set_defaults(fn=command_review_seed_chapters)

    # --- agents ---
    agent = sub.add_parser("agent", help="run a stage's agent against a project")
    agent_sub = agent.add_subparsers(dest="agent_command", required=True)

    p = add_parser(agent_sub, "ask", help="ask a stage agent a question; writes nothing")
    p.add_argument("project")
    p.add_argument("stage",
                   choices=["extraction", "scene-plan", "script-staging", "studio", "reviewing"])
    p.add_argument("--question", required=True)
    p.set_defaults(fn=command_agent_ask)

    p = add_parser(agent_sub, "draft-script",
                   help="write narration for one plan section; saves it")
    p.add_argument("project")
    p.add_argument("--section", required=True, help="a plan section id")
    p.add_argument("--instruction", default="")
    p.set_defaults(fn=command_agent_draft_script)

    p = add_parser(agent_sub, "draft-unwritten",
                   help="write narration for every section that has none; saves it")
    p.add_argument("project")
    p.add_argument("--instruction", default="")
    p.set_defaults(fn=command_agent_draft_unwritten)

    p = add_parser(sub, "voices", help="text-to-speech providers and their availability")
    p.set_defaults(fn=command_voices)

    p = add_parser(sub, "render", help="synthesise narration and render the video")
    p.add_argument("project")
    p.add_argument("--voice-provider", default="", dest="voice_provider",
                   help="silent, edge, kokoro, piper, huggingface_local, "
                        "huggingface_api, openai_compatible, elevenlabs")
    p.add_argument("--voice", default="", help="provider-specific voice id")
    p.set_defaults(fn=command_render)

    p = add_parser(sub, "doctor", help="check tools, disk, memory and services before a job")
    p.add_argument("--deep", action="store_true", help="also call each service once")
    p.set_defaults(fn=command_doctor)

    p = add_parser(sub, "model", help="which model would be used, and whether a key is set")
    p.set_defaults(fn=command_model_status)

    from pipeline.cli_credentials import add_credentials_commands

    add_credentials_commands(sub, add_parser)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    use_work_dir()
    try:
        return args.fn(args)
    except OperationFailed as failure:
        # Message on stderr, non-zero exit: a caller piping stdout into `jq`
        # must not receive an error message where JSON was promised.
        print(f"error: {failure}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
