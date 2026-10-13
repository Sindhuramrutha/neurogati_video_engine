# Robustness plan: no crash, no silent default

The Demo 001 run (21 slides, 43 scenes) stopped or degraded nine times. None was
exotic; each was an outside service behaving as outside services do, or a path
no test walked:

| What happened | Root cause |
|---|---|
| Run stopped on Edge "NoAudioReceived" (x2) | free service throttles bursts; one failure stopped the job |
| 429 from the model provider | each process paced itself; two processes doubled the rate |
| Script drafting took 75 min | provider stalled; 600 s timeout x 3 silent retries |
| A vision answer cut off | thinking tokens counted against a 1,500 budget |
| First render failed | a new code path (scene-by-scene narration) never ran in a test |
| A crashed scene showed "working" forever | the worker logged the exception, never wrote "failed" |
| A narration failure killed a scene before round 1 | measuring the narration sat outside the scene's error handling |
| Badges and covers became scene pictures | nothing asked whether a picture teaches |
| Most scenes ended below the quality bar | six rounds, then the best was used, with nothing more tried |

Research agrees with what the run showed: throttle and space requests to Edge,
retry with backoff and jitter, honour Retry-After, share a circuit breaker
across processes, make stages idempotent and checkpointed, and quarantine a
failing item instead of failing the run ([edge-tts #74](https://github.com/rany2/edge-tts/issues/74),
[AWS agentic lens REL07](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentrel07-bp02.md),
[retry patterns](https://fast.io/resources/ai-agent-retry-patterns/)).

## Principles

1. **Every outside call goes through one gate** (`resilience.py`): a timeout,
   retries with exponential backoff and full jitter, Retry-After honoured, the
   failure classed as *transient* (try again later) or *permanent* (a bad key,
   a bad request: stop and say so), and a circuit breaker per service shared by
   every process on the machine. When a service is down, work waits; it does not
   hammer the service or fail item after item.
2. **One item never stops a job.** A scene, a section, a picture that fails is
   recorded with its reason, and the rest go on.
3. **Every long job is resumable from where it stopped**, and a job stopped by a
   transient outage resumes on its own (decided: pause and auto-resume; the voice
   never changes mid-video).
4. **The state on disk is always the truth.** No "working" left behind by a crash.
5. **Check before starting.** A pre-flight (`pipeline doctor`) checks every tool
   and service a job will need, before the job spends anything.
6. **Quality is worked for, not defaulted.** A scene that has not met the bar
   after its rounds escalates (fresh approach, new picture, different shot); the
   best version is used only after the ladder is exhausted, and every such scene
   is named on the Export page and in the report.
7. **No path ships untested.** An end-to-end smoke test (a 2-slide deck, upload
   to export, stand-in AI and voice, real Manim and ffmpeg) must pass before any
   commit, with fault-injection tests for each failure above.

## Work

| # | Change | Where |
|---|---|---|
| R1 | Status truth: a crashed scene is `failed` with its error; narration measuring inside the scene's handling; drafting saves each section as it lands and isolates any exception; storyboard goes past a failing card | scene_agent, scene_maker, script_drafting, storyboard |
| R2 | `resilience.py`: retry policy (backoff + jitter + Retry-After), transient/permanent classes, cross-process circuit breaker; used by Edge and HTTP voices, image painting, scene model calls, vision | new + speech, llm, scene_illustration, scene_maker |
| R3 | Render auto-resume: a render stopped by a transient failure waits and resumes by itself (5 min, growing, up to 12 h), from its checkpoint; the queue shows why and when | render_queue |
| R4 | `pipeline doctor`: ffmpeg/ffprobe, uv, a 1-second Manim render, disk space, write access, model key and a one-token call, vision, voice; run before a render and before scene making; on the API for the app | new doctor.py, cli, routes |
| R5 | Quality ladder: after 6 rounds below the bar, up to 2 escalations of 4 rounds each (fresh program with a different shot; repaint the picture from the reviewer's notes); best-of only after that, and named | scene_maker |
| R6 | Smoke test + fault injection + a pre-commit hook running lint and the fast suite with the smoke test | tests, tools/hooks |
