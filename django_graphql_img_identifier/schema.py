import graphene
from images import schema


class Query(schema.Query, graphene.ObjectType):
    pass


class Mutation(schema.ImageMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)