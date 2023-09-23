# FastAPI + Strawberry + Autometrics

> I followed the Strawberry + FastAPI integration docs at [https://strawberry.rocks/docs/integrations/fastapi](https://strawberry.rocks/docs/integrations/fastapi)

To run this example:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn schema:app --reload --port=8000
```

Then open [http://localhost:8000/graphql](http://localhost:8000/graphql) in your browser, which should show the GraphQL Playground.

Try the named query `lastBook`, which is instrumented with autometrics:

```graphql
{
  lastBook {
    title
  }
}
```

You can also try the named query `books`, but I wasn't able to instrument this one with autometrics. I think we'd need to instrument the resolver itself, absent some modifications to the autometrics library to support `@strawberry.field`:



```graphql
{
  books {
    title
    author
  }
}
```

## Adding Metrics

We can use the the autometrics cli to get going fast with prometheus locally.

Once that's installed, we just need to tell it how to scrape the example app:

```bash
# Install the CLI
brew install autometrics-dev/tap/am
# Boot up Prometheus and the Explorer
am start :8000
# Visit the explorer
open http://localhost:6789
```

After you've used the `lastBook` query a few times (via the GraphiQL interface), you should see metrics in the explorer.