function agregarFila() {
  const contenedor = document.getElementById("contenedor-ingredientes");
  const fila = document.createElement("div");

  const botonEnviar = document.getElementById("btn-enviar-ingredientes");
  botonEnviar.style.display = "inline-block"; 

  fila.className = "bg-white bg-opacity-90 p-4 rounded-lg shadow flex flex-col md:flex-row md:items-end gap-4";

  fila.innerHTML = `
  <input type="text" name="ingrediente[]" placeholder="Ingrediente" required
    class="w-full md:w-1/6 p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-lime-500">

  <input type="number" name="cantidad[]" placeholder="Cantidad" required
    class="w-full md:w-1/6 p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-lime-500">

  <select name="unidad[]" required
    class="w-full md:w-1/6 p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-lime-500">
    <option value="" disabled selected>Unidad</option>
    <option value="gr">gr</option>
    <option value="kg">kg</option>
    <option value="unidad">unidad</option>
  </select>

  <select name="tipo[]" onchange="toggleFecha(this)" required
    class="w-full md:w-1/6 p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-lime-500">
    <option value="natural">Natural</option>
    <option value="envasado">Envasado</option>
  </select>

  <select name="guardado[]" required
    class="w-full md:w-1/6 p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-lime-500">
    <option value="" disabled selected>Guardado</option>
    <option value="fresco">Fresco</option>
    <option value="camara">Cámara</option>
    <option value="ambiente">Ambiente</option>
  </select>

  <input type="date" name="vencimiento[]" disabled
    class="w-full md:w-1/6 p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-lime-500">

  <button type="button" onclick="eliminarFila(this)"
    class="text-red-600 hover:font-bold hover:text-red-800 transition">Eliminar</button>
`;

  contenedor.appendChild(fila);
}

function eliminarFila(btn) {
  btn.parentElement.remove();
}

function toggleFecha(select) {
  const fecha = select.parentElement.querySelector('input[type="date"]');
  fecha.disabled = (select.value !== "envasado");
}


function mostrarVista(idVista) {
  document.getElementById("vista-menu").style.display = "none";
  document.getElementById("logo-karu").style.display = "none";

  const menu = document.getElementById("menu-principal");
  menu.classList.remove("hidden");
  menu.classList.add("flex");


  document.querySelectorAll(".vista").forEach(v => {
    v.style.display = "none";
    v.classList.remove("animate-fadeIn");
  });

  const seleccionada = document.getElementById(idVista);
  if (seleccionada) {
    seleccionada.style.display = "block";
    seleccionada.classList.add("animate-fadeIn");
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
}

function volverAlInicio() {
  document.getElementById("vista-menu").style.display = "flex";
  document.getElementById("logo-karu").style.display = "flex";

  const menu = document.getElementById("menu-principal");
  menu.classList.add("hidden");
  menu.classList.remove("flex");

  document.querySelectorAll(".vista").forEach(v => {
    v.style.display = "none";
    v.classList.remove("animate-fadeIn");
  });

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function toggleListaIngredientes() {
  const lista = document.getElementById("lista-ingredientes");
  lista.classList.toggle("hidden");
}

document.getElementById("ingredientes-form").addEventListener("submit", 
  function (e) {
  e.preventDefault();

  const filas = document.querySelectorAll("#contenedor-ingredientes > div");
  const ingredientes = [];

  filas.forEach(fila => {
    const ingrediente = fila.querySelector('input[name="ingrediente[]"]').value;
    const cantidad = parseInt(fila.querySelector('input[name="cantidad[]"]').value);
    const unidad = fila.querySelector('select[name="unidad[]"]').value;
    const tipo = fila.querySelector('select[name="tipo[]"]').value;
    const guardado = fila.querySelector('select[name="guardado[]"]').value;
    const vencimiento = fila.querySelector('input[name="vencimiento[]"]').value || null;

    ingredientes.push({ ingrediente, cantidad, unidad, tipo, guardado, vencimiento });
  });

  fetch("/agregar-ingredientes", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(ingredientes)
  }).then(res => {
    if (res.ok) {
      alert("Ingredientes agregados correctamente");
      location.reload();
    } else {
      alert("Hubo un error al guardar los ingredientes.");
    }
  });
});

document.addEventListener("DOMContentLoaded", () => {
  // Mostrar y ocultar formulario
  const btnMostrar = document.getElementById("btn-mostrar-formulario");
  const seccionFormulario = document.getElementById("vista-formulario_receta");

  btnMostrar.addEventListener("click", () => {
    const visible = seccionFormulario.style.display === "block";
    seccionFormulario.style.display = visible ? "none" : "block";
    btnMostrar.textContent = visible ? "Agregar nueva receta" : "Ocultar formulario";
  });

  // Enviar formulario
  document.getElementById("form-nueva-receta").addEventListener("submit", async (e) => {
    e.preventDefault(); 

    const form = e.target;
    const datos = {
      nombre_receta: form.nombre_receta.value,
      descripcion: form.descripcion.value,
      ingredientes: form.ingredientes.value,
      pasos: form.pasos.value,
      tiempo: form.tiempo.value,
      categoria: form.categoria.value,
      dieta: form.dieta.value,
      porciones: parseInt(form.porciones.value),
      calorias: parseInt(form.calorias.value),
      proteina: form.proteina.value,
      grasa: form.grasa.value,
      carbohidratos: form.carbohidratos.value
    };

    const res = await fetch("/crear-receta", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(datos)
    });

    if (res.ok) {
      alert("Receta agregados correctamente");
      location.reload();
    } else {
      alert("Hubo un error al guardar la receta.");
    }
  });

  // Buscador de recetas
  const input = document.getElementById("buscador-recetas");
  input?.addEventListener("change", () => {
    buscarReceta(input.value);
  });

  input?.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      buscarReceta(input.value);
    }
  });

  let todasLasRecetas = [];

  document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("buscador-recetas");
    const botonBuscar = document.getElementById("btn-buscar-receta");

  input.addEventListener("change", () => {
    buscarReceta(input.value);
  });

  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      buscarReceta(input.value);
    }
  });

  botonBuscar.addEventListener("click", () => {
    buscarReceta(input.value);
  });

  const btnMostrar = document.getElementById("btn-mostrar-formulario");
  const seccionFormulario = document.getElementById("vista-recetas");

  btnMostrar.addEventListener("click", () => {
    const visible = seccionFormulario.style.display === "block";
    seccionFormulario.style.display = visible ? "none" : "block";
  });
});




  fetch("/todas-las-recetas")
    .then(res => res.json())
    .then(data => {
      todasLasRecetas = data;

      const datalist = document.getElementById("recetas-lista");
      datalist.innerHTML = "";

      data.forEach(receta => {
        const option = document.createElement("option");
        option.value = receta.nombre_receta;
        datalist.appendChild(option);
      });
    })
    .catch(err => console.error("Error al cargar las recetas:", err));
  

  function buscarReceta(nombre) {
    const recetaSeleccionada = todasLasRecetas.find(
      r => r.nombre_receta.toLowerCase() === nombre.toLowerCase()
    );

    if (recetaSeleccionada) {
      mostrarReceta(recetaSeleccionada);
    }
  }

  function mostrarReceta(receta) {
    document.getElementById("vista-comidas").style.display = "block";
    
    const contenedor = document.getElementById("detalle-receta");

    contenedor.innerHTML = `
      <div class="bg-white bg-opacity-90 p-6 rounded-lg shadow-md">
        <h2 class="text-2xl font-bold mb-2 text-gray-800">${receta.nombre_receta}</h2>
        <p class="text-gray-600 mb-4 italic">${receta.descripcion}</p>
        <div class="text-sm text-gray-500 mb-6">
          ⏱️ Tiempo: <strong>${receta.tiempo}</strong> &nbsp; 🍽️ Porciones: <strong>${receta.porciones}</strong> &nbsp; 🗂️ Categoría: <strong>${receta.categoria}</strong>
        </div>
        <h3 class="font-semibold text-lime-700 mb-2">🥕 Ingredientes:</h3>
        <ul class="list-disc pl-5 mb-4">
          ${receta.ingredientes.split(';').map(ing => `<li>${ing.trim()}</li>`).join('')}
        </ul>
        <h3 class="font-semibold text-blue-700 mb-2">📋 Pasos:</h3>
        <ol class="list-decimal pl-5 mb-4">
          ${receta.pasos.split('|').map(p => `<li>${p.trim()}</li>`).join('')}
        </ol>
        <h3 class="font-semibold text-purple-700 mb-2">🍎 Información nutricional:</h3>
        <p class="text-gray-700">
          Calorías: <strong>${receta.calorias}</strong>, 
          Proteína: <strong>${receta.proteina}</strong>, 
          Grasa: <strong>${receta.grasa}</strong>, 
          Carbohidratos: <strong>${receta.carbohidratos}</strong>
        </p>
      </div>
    `;
  }
});

document.getElementById("btn-solicitar-receta").addEventListener("click", async () => {
  try {
    const response = await fetch("/generar-receta-inteligente", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      }
    });

    const data = await response.json();

    if (response.ok) {
      console.log("Receta generada:", data.receta);
      // Si querés mostrarlo en el HTML, podés agregarlo a un div
      alert(`Receta generada: ${data.receta.nombre_receta}`);
    } else {
      alert(data.error || "Ocurrió un error.");
    }

  } catch (error) {
    console.error("Error:", error);
    alert("No se pudo conectar con el servidor.");
  }
});
