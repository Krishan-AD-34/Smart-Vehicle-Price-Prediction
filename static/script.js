document.getElementById("predictForm").addEventListener("submit", async function(e){

    e.preventDefault();

    // Show loading
    document.getElementById("output").innerHTML =
        "Predicting vehicle price...";

    const data = {

        brand: document.getElementById("brand").value,

        car_age: parseInt(
            document.getElementById("car_age").value
        ),

        fuel: document.getElementById("fuel").value,

        seller_type: document.getElementById("seller_type").value,

        owner: document.getElementById("owner").value,

        transmission: document.getElementById("transmission").value,

        km_driven: parseInt(
            document.getElementById("km_driven").value
        ),

    };

    try {

        const response = await fetch('/predict', {

            method:'POST',

            headers:{
                'Content-Type':'application/json'
            },

            body:JSON.stringify(data)
        });

        const result = await response.json();

        // Success
        if(result.predicted_price){

            document.getElementById("output").innerHTML = `

                <div class="result-card">

                    <h2>
                        Estimated Vehicle Price
                    </h2>

                    <h1>
                        ₹ ${result.lower_price.toLocaleString()}
                        -
                        ₹ ${result.upper_price.toLocaleString()}
                    </h1>

                    <p>
                        Average Estimated Price:
                        ₹ ${result.predicted_price.toLocaleString()}
                    </p>

                    <p>
                        Prediction Confidence:
                        ${result.confidence}%
                    </p>

                </div>

            `;
        }

        // Error
        else{

            document.getElementById("output").innerHTML =

                `<span style="color:red;">
                    Error: ${result.error}
                </span>`;
        }

    }

    catch(error){

        document.getElementById("output").innerHTML =

            `<span style="color:red;">
                Server Error
            </span>`;
    }

});