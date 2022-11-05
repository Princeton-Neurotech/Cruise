# Netlify internal helpers for OneGraph


## Install

```
npm install netlify-onegraph-internal
```

## Example

```ts
import { OneGraphClient } from "netlify-onegraph-internal";

console.log(OneGraphClient);
```

### Developing

- While the multi-file branch in the CLI isn't ready:

1. Update the GraphQL schema with:
```shell
$ npx get-graphql-schema "https://graph.netlify.com/graphql?app_id=NETLIFY_SITE_ID"
```
2. Add a new `.graphql` file under `./netlify/functions/netlifyGraph/operations`
3. Don't forget to add a `@netlify(id: SOME_UUID)` directive to the operation
4. run `cat ./netlify/functions/netlifyGraph/operations/*` > operations.graphql`
   to bundle all the operations into a single file
5. run `ntl graph:library`
