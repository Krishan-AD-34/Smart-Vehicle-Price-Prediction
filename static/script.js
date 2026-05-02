// ========================================
// ELEMENTS
// ========================================

const brandSelect =
    document.getElementById("brand");

const modelSelect =
    document.getElementById("car_name");

const resultBox =
    document.getElementById("result");

// ========================================
// LOAD MODELS DYNAMICALLY
// ========================================

brandSelect.addEventListener(
    "change",
    async () => {

        const brand = brandSelect.value;

        // RESET MODEL
        modelSelect.innerHTML = `
            <option value="">
                Loading Models...
            </option>
        `;

        // RESET SPECS
        document.getElementById("mileage").value = "";
        document.getElementById("engine").value = "";
        document.getElementById("max_power").value = "";
        document.getElementById("seats").value = "";

        if (!brand) {

            modelSelect.innerHTML = `
                <option value="">
                    Select Model
                </option>
            `;

            return;
        }

        try {

            const response = await fetch(
                `/get_models/${brand}`
            );

            const models = await response.json();

            modelSelect.innerHTML = `
                <option value="">
                    Select Model
                </option>
            `;

            models.forEach(model => {

                const option =
                    document.createElement(
                        "option"
                    );

                option.value = model;

                option.textContent = model;

                modelSelect.appendChild(option);
            });

        }

        catch(error){

            console.log(error);

            modelSelect.innerHTML = `
                <option value="">
                    Failed To Load Models
                </option>
            `;
        }
    }
);

// ========================================
// AUTO FILL VEHICLE SPECS
// ========================================

modelSelect.addEventListener(
    "change",
    async () => {

        const model =
            modelSelect.value;

        if(!model) return;

        try {

            const response = await fetch(
                `/get_specs/${model}`
            );

            const specs =
                await response.json();

            document.getElementById(
                "mileage"
            ).value = specs.mileage;

            document.getElementById(
                "engine"
            ).value = specs.engine;

            document.getElementById(
                "max_power"
            ).value = specs.max_power;

            document.getElementById(
                "seats"
            ).value = specs.seats;

        }

        catch(error){

            console.log(error);
        }
    }
);

// ========================================
// FORM SUBMIT
// ========================================

document
.getElementById("predictForm")

.addEventListener(
    "submit",

    async function(e){

        e.preventDefault();

        // ========================================
        // LOADING
        // ========================================

        resultBox.innerHTML = `

            <div class="loading">

                Predicting Vehicle Price...

            </div>

        `;

        // ========================================
        // FORM DATA
        // ========================================

        const data = {

            brand:
                document
                .getElementById("brand")
                .value,

            car_name:
                document
                .getElementById("car_name")
                .value,

            vehicle_age:
                parseFloat(
                    document
                    .getElementById("vehicle_age")
                    .value
                ),

            km_driven:
                parseFloat(
                    document
                    .getElementById("km_driven")
                    .value
                ),

            seller_type:
                document
                .getElementById("seller_type")
                .value,

            fuel_type:
                document
                .getElementById("fuel_type")
                .value,

            transmission_type:
                document
                .getElementById("transmission_type")
                .value,

            mileage:
                parseFloat(
                    document
                    .getElementById("mileage")
                    .value
                ),

            engine:
                parseFloat(
                    document
                    .getElementById("engine")
                    .value
                ),

            max_power:
                parseFloat(
                    document
                    .getElementById("max_power")
                    .value
                ),

            seats:
                parseFloat(
                    document
                    .getElementById("seats")
                    .value
                )
        };

        console.log(data);

        // ========================================
        // API CALL
        // ========================================

        try {

            const response = await fetch(
                "/predict",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify(data)
                }
            );

            const result =
                await response.json();

            // ========================================
            // SUCCESS
            // ========================================

            if(result.success){

                resultBox.innerHTML = `

                    <div class="price">

                        ${result.predicted_price}

                    </div>

                    <div class="details">

                        <p>

                            Estimated Range:

                            ${result.lower_price}

                            -

                            ${result.upper_price}

                        </p>

                        <p>

                            Prediction Confidence:

                            ${result.confidence}

                        </p>

                    </div>

                `;
            }

            // ========================================
            // ERROR
            // ========================================

            else{

                resultBox.innerHTML = `

                    <div class="error">

                        ${result.error}

                    </div>

                `;
            }

        }

        // ========================================
        // SERVER ERROR
        // ========================================

        catch(error){

            console.log(error);

            resultBox.innerHTML = `

                <div class="error">

                    Server Error

                </div>

            `;
        }
    }
);