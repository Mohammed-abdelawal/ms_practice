const express = require('express');
const { createYoga, createSchema } = require('graphql-yoga');

const service = require('./productsService');

const app = express();

// The schema is the contract: types, what can be asked, what can be changed.
// The resolvers are thin -- they only translate GraphQL arguments into service
// calls, so the storage can change without touching this file.
const schema = createSchema({
    typeDefs: /* GraphQL */ `
        type Product {
            id: Int!
            name: String!
            price: Float!
        }

        type Query {
            products: [Product!]!
            product(id: Int!): Product
        }

        type Mutation {
            addProduct(name: String!, price: Float!): Product!
            updateProduct(id: Int!, name: String, price: Float): Product
            deleteProduct(id: Int!): Boolean!
        }
    `,
    resolvers: {
        Query: {
            products: () => service.listProducts(),
            product: (_, { id }) => service.getProduct(id)
        },
        Mutation: {
            addProduct: (_, { name, price }) => service.addProduct(name, price),
            // Only the arguments the client sent are present in `fields`.
            updateProduct: (_, { id, ...fields }) => service.updateProduct(id, fields),
            deleteProduct: (_, { id }) => service.deleteProduct(id)
        }
    }
});

const yoga = createYoga({ schema });
app.use(yoga.graphqlEndpoint, yoga);

app.listen(3000, () => {
    console.log("GraphQL ready on http://localhost:3000/graphql");
});
