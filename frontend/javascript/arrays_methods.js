import {deliveryCharges as ds, display, projectName} from "./functiions_and_scope.js"
// array is an ordered list of values
const prices = [79999, 999, 699]
const categories = ["Electronics", "books", "Fashion", "Footwear", "Food Items"]
const emptyArray = []
const mixedData = ["iphone17 pro max", 139450] // 


console.log(categories[0], categories[3])
console.log(categories.length)

console.log(categories[categories.length-1], categories.at(-1))

console.log(categories[6])

export const products = [
    {product_id: 1, name: "iphone17 pro max", category: "electronics", price: 139450, stock: 3},
    {product_id: 2, name: "airpods", category: "electronics", price: 16000, stock: 3},
    {product_id: 3, name: "Tshirt", category: "fashion", price: 499, stock: 3},
    {product_id: 4, name: "Attitude Is Everything by James keller", category: "Books", price: 499, stock: 3},
    {product_id: 5, name: "iphone15 pro max", category: "electronics", price: 109450, stock: 3},
]

// export {products}; // this will make products array to be avaiable other files
// export {categories};

// export keyword is used to share functions, variables or classes, object from one javascript file, so that other files can use thems


// different methods on arrays
const recentlyViewed = ["Nike shoes", "Puma shoes"]
recentlyViewed.push("airpods 2nd generation") 
console.log("Recently viewed list", recentlyViewed)

recentlyViewed.unshift("iphone 17 pro max")
console.log("Recently viewed list", recentlyViewed)

recentlyViewed.pop()
console.log(recentlyViewed)
recentlyViewed.shift()
console.log(recentlyViewed)
recentlyViewed.push("airpods 2nd generation", "hoodie", "trousers") 

console.log(recentlyViewed)

recentlyViewed.splice(1, 3)
console.log(recentlyViewed)

let slicedList = recentlyViewed.slice(1, 4)
console.log(slicedList)


// searching or reading
let categoryCheck = p => p.category == "electronics"

let nameCheck = p => p.name.includes("iphone")
// function categoryCheck(product, searchString) {
//     return product.category == searchString 
// }
console.log(products.find(categoryCheck))
console.log(products.filter(categoryCheck))
console.log("all products contains iphone", products.filter(nameCheck))
/* 
let filteredProducts = []
function findProductsByCategory(categoryCheck) {
    for(const product of products) {
        if(categoryCheck(product)) {
            filteredProducts.push(product);
        }
    }
    return filteredProducts;
}
*/

// console.log(findProductsByCategory(categoryCheck))

const index = products.findIndex(p => p.name.includes("shirt"))
console.log("find index value:", index)


const mappedProducts = products.map(p => ({name: p.name, category: p.category, price: p.price, priceWithGst:Math.round(p.price * 0.18)}))
console.log("mappedProducts", mappedProducts)

// reduce : combine every item in the list to one value
// const total = products.reduce
// let total = 0;
// for(let product of products) {
//     total += product.price * product.stock
// }
// total value of all stock, start at 0, add price * stock of each product
const total = products.reduce((sum, p) => sum+p.price*p.stock, 0);
console.log("total cart value is:", total)

const priceList = [1299, 499, 999, 2599]
const names = ["kasi", "rithwik", "mohan", "varshith", "chandu"]
console.log(priceList.sort((a, b) => a - b))
console.log(names.sort())

for(const price of priceList) {
    
}