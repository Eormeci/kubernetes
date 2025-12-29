let dbReady = false;

const components = [
  "api",
  "db",
  "cache",
  "queue",
  "custom"
];

loadComponents();

async function loadComponents() {
  const container = document.getElementById("panels");

  for (let name of components) {
    const html = await fetch(`components/${name}.html`).then(r => r.text());
    const wrapper = document.createElement("div");
    wrapper.innerHTML = html;
    container.appendChild(wrapper);
  }
}

// --- DB placeholder güncelleme --- //
document.addEventListener("change", (e) => {
  if (e.target.id !== "db-endpoint-select") return;

  const textarea = document.getElementById("db-body");
  const value = e.target.value;

  let example = `{ "example": "data" }`;

  switch (value) {
    case "/db/ping":
      example = "// ping body almaz";
      break;

    case "GET:/db/users":
      example = "// GET /db/users body almaz";
      break;

    case "POST:/db/users":
      example = JSON.stringify({
        name: "Ahmet",
        email: "ahmet@example.com"
      }, null, 2);
      break;

    case "PUT:/db/users":
      example = JSON.stringify({
        id: 1,
        name: "Yeni İsim",
        email: "yeni@example.com"
      }, null, 2);
      break;

    case "DELETE:/db/users":
      example = JSON.stringify({
        id: 1
      }, null, 2);
      break;

    case "POST:/db/migrate":
      example = "// migrate body almaz";
      break;
  }

  textarea.value = example;
});


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

document.addEventListener("DOMContentLoaded", () => {
    // DB paneli yüklendiğinde yalnız migrate aktif kalsın
    lockDbActions(true);
});

function lockDbActions(lock) {
    const select = document.getElementById("db-endpoint-select");

    for (let option of select.options) {
        if (!option.value.includes("migrate")) {
            option.disabled = lock;
        }
    }

    // UI efekti - tasarıma dokunmadan sadece blur
    select.style.filter = lock ? "blur(2px)" : "none";
}

async function runDbPreset() {
    const raw = document.getElementById('db-endpoint-select').value;
    const bodyText = document.getElementById('db-body').value;
    const output = document.getElementById('db-output');

    output.classList.remove('placeholder');
    output.textContent = 'Gönderiliyor...';

    // --- endpoint + method ayırma ---
    let method = "GET";
    let endpoint = raw;

    if (raw.includes(":")) {
        const [m, url] = raw.split(":");
        method = m.trim();
        endpoint = url.trim();
    }

    let options = { method, headers: {} };

    if (method !== "GET") {
        options.headers["Content-Type"] = "application/json";

        if (bodyText.trim()) {
            try {
                options.body = JSON.stringify(JSON.parse(bodyText));
            } catch (err) {
                output.textContent = "JSON hatası: " + err.message;
                return;
            }
        }
    }

    try {
        const res = await fetch(endpoint, options);
        const ok = res.ok;

        let data;
        try {
            data = await res.json();
        } catch {
            data = await res.text();
        }

        output.textContent = JSON.stringify(data, null, 2);

        // migrate başarılıysa diğer endpointler açılsın
        if (endpoint === "/db/migrate" && ok) {
            dbReady = true;
            lockDbActions(false);
        }

    } catch (err) {
        output.textContent = "Fetch Hatası: " + err.message;
    }
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

// --- SQLite API CRUD işlemleri ---
async function fetchItems() {
    const output = document.getElementById("db-output");
    output.textContent = "Fetching items...";

    try {
        const response = await fetch("/api/items");
        const items = await response.json();
        output.textContent = JSON.stringify(items, null, 2);
    } catch (error) {
        output.textContent = "Error: " + error.message;
    }
}

async function addItem() {
    const name = document.getElementById("item-name").value;
    const description = document.getElementById("item-description").value;
    const output = document.getElementById("db-output");

    try {
        const response = await fetch("/api/items", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, description })
        });
        const result = await response.json();
        output.textContent = JSON.stringify(result, null, 2);
    } catch (error) {
        output.textContent = "Error: " + error.message;
    }
}

async function updateItem() {
    const id = document.getElementById("item-id").value;
    const name = document.getElementById("item-name").value;
    const description = document.getElementById("item-description").value;
    const output = document.getElementById("db-output");

    try {
        const response = await fetch(`/api/items/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, description })
        });
        const result = await response.json();
        output.textContent = JSON.stringify(result, null, 2);
    } catch (error) {
        output.textContent = "Error: " + error.message;
    }
}

async function deleteItem() {
    const id = document.getElementById("item-id").value;
    const output = document.getElementById("db-output");

    try {
        const response = await fetch(`/api/items/${id}`, {
            method: "DELETE"
        });
        const result = await response.json();
        output.textContent = JSON.stringify(result, null, 2);
    } catch (error) {
        output.textContent = "Error: " + error.message;
    }
}
