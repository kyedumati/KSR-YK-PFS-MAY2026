// An objects is group of key and value pairs
const product = {
    id : 6,
    name: 'running shoes',
    brand: 'puma',
    price: '4999',
    in_stock: true,
    sizes: [7,8,9,10,11],
    "manfacturing-year": 2025
}

console.log(product["price"]) // with the key
console.log(product.name) //dot notation
const key = "brand"
console.log(product[key])

console.log(product.sizes)

console.log(product.sizes[3])
console.log(product.sizes.length)


// add, update and delete itesm from objects
const cartItem = {product_id: 6, qty: 1}

cartItem.qty = 2;  // modify or update
console.log("cartItem", cartItem)
cartItem.size = 10;  // add or update if the key is exist
console.log("cartItem", cartItem)
delete cartItem.size;  // delete key and value pair from json
console.log("cartItem", cartItem)

// pull name, brand and price into their own variables
const pan = { id: 12, name: "Non-stick Pan", brand: "Prestige", price: 1599, stock: 35 };
const { name, brand, price } = pan;
console.log(`${name} - ${brand} - ₹${price.toLocaleString("en-IN")}`);

// copy the line and replace qty; the original line is left as it was
const updateQty = (cartItem, qty) => ({ ...cartItem, qty });
const line = { product_id: pan.id, name, brand, price, qty: 1 };
const updatedLine = updateQty(line, 3);
console.log("line before", line);
console.log("updated line", updatedLine);
console.log("line total", `₹${(updatedLine.price * updatedLine.qty).toLocaleString("en-IN")}`);


// cartItem = {"employee_id": "1234"} // TypeError: Assignment to constant variable.
// console.log(cartItem)

// a function stores in an object is called method,
const cart = {
    items: [
    ],
    add(price, qty) {
        this.items.push({price, qty});
        return this;
    },
    totalValue(){
        return this.items.reduce((sum, item) => sum + item.price * item.qty, 0);
    }
}


console.log("Cart Total", cart.totalValue())
console.log("adding item to the cart", cart.add(1299, 2))
console.log("Cart Total", cart.totalValue())

// Dealing with JSON objects
const order = {
    id : "375609710903",
    total : 2598,
    paid : true,
    status : "shipped",
    items : [{product_id: 6, qty: 1}],
    placed_date : new Date("2026-11-24T08:33:00")
}

const text = JSON.stringify(order, null, 4)
console.log(text)

// {"id":"375609710903","total":2598,"paid":true,"status":"shipped","items":
//     [{"product_id":6,"qty":1}],"placed_date":"2026-11-24T03:03:00.000Z"}
console.log(typeof text)
let backendResponse = '{"id":"375609710903","total":2598,"paid":true,"status":"shipped","items":[{"product_id":6,"qty":1}],"placed_date":"2026-11-24T03:03:00.000Z"}'
console.log(backendResponse.id)
try {
    backendResponse = JSON.parse(backendResponse)
    const testResp = JSON.parse("{name:'baddata'")
} catch(error) {
    console.log(error.name, error.message)
}
console.log(backendResponse.id)