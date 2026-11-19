console.log("Hello everyone, welcome to javascript") //print statment in python
console.log("20+30 =", 20+30)

const webpageName = "KSR Mart"
try { //try block
    webpageName = "Kasi"
    console.log(webpageName)
} catch(error) { // catch block
    console.log("error while reassinging const vartiable:", error.name, error.message)
}

/*let cartCount = 0; // if we are creating variable with let, we can modify them
cartCount = cartCount + 1;

cartCount += 2;
console.log(webpage_name, cartCount)*/

/*var cartCount = 0; // if we are creating variable with let, we can modify them
cartCount = cartCount + 1;

cartCount += 2;
console.log(webpage_name, cartCount)*/

let trainerName = "kasi yedumati" // declaration + initialisaiton

let trainer; // declaration
console.log(trainer)
trainer = "kasi yedumati"// initialisation

// datatypes
let studentData;
console.log(typeof "kasi yedumati")
console.log(typeof 599)
console.log(typeof false)
console.log(typeof null) //object
console.log(typeof studentData)
studentData = {"name":"kasi yedumait", "rollno": 1234}
console.log(typeof studentData)
let student_ids = [123,234,555,666]
console.log(typeof student_ids)