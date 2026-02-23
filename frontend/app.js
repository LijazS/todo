const API = "http://localhost:8000";

async function loadTasks() {
  const res = await fetch(`${API}/tasks`);
  const tasks = await res.json();
  const tbody = document.getElementById("task-body");
  tbody.innerHTML = "";
  tasks.forEach(t => {
    const tr = document.createElement("tr");
    if (t.completed) tr.classList.add("done");
    tr.innerHTML = `
      <td>${t.id}</td>
      <td>${t.title}</td>
      <td>${t.description}</td>
      <td>${t.completed ? "✅" : "❌"}</td>
      <td>
        <button class="btn-done" onclick="toggleDone(${t.id}, ${!t.completed}, '${t.title}', '${t.description}')">
          ${t.completed ? "Undo" : "Done"}
        </button>
        <button class="btn-delete" onclick="deleteTask(${t.id})">Delete</button>
      </td>`;
    tbody.appendChild(tr);
  });
}

async function addTask() {
  const title = document.getElementById("title").value.trim();
  const description = document.getElementById("description").value.trim();
  if (!title) return alert("Title is required");
  await fetch(`${API}/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, description })
  });
  document.getElementById("title").value = "";
  document.getElementById("description").value = "";
  loadTasks();
}

async function toggleDone(id, completed, title, description) {
  await fetch(`${API}/tasks/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, description, completed })
  });
  loadTasks();
}

async function deleteTask(id) {
  await fetch(`${API}/tasks/${id}`, { method: "DELETE" });
  loadTasks();
}

async function checkHealth() {
  try {
    const res = await fetch(`${API}/health`);
    if (res.ok) {
      document.getElementById("api-status").textContent = "🟢 API Connected";
    } else {
      document.getElementById("api-status").textContent = "🔴 API Error";
    }
  } catch {
    document.getElementById("api-status").textContent = "🔴 API Offline";
  }
}

checkHealth();
loadTasks();
