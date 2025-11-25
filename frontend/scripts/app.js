const components = [
  "api",
  "db",
  "cache",
  "queue",
  "custom"
];

async function loadComponents() {
  const container = document.getElementById("panels");

  for (let name of components) {
    const html = await fetch(`components/${name}.html`).then(r => r.text());
    const wrapper = document.createElement("div");
    wrapper.innerHTML = html;
    container.appendChild(wrapper);
  }
}

// Component loader
loadComponents();


// Aşağıda önceki fonksiyonlar
async function callService(method, path, body, outputId) {
  const out = document.getElementById(outputId);
  out.classList.remove("placeholder");
  out.textContent = "İstek atılıyor...";

  try {
    const opts = { method, headers: {} };

    if (body && method !== "GET") {
      opts.headers["Content-Type"] = "application/json";
      opts.body = body;
    }

    const res = await fetch(path, opts);
    const text = await res.text();

    out.textContent = `Status: ${res.status}\n\n${text}`;
  } catch (err) {
    out.textContent = "Hata: " + err.message;
  }
}

function runPreset(selId, outId) {
  const value = document.getElementById(selId).value;
  callService("GET", value, null, outId);
}

function runDbPreset() {
  const sel = document.getElementById("db-endpoint-select");
  const value = sel.value;
  const body = document.getElementById("db-body").value;

  if (value === "/db/migrate")
    callService("POST", value, body, "db-output");
  else
    callService("GET", value, null, "db-output");
}

function setCache() {
  const key = document.getElementById("cache-key").value;
  const value = document.getElementById("cache-value").value;
  callService("POST", "/cache/set", JSON.stringify({ key, value }), "cache-output");
}

function getCache() {
  const key = document.getElementById("cache-key-get").value;
  callService("GET", "/cache/get?key=" + key, null, "cache-output");
}

function runCustom() {
  const method = document.getElementById("custom-method").value;
  const path = document.getElementById("custom-path").value;
  const body = document.getElementById("custom-body").value;
  callService(method, path, body, "custom-output");
}
