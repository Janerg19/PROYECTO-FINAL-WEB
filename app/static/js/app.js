const state = {

    /*
     * Si tiene valor significa que estamos editando.
     */

    editingId: null,


    /*
     * Guardamos los productos recibidos
     * desde la API.
     */

    products: []
};


/*
 * ============================================================
 * MENSAJES
 * ============================================================
 */

function showMessage(
    message,
    type = "success"
) {

    const element =
        document.getElementById(
            "message"
        );


    element.textContent =
        message;


    element.classList.remove(
        "hidden",
        "bg-green-100",
        "text-green-800",
        "bg-red-100",
        "text-red-800"
    );


    if (type === "success") {

        element.classList.add(
            "bg-green-100",
            "text-green-800"
        );

    } else {

        element.classList.add(
            "bg-red-100",
            "text-red-800"
        );
    }


    setTimeout(
        function () {

            element.classList.add(
                "hidden"
            );

        },
        3000
    );
}


/*
 * ============================================================
 * SEGURIDAD FRONTEND
 * ============================================================
 *
 * Escapamos contenido antes de introducirlo
 * mediante innerHTML.
 */

function escapeHtml(value) {

    return String(value)

        .replaceAll(
            "&",
            "&amp;"
        )

        .replaceAll(
            "<",
            "&lt;"
        )

        .replaceAll(
            ">",
            "&gt;"
        )

        .replaceAll(
            '"',
            "&quot;"
        )

        .replaceAll(
            "'",
            "&#039;"
        );
}


/*
 * ============================================================
 * MOSTRAR APLICACIÓN
 * ============================================================
 */

function showApplication() {

    document
        .getElementById(
            "auth-section"
        )
        .classList.add(
            "hidden"
        );


    document
        .getElementById(
            "app-shell"
        )
        .classList.remove(
            "hidden"
        );


    document
        .querySelectorAll(
            "[data-screen]"
        )
        .forEach(function (button) {
            if (button.id !== "logout-button") {
                button.classList.remove("hidden");
            }
        });


    document
        .getElementById(
            "logout-button"
        )
        .classList.remove(
            "hidden"
        );

    showScreen("dashboard");
    renderDashboardSummary();
}


/*
 * ============================================================
 * MOSTRAR LOGIN
 * ============================================================
 */

function showLogin() {

    document
        .getElementById(
            "auth-section"
        )
        .classList.remove(
            "hidden"
        );


    document
        .getElementById(
            "app-shell"
        )
        .classList.add(
            "hidden"
        );


    document
        .querySelectorAll(
            "[data-screen]"
        )
        .forEach(function (button) {
            if (button.id !== "logout-button") {
                button.classList.add("hidden");
            }
        });


    document
        .getElementById(
            "logout-button"
        )
        .classList.add(
            "hidden"
        );
}


/*
 * ============================================================
 * REGISTRO
 * ============================================================
 */

async function register() {

    try {

        /*
         * Obtenemos información
         * desde el formulario.
         */

        const payload = {

            name:
                document.getElementById(
                    "register-name"
                ).value,

            email:
                document.getElementById(
                    "register-email"
                ).value,

            password:
                document.getElementById(
                    "register-password"
                ).value
        };


        /*
         * Axios realiza:

         * POST /api/auth/register
         */

        const response =
            await api.post(
                "/auth/register",
                payload
            );


        showMessage(
            response.data.message
        );


    } catch (error) {

        showMessage(

            error.response?.data?.message ||
            "Error al registrar usuario",

            "error"
        );
    }
}


/*
 * ============================================================
 * LOGIN
 * ============================================================
 */

async function login() {

    try {

        const payload = {

            email:
                document.getElementById(
                    "login-email"
                ).value,

            password:
                document.getElementById(
                    "login-password"
                ).value
        };


        /*
         * Axios:
         *
         * POST /api/auth/login
         */

        const response =
            await api.post(
                "/auth/login",
                payload
            );


        /*
         * Obtenemos los datos
         * devueltos por Flask.
         */

        const data =
            response.data.data;


        /*
         * Guardamos el JWT.
         */

        localStorage.setItem(
            "access_token",
            data.access_token
        );


        /*
         * Guardamos información
         * básica del usuario.
         */

        localStorage.setItem(
            "user",
            JSON.stringify(
                data.user
            )
        );


        /*
         * Mostramos la aplicación.
         */

        showApplication();


        /*
         * Cargamos productos.
         */

        await loadProducts();


    } catch (error) {

        showMessage(

            error.response?.data?.message ||
            "Credenciales inválidas",

            "error"
        );
    }
}


/*
 * ============================================================
 * LOGOUT
 * ============================================================
 */

function logout() {

    localStorage.removeItem(
        "access_token"
    );


    localStorage.removeItem(
        "user"
    );


    location.reload();
}


/*
 * ============================================================
 * GET PRODUCTS
 * ============================================================
 */

async function loadProducts() {

    try {

        /*
         * GET /api/products/
         *
         * Axios agrega automáticamente:
         *
         * Authorization: Bearer TOKEN
         */

        const response =
            await api.get(
                "/products/"
            );


        /*
         * Guardamos los datos.
         */

        state.products =
            response.data.data;


        /*
         * Actualizamos el HTML.
         */

        renderProducts(
            state.products
        );


    } catch (error) {

        showMessage(

            error.response?.data?.message ||
            "Error cargando productos",

            "error"
        );
    }
}


/*
 * ============================================================
 * RENDER PRODUCTOS
 * ============================================================
 */

function renderDashboardSummary() {

    const totalProducts = state.products.length;

    const totalStock = state.products.reduce(
        function (sum, product) {
            return sum + Number(product.stock || 0);
        },
        0
    );

    const totalValue = state.products.reduce(
        function (sum, product) {
            return sum + Number(product.price || 0) * Number(product.stock || 0);
        },
        0
    );

    const user = JSON.parse(
        localStorage.getItem("user") || "{}"
    );

    const dashboardUser = document.getElementById("dashboard-username");
    const dashboardProducts = document.getElementById("dashboard-total-products");
    const dashboardStock = document.getElementById("dashboard-total-stock");
    const dashboardValue = document.getElementById("dashboard-total-value");
    const profileName = document.getElementById("profile-name");
    const profileEmail = document.getElementById("profile-email");

    if (dashboardUser) {
        dashboardUser.textContent = user.name || "Usuario";
    }

    if (profileName) {
        profileName.textContent = user.name || "-";
    }

    if (profileEmail) {
        profileEmail.textContent = user.email || "-";
    }

    if (dashboardProducts) {
        dashboardProducts.textContent = totalProducts;
    }

    if (dashboardStock) {
        dashboardStock.textContent = totalStock;
    }

    if (dashboardValue) {
        dashboardValue.textContent = `$${Number(totalValue).toLocaleString("es-CO")}`;
    }
}


function showScreen(screenName) {

    document
        .querySelectorAll(".app-screen")
        .forEach(function (screen) {
            screen.classList.add("hidden");
        });

    const target = document.getElementById(`${screenName}-screen`);

    if (target) {
        target.classList.remove("hidden");
    }

    document
        .querySelectorAll("[data-screen]")
        .forEach(function (button) {
            if (button.id === "logout-button") {
                return;
            }

            const active = button.dataset.screen === screenName;

            button.classList.toggle("bg-indigo-600", active);
            button.classList.toggle("text-white", active);
            button.classList.toggle("bg-slate-200", !active);
            button.classList.toggle("text-slate-700", !active);
        });
}


function renderProducts(
    products
) {

    const tbody =
        document.getElementById(
            "products-body"
        );


    /*
     * Limpiamos la tabla.
     */

    tbody.innerHTML = "";


    /*
     * Recorremos los productos.
     */

    products.forEach(
        function (product) {

            const row =
                document.createElement(
                    "tr"
                );


            row.className =
                "border-b hover:bg-slate-50";


            /*
             * Creamos el HTML de cada fila.
             */

            row.innerHTML = `

                <td class="px-4 py-4">
                    ${product.id}
                </td>


                <td class="px-4 py-4 font-semibold">
                    ${escapeHtml(
                        product.name
                    )}
                </td>


                <td class="px-4 py-4">
                    ${escapeHtml(
                        product.description || ""
                    )}
                </td>


                <td class="px-4 py-4">
                    $${Number(
                        product.price
                    ).toLocaleString(
                        "es-CO"
                    )}
                </td>


                <td class="px-4 py-4">
                    ${product.stock}
                </td>


                <td class="px-4 py-4">

                    <div class="flex gap-2">

                        <button
                            onclick="editProduct(${product.id})"
                            class="rounded-lg
                                   bg-yellow-500
                                   px-3 py-2
                                   text-white"
                        >
                            Editar
                        </button>


                        <button
                            onclick="deleteProduct(${product.id})"
                            class="rounded-lg
                                   bg-red-600
                                   px-3 py-2
                                   text-white"
                        >
                            Eliminar
                        </button>

                    </div>

                </td>
            `;


            tbody.appendChild(
                row
            );
        }
    );
}


/*
 * ============================================================
 * CREATE / UPDATE
 * ============================================================
 */

async function saveProduct() {

    /*
     * Obtenemos información del formulario.
     */

    const payload = {

        name:
            document.getElementById(
                "product-name"
            ).value,

        description:
            document.getElementById(
                "product-description"
            ).value,

        price:
            Number(
                document.getElementById(
                    "product-price"
                ).value
            ),

        stock:
            Number(
                document.getElementById(
                    "product-stock"
                ).value
            )
    };


    try {

        /*
         * Si editingId tiene valor:
         *
         * estamos actualizando.
         */

        if (state.editingId) {

            await api.put(

                `/products/${state.editingId}`,

                payload
            );


            showMessage(
                "Producto actualizado"
            );


        } else {

            /*
             * De lo contrario:
             *
             * CREATE
             */

            await api.post(
                "/products/",
                payload
            );


            showMessage(
                "Producto creado"
            );
        }


        /*
         * Limpiamos formulario.
         */

        resetForm();


        /*
         * Volvemos a consultar API.
         */

        await loadProducts();


    } catch (error) {

        showMessage(

            error.response?.data?.message ||
            "Error guardando producto",

            "error"
        );
    }
}


/*
 * ============================================================
 * EDITAR
 * ============================================================
 */

function editProduct(id) {

    /*
     * Buscamos el producto
     * en nuestro estado local.
     */

    const product =
        state.products.find(
            function (item) {

                return item.id === id;
            }
        );


    if (!product) {

        return;
    }


    /*
     * Guardamos ID del producto.
     */

    state.editingId = id;


    /*
     * Cargamos información
     * dentro del formulario.
     */

    document.getElementById(
        "product-name"
    ).value =
        product.name;


    document.getElementById(
        "product-description"
    ).value =
        product.description || "";


    document.getElementById(
        "product-price"
    ).value =
        product.price;


    document.getElementById(
        "product-stock"
    ).value =
        product.stock;


    /*
     * Cambiamos título.
     */

    document.getElementById(
        "form-title"
    ).textContent =
        `Editar producto #${id}`;
}


/*
 * ============================================================
 * DELETE
 * ============================================================
 */

async function deleteProduct(id) {

    /*
     * Confirmación antes de eliminar.
     */

    const confirmed =
        confirm(
            "¿Deseas eliminar este producto?"
        );


    if (!confirmed) {

        return;
    }


    try {

        /*
         * DELETE /api/products/<id>
         */

        await api.delete(
            `/products/${id}`
        );


        showMessage(
            "Producto eliminado"
        );


        /*
         * Actualizamos la tabla.
         */

        await loadProducts();


    } catch (error) {

        showMessage(

            error.response?.data?.message ||
            "Error eliminando producto",

            "error"
        );
    }
}


/*
 * ============================================================
 * RESET FORM
 * ============================================================
 */

function resetForm() {

    state.editingId = null;


    document.getElementById(
        "form-title"
    ).textContent =
        "Nuevo producto";


    document.getElementById(
        "product-form"
    ).reset();
}


/*
 * ============================================================
 * INICIALIZACIÓN
 * ============================================================
 */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        /*
         * Obtenemos el token.
         */

        const token =
            localStorage.getItem(
                "access_token"
            );


        /*
         * Eventos del formulario de registro.
         */

        document
            .getElementById(
                "register-button"
            )
            .addEventListener(
                "click",
                register
            );


        /*
         * Evento login.
         */

        document
            .getElementById(
                "login-button"
            )
            .addEventListener(
                "click",
                login
            );


        /*
         * Evento logout.
         */

        document
            .getElementById(
                "logout-button"
            )
            .addEventListener(
                "click",
                logout
            );


        /*
         * Evento formulario de producto.
         */

        document
            .getElementById(
                "product-form"
            )
            .addEventListener(
                "submit",
                function (event) {

                    /*
                     * Evitamos que el navegador
                     * recargue la página.
                     */

                    event.preventDefault();


                    saveProduct();
                }
            );


        /*
         * Botón cancelar edición.
         */

        document
            .getElementById(
                "cancel-edit"
            )
            .addEventListener(
                "click",
                resetForm
            );


        document
            .querySelectorAll("[data-screen]")
            .forEach(function (button) {
                if (button.id === "logout-button") {
                    return;
                }

                button.addEventListener("click", function () {
                    showScreen(button.dataset.screen);
                });
            });

        /*
         * Si existe JWT:
         *
         * el usuario está autenticado.
         */

        if (token) {

            showApplication();

            loadProducts();

        } else {

            showLogin();
        }
    }
);