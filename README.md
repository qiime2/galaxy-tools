# QIIME 2 Galaxy Tools

**Current Version:** 2026.1

**Toolshed Link:** [QIIME 2 Core Distribution](https://toolshed.g2.bx.psu.edu/repository?repository_id=d256b91a26ac697f)

## How to update the tools
All tools and ToolShed metadata are generated directly by [q2galaxy](https://github.com/qiime2/q2galaxy).
The renderer runs inside a QIIME 2 distribution image layered with a selected q2galaxy release from PyPI.
These `*.xml` and `.shed.yml` files should not be manually modified.
The Dockerfiles for the runtime and Galaxy server images are maintained under
`docker/` in this repository as part of the published Galaxy tool set.

The state of this repo is controlled by `distros.yaml` in the root.
To add or update tools, modify that file and merge the change before rendering.

To publish a new set of wrappers, manually run the `Render Galaxy Tools`
workflow with the released QIIME 2 image, the q2galaxy version published to
PyPI, and a tag for the layered runtime image. The workflow pushes the runtime
to Quay, renders wrappers containing its immutable digest, and opens one PR
containing both tools and collections. After merge, the deployment workflow
uploads all changed tool repositories before uploading the collections.
