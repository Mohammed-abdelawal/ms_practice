// The products store, independent of how it is exposed.
//
// The GraphQL resolvers call these functions, so swapping the in-memory object
// for a database means changing this file and nothing else. Nothing here knows
// about GraphQL or HTTP -- it returns null or false and lets the transport
// decide what that means on the wire.

let products = {
    1: { id: 1, name: "Product 1", price: 10 },
    2: { id: 2, name: "Product 2", price: 20 },
    3: { id: 3, name: "Product 3", price: 30 }
};

function listProducts() {
    return Object.values(products);
}

// The product, or null if there is no such id.
function getProduct(id) {
    return products[id] ?? null;
}

function addProduct(name, price) {
    const id = Math.max(0, ...Object.keys(products).map(Number)) + 1;
    products[id] = { id, name, price };
    return products[id];
}

// Merge the given fields into the product; null if there is no such id.
function updateProduct(id, fields) {
    const product = products[id];
    if (!product) {
        return null;
    }
    Object.assign(product, fields);
    return product;
}

// True if a product was removed, false if there was nothing to remove.
function deleteProduct(id) {
    if (!products[id]) {
        return false;
    }
    delete products[id];
    return true;
}

module.exports = {
    listProducts,
    getProduct,
    addProduct,
    updateProduct,
    deleteProduct
};
