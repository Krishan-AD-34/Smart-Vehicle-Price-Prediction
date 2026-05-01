document.getElementById("predictForm").addEventListener("submit", async function(e){

    e.preventDefault();

   const data = {

    brand: document.getElementById("brand").value,
    car_age: parseInt(document.getElementById("car_age").value),
    fuel: document.getElementById("fuel").value,

    seller_type: document.getElementById("seller_type").value,
    owner: document.getElementById("owner").value,

    transmission: document.getElementById("transmission").value,
    km_driven: parseInt(document.getElementById("km_driven").value),
    mileage: parseFloat(document.getElementById("mileage").value),
    engine: parseInt(document.getElementById("engine").value)

};
    const response = await fetch('/predict', {
        method:'POST',
        headers:{
            'Content-Type':'application/json'
        },
        body:JSON.stringify(data)
    });

    const result = await response.json();

    if(result.predicted_price){
        document.getElementById("output").innerHTML =
            `Estimated Price: ₹ ${result.predicted_price}`;
    }
    else{
        document.getElementById("output").innerHTML =
            `Error: ${result.error}`;
    }

});