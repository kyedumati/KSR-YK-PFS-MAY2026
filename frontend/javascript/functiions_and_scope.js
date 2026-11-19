// someone is tryin to shop in amazon, they are going to generate some bill, and some people may or may not prime account
// prime vs non prime, totalbill is > 1000
function deliveryCharges(isPrimeMember, totalBill, expressDelivery) {
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

function display() {
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






