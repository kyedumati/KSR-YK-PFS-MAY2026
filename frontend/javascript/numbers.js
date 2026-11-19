const price = 1499; // tshirt puma
const quantity = 5; 
const gstRate = 0.18;

console.log(price * quantity) 
const gstValue = price * quantity * gstRate
console.log(gstValue)
console.log((price * quantity) + gstValue)

console.log(0.2 + 0.6)
console.log(0.2 - 0.6)
console.log(0.2 * 0.6)

console.log(Math.round(3.147))

console.log(Math.round(3.5))
console.log(Math.floor(3.147))
console.log(Math.floor(3.5))
console.log(Math.floor(3.9))
console.log(Math.ceil(3.9))
console.log(Math.ceil(3.147))


console.log(Math.max(499, 1299, 1699, 1690), Math.min(499, 1299, 1699, 1690))

console.log((127900).toLocaleString("en-IN"))


console.log((127900).toLocaleString("en-IN", {style : "currency", currency: "INR"}))


//type casting/conversion 
const cartQuantity = "6"
console.log(Number(cartQuantity) + 4)

// parseInt, parseFloat, parseBool

const mobileHeight = "691.667px"
console.log(parseInt(mobileHeight))
console.log(parseFloat(mobileHeight))
console.log(Number("kasi yedumati"))

console.log(String(499))
console.log(Boolean(0))
console.log(Boolean(12))
console.log(Boolean(""))
console.log(Boolean("0"))
console.log(Boolean("abc"))
// if(Number("kasi yedumati") == NaN)

