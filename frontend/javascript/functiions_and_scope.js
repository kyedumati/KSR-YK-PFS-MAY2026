// someone is tryin to shop in amazon, they are going to generate some bill, and some people may or may not prime account
// prime vs non prime, totalbill is > 1000
export function deliveryCharges(isPrimeMember, totalBill, expressDelivery) {
    // let deliveryCharges;

    if (expressDelivery) {
        return 49
    } else if(isPrimeMember || totalBill > 999) {
        return 0
    } else {
        return 40
    }
    // return deliveryCharges;
}

export function display() {
    console.log("dispaly function")
}

// 2nd way to create function expression
const formatRupees = function(amount) {
    return amount.toLocaleString("en-IN", {style: "currency", currency: "INR"});
}

console.log("formatted price", formatRupees(9999))

console.log("delivery charge",formatRupees(deliveryCharges(true, 1299, false)))
console.log("delivery charge",formatRupees(deliveryCharges(false, 1299, false)))
console.log("delivery charge",formatRupees(deliveryCharges(false, 499, false)))

console.log(display())

// arrow functions : lambda expressions : anonymous functions
const subTotal = (price, quantity) => price * quantity // simple expresion and it automatically returns the value
console.log(formatRupees(subTotal(429, 3)))


// function parameters
// default arguments
function priceWithTax(amount, rate= 0.18) { // rate is default param/arguments
    return Math.round((amount*rate)+amount);
}

console.log(priceWithTax(1000)) //it will use default 18% rate
console.log(priceWithTax(1200, 0.05)) // it is going to overrid rate of interest to 5%, in case of books

// missing to pass or pass extra arguments
function calTotal(price, qty) {
    return price * qty
}

console.log(calTotal(499, 2)) // this works as expected
console.log(calTotal(499, 2, "kasi")) // extra arugments will be ignored
console.log(calTotal(499)) // missed args going to get undefined 

// variable length arguments/ any number of arguments
function cartTotal(...prices) { // python *args // it is going to store in an array
    let sum =0;
    for(const p of prices) {
        sum += p;
    }
    return sum ;
}

console.log(calTotal(1299, 499))
console.log(calTotal(1299, 499, 999))

console.log(calTotal(1299, 499, 999,12345,12345,12345,12345,2345,234))

function sum(a,b) {
    return [a,b]
}


// import products from "./arrays_methods.js"
// console.log(products)


export const projectName = "KSR Mart"
export {deliveryCharges as dc, display as dp}; 