# Documentation

What the system is and how it works. The repository's own overview, its quick start
and the stage-by-stage description are in the [root README](../README.md); the picture
of the layers is [WORKFLOW-DIAGRAM.md](../WORKFLOW-DIAGRAM.md).

```text
docs/
├── README.md                          this index
├── architecture/
│   └── system-map.md                  boundaries, contracts and the rules that hold it together
└── operations/                        one procedure per layer: what it does, what it guarantees
    ├── extraction-pictures-sop.md     pictures taken from the source, and their checks
    ├── assets-and-design-sop.md       the picture library and the video's look
    ├── scene-plan-sop.md              the video's shape, agreed in a conversation
    ├── script-and-staging-sop.md      narration and what is on screen, per scene
    ├── generation-sop.md              making, approving and transferring the scenes
    ├── scene-programs-sop.md          a scene program, how it is made, its renderers and checks
    └── change-flags-sop.md            what happens downstream when an earlier layer changes
```

Each agent's instructions are in [agents/](../agents), and the kits and method notes the
scene programs are written with are in [resources/](../resources).
