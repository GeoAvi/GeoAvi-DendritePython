from flask import Flask, request, jsonify
from flask_graphql import GraphQLView
from graphene import ObjectType, String, Field, List, Mutation, Schema
from keycloak import KeycloakOpenID
import stripe

app = Flask(__name__)
app.config['SECRET_KEY'] = '3809d38438c5e693a95abdc86c3d7cc8'

# Keycloak configuration
keycloak_openid = KeycloakOpenID(
    server_url='https://your-keycloak-server.com/auth/',
    client_id='your-client-id',
    realm_name='your-realm',
    client_secret_key='your-client-secret'
)

# Stripe configuration
stripe.api_key = 'your-stripe-secret-key'

# Define the Todo model
class TodoType(ObjectType):
    id = String()
    title = String()
    description = String()
    time = String()
    images = List(String)

# Define the Todo queries
class Query(ObjectType):
    todos = List(TodoType)
    todo = Field(TodoType, id=String())

    def resolve_todos(self, info):
        # Example todos data
        todos = [
            {'id': '1', 'title': 'Sample Todo', 'description': 'This is a sample todo', 'time': '2024-08-26T12:00:00Z', 'images': []}
        ]
        return [TodoType(**todo) for todo in todos]

    def resolve_todo(self, info, id):
        # Example todo data
        todo = {'id': '1', 'title': 'Sample Todo', 'description': 'This is a sample todo', 'time': '2024-08-26T12:00:00Z', 'images': []}
        if todo['id'] == id:
            return TodoType(**todo)
        return None

# Define the Todo mutations
class CreateTodoMutation(Mutation):
    class Arguments:
        title = String()
        description = String()
        time = String()

    todo = Field(TodoType)

    def mutate(self, info, title, description, time):
        # Example new todo creation
        new_todo = {'id': 'new-id', 'title': title, 'description': description, 'time': time, 'images': []}
        return CreateTodoMutation(todo=TodoType(**new_todo))

class UpdateTodoMutation(Mutation):
    class Arguments:
        id = String()
        title = String()
        description = String()
        time = String()

    todo = Field(TodoType)

    def mutate(self, info, id, title, description, time):
        # Example todo update
        updated_todo = {'id': id, 'title': title, 'description': description, 'time': time, 'images': []}
        return UpdateTodoMutation(todo=TodoType(**updated_todo))

class DeleteTodoMutation(Mutation):
    class Arguments:
        id = String()

    success = String()

    def mutate(self, info, id):
        # Example todo deletion
        return DeleteTodoMutation(success="true")

# Define the schema
class Mutation(ObjectType):
    create_todo = CreateTodoMutation.Field()
    update_todo = UpdateTodoMutation.Field()
    delete_todo = DeleteTodoMutation.Field()

schema = Schema(query=Query, mutation=Mutation)

# Create the GraphQL view
view = GraphQLView.as_view('graphql', schema=schema, batch=True)

# Register the GraphQL view
app.add_url_rule('/graphql', view_func=view)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
