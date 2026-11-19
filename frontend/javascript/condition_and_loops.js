const totalBill = 999
const expressDelivery = false
const isPrimeMember = false

let deliveryPrice;

if (expressDelivery) {
    deliveryPrice = 49
} else if(isPrimeMember || totalBill > 999) {
    deliveryPrice = 0
} else {
   deliveryPrice = 40
}

console.log(`Total ${totalBill}, delivery changes are ${deliveryPrice} and finall payable amount is: ${totalBill+ deliveryPrice}`)


const stock = 0;
const label = stock > 0 ? "In Stock" : "Out of stock"

console.log(label)

// switch --> whenever you compare one value against many fixed values then switch is better for readability and maintainability
deliveryStatus = "abc"

switch(deliveryStatus) { // by default will compare with ===
    case "pending":
        console.log("We've received your order, waiting for shippments")
        break;
    case "shipped":
        console.log("Your are order is shipped, and its on the way")
        // break;
    case "delivered":
        console.log("your order has been delivered and thanks for shopping with us.")
        // break;
    case "cancelled":
    case "returned":
        console.log("this order was cancelled, your money will be refunded within 24 hours")
        break;
    default:
        console.log("Unknown status")
        break;
}


// const values = [0, 1, "", "0", " ", null, undefined, [], {}, "false", NaN];
for(let i=1; i<=10; i++) { // i =1; true; blocks : increment()
    console.log(`Incrementing value ${i}`)
}

const numbers = [10,20,30,40,50]
for(const i of numbers) {
    console.log(`numbers is ${i}`)
}

const cartItems = [
    {"productName": "Symbol Premium Women's Fit & Flare Wrap Dress", "price": "429", "quantity": "3"},
     {"productName": "T-shirt", "price": "1999", "quantity": "1"}
]

for(const item of cartItems) {
    console.log(item.productName, item.price) // item.get("productName")
}


let saving = 560000;
const perMonthExpenditure = 45000;
let months = 0;

while(saving>perMonthExpenditure) { //i need to iterate this loop until saving money is less than 45000
   months++;
   saving-=perMonthExpenditure 
}

console.log(`Your saving money is sufficient for only for ${months} months and remaining balance will be ${saving}`)

let correctPin = 1234
let attempts = 0;
let enteredPin = 0;
do {
    attempts++
    console.log("attempt", attempts)
    // enteredPin = Number(prompt("Enter your ATM pin:"))
    enteredPin = 123
    if(enteredPin != correctPin) {
        console.log("Invalid pin entereed")
        continue;
    }
    
} while(attempts<3)