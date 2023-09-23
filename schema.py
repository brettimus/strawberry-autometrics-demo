import typing
from fastapi import FastAPI, Response
import strawberry
from strawberry.fastapi import GraphQLRouter
from autometrics import autometrics
from prometheus_client import generate_latest

@strawberry.type
class Book:
    title: str
    author: str


@strawberry.type
class Query:
    books: typing.List[Book]


def get_books():
    return [
        Book(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
        ),
    ]


@strawberry.type
class Query:
    books: typing.List[Book] = strawberry.field(resolver=get_books)

    # NOTE - `@autometrics` broke unless it was the first decorator on top of the resolver
    #        We get the error `AttributeError: 'StrawberryField' object has no attribute '__qualname__'`
    @autometrics
    @strawberry.field
    def last_book(self) -> Book:
        return get_books()[-1]


schema = strawberry.Schema(query=Query)

graphql_app = GraphQLRouter(schema)

app = FastAPI()

# Set up the graphql server
app.include_router(graphql_app, prefix="/graphql")

# Set up a metrics endpoint for Prometheus to scrape
#   `generate_latest` returns metrics data in the Prometheus text format
@app.get("/metrics")
def metrics():
    return Response(generate_latest())

