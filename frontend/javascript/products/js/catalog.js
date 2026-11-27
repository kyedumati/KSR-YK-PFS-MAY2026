import products from "./products-data.js";

const grid = document.querySelector("#product-grid");
const resultCount = document.querySelector("#result-count");

const formatRupees = amount => amount.toLocaleString("en-IN", {style:"currency", currency:"INR"});

function productCard(product) {
    // it is going to generate card or article for each product
    /*
        <article class="product-card">
            <img src="images/employee_01.png" alt="Ananya Rao">
            <h2>Ananya Rao</h2>
            <p>Senior Software Engineer</p>
        </article>
    */
    const card = document.createElement("article");
    card.className = "product-card";
    card.dataset.id = product.id;
    card.dataset.price = product.price;

    card.innerHTML = `
            <img src="images/${product.image}" alt="" width="400" height="300">
            <h3></h3>
            <p><span class="price"> ${formatRupees(product.price)} </span>
            </p> 
            <p class="stock-label"> ${product.stock > 0 ? `${product.stock} in stock` : "Out of stock"} </p>
            `;
    card.querySelector("img").alt = product.name;
    card.querySelector("h3").textContent = product.name;

    return card;

}


function renderProducts(products) {
    for(const product of products) {
        grid.append(productCard(product))
    }
}

renderProducts(products);

console.log("redendered products", grid.children.length)

