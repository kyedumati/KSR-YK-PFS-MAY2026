console.log("document object:",document)
console.log("document object:",document)
console.log(document.title)
let headerContent = document.querySelector("#header1"); // i want to get html element whose id is header1
console.log(headerContent, headerContent.textContent)
// document.querySelectorAll()

const pList = document.querySelectorAll(".sales_message") // this functions is going to return NodeList who is matching class .sales_message

for(const p of pList) {
    console.log("parapgras: ", p.textContent)
}

let liItems = document.querySelectorAll(".electronics li")
for(const li in liItems) {
    console.log(li)
    console.log("li text:", li.textContent)
}

const header1 = document.getElementById("header1")
console.log("header1....:", header1)

const salesmessages = document.getElementsByClassName("sales_message")
console.log(salesmessages)

const tagList = document.getElementsByTagName("li")
console.log("taglist: ", tagList)


// get the
const helloAnchor = document.querySelector("#hello")

// chaning the elements 
header1.textContent = "Diwali deals"


// header1.innerHTML = "Prices drop at <strong>midnight</strong>!"; // parses HTML

// Attributes
const hello = document.querySelector("#hello");
hello.setAttribute("href", "https://ksrdatavizon.com/");
// hello.getAttribute("href");
hello.textContent = "FAQ";
console.log("link now goes to", hello.getAttribute("href"));



// creating, inserting and removing

let electronicsList = document.querySelector(".electronics")
const li = document.createElement("li") //  a new element , detached element
li.textContent = "Yoga mat"
li.dataset.price = "999" // <li data-price="999"> </li>



const li2 = document.createElement("li") //  a new element , detached element
li2.textContent = "Trimmer"
li2.dataset.price = "1999" // <li data-price="999"> </li>
li2.dataset.id = "5"

electronicsList.append(li); // add as a new child for the existing child
electronicsList.prepend(li2); // add as a new child for the existing child

li.remove()
