// comparision operatos
console.log(1299 > 699)
console.log(1299 < 699)

console.log(499 == 499)
console.log(499 == "499") // true // it will convert the types first and then compare 
console.log(499 === "499") // false
console.log(5 !== "5")

// logical operators &&, ||, ! (Python: AND, OR, NOT)

const orderTotal = 499;
const isPrimeMember = false;

const freeDelivery = isPrimeMember || orderTotal >= 1000;
console.log("Free develiery? ", freeDelivery)

const inStock = true;
const amazonBal = 1000
const canBuy = inStock && amazonBal > orderTotal;
console.log("can he buy?", canBuy)

const isLoggedIn = false
if(!isLoggedIn) {
    console.log("You have not actually logged in , please login to access this page")
}





