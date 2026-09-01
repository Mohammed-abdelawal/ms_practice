const express = require('express');
const app = express();


let products = {
    1: { id: 1, name: "Product 1", price: 10 },
    2: { id: 2, name: "Product 2", price: 20 },
    3: { id: 3, name: "Product 3", price: 30 }
};



app.get("/products", (req,res) => {
    res.json(Object.values(products));
});

app.get("/products/:id", (req,res) => {
    const productId = parseInt(req.params.id);
    const product = products[productId];
    if(product) {
        res.json(product);
    } else {
        res.status(404).json({msg: "Product not found"});
    }
});

app.post("/products", (req,res) => {
    const newProduct = {
        id: products.length + 1,
        name: req.body.name,
        price: req.body.price
    };
    products[newProduct.id] = newProduct;
    res.status(201).json(newProduct);
});

app.delete("/products/:id", (req,res) => {
    const productId = parseInt(req.params.id);
    if(!products[productId]) {
        return res.status(404).json({msg: "Product not found"});
    }
    delete products[productId];
    res.status(204).send();
});

app.put("/products/:id", (req, res) => {
    const productId = parseInt(req.params.id);
    if(!products[productId]) {
        return res.status(404).json({msg: "Product not found"});
    }
    products[productId] = {
        id: productId,
        name: req.body.name,
        price: req.body.price
        };
        res.json(products[productId]);
});


app.listen(3000, () => {
    console.log("Server is running on port 3000");
});