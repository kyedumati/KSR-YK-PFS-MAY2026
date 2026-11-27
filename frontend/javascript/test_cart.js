// const pan = { id: 12, name: "Non-stick Pan", brand: "Prestige", price: 1599, stock: 35 };
// const { name, brand, price } = pan;
// console.log(`${name} - ${brand} - ₹${price.toLocaleString("en-IN")}`);

// copy the line and replace qty; the original line is left as it was
const updateQty = (cartItem, qty) => ({ ...cartItem, qty });
const line = { product_id: 123, brand: "Prestige", price: 1599, qty: 1 };
const updatedLine = updateQty(line, 3);
console.log("line before", line);
console.log("updated line", updatedLine);
console.log("line total", `₹${(updatedLine.price * updatedLine.qty).toLocaleString("en-IN")}`);