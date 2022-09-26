
## Release of V0.1.0

We have released version 0.1.0. We now support different components of model registry. Here is the list of actionable items that are supported in the release version.


- Projects:
    - create: Create a new project
    - list: List existing projects created by a user
    - details: Fetch details for an existing project
    - clone: Clone an existing project and set it as current project
- Models:
    - register: Register a production ready model(in-memory) to the remote model registry
    - fetch: Fetch any model from the model registry as python object
    - list: List all the registered models under a project
    - details: Fetch details for an existing model
    - delete: Delete a model from the model registry
- Metrics:
    - add: Add metrics obtained for a model
    - fetch: Fetch the metrics added for a model. To obtain selective metrics, a key has to be passed
    - delete: Delete an added metric
- Params:
    - add: Add params related to a model
    - fetch: Fetch the params added for a model. To obtain selective params, a key has to be passed
    - delete: Delete an added param
- Artifacts:
    - add: Add artifacts for a registered model. 
    - details: Obtain the details for the added artifacts. 
    - fetch: Fetch the added artifacts. Fetched artifacts will be stored in local disk
    - delete: Delete the added artifacts