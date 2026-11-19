const productName = "puma shoes";
const price = 4999;

console.log("purchasing shoes of brand and it cost is 4999") 
console.log(`purchasing ${productName} and its cost is ${price}`)

const message = `your purhcase of puma shoes is confirmed!
It will be delivered in 1 or 2days`;
console.log(message)


console.log(productName.length)
console.log(productName.toUpperCase())
console.log(productName.includes("shoes"))
console.log(productName.includes("Shoes"))
console.log(productName.includes("shoes", 6))
console.log(productName.slice(0,6))

var stmt = "welcome to KSR, python full stack training at KSR"
console.log(stmt.replace("KSR", "Kasi"))
console.log(stmt.replaceAll("KSR", "Kasi"))

console.log(stmt.split(","))
console.log(" iphone 17 pro max      ".trim())
console.log(" iphone 17 pro max      ".trim().replaceAll(" ", ""))

console.log("+91"+ "75".padStart(10, "X"))

console.log("kasi yedumati".substring(4))

console.log("kasi yedumati".substring(4, 8))


