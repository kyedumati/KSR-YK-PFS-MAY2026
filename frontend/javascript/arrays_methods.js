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

const products = [
    {product_id: 1, name: "iphone17 pro max", category: "electronics", price: 139450, stock: 3},
    {product_id: 2, name: "airpods", category: "electronics", price: 16000, stock: 3},
    {product_id: 3, name: "Tshirt", category: "fashion", price: 499, stock: 3},
    {product_id: 4, name: "Attitude Is Everything by James keller", category: "Books", price: 499, stock: 3}
]

export default products; // this will make products array to be avaiable other files
export default categories;

// export keyword is used to share functions, variables or classes, object from one javascript file, so that other files can use thems



