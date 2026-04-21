const API = "";
let token = localStorage.getItem("cybernews_token");
let currentUser = null;

function showSection(name) {
  document
    .querySelectorAll("section")
    .forEach((s) => (s.style.display = "none"));
  const el = document.getElementById(name + "-section");
  if (el) el.style.display = "block";

  document
    .querySelectorAll(".nav-link")
    .forEach((b) => b.classList.remove("active"));
  const btn = document.querySelector(`[data-nav="${name}"]`);
  if (btn) btn.classList.add("active");

  localStorage.setItem("current_section", name);

  if (name === "dashboard") {
    restoreTab();
  }
}

function showTab(name) {
  document
    .querySelectorAll(".dash-tab")
    .forEach((t) => (t.style.display = "none"));
  document
    .querySelectorAll(".tab-btn")
    .forEach((b) => b.classList.remove("active"));

  const tab = document.getElementById(name + "-tab");
  if (tab) tab.style.display = "block";

  const btn = document.querySelector(`[data-tab="${name}"]`);
  if (btn) btn.classList.add("active");

  localStorage.setItem("current_tab", name);
}

function restoreTab() {
  const saved = localStorage.getItem("current_tab");
  if (saved) {
    showTab(saved);
  } else {
    showTab("write");
  }
}

/* ─── Auth State ─── */

function updateAuthUI() {
  const loggedIn = !!token;
  document.getElementById("nav-signup").style.display = loggedIn ? "none" : "";
  document.getElementById("nav-login").style.display = loggedIn ? "none" : "";
  document.getElementById("nav-dashboard").style.display = loggedIn
    ? ""
    : "none";
  document.getElementById("nav-logout").style.display = loggedIn ? "" : "none";

  if (loggedIn) {
    loadUserInfo();
    loadMyPosts();
    loadFollowing();
  }

  const saved = localStorage.getItem("current_section");
  if (loggedIn) {
    if (saved === "login" || saved === "signup") {
      showSection("dashboard");
    } else if (saved) {
      showSection(saved);
    } else {
      showSection("dashboard");
    }
  } else {
    if (saved === "dashboard") {
      showSection("login");
    } else if (saved) {
      showSection(saved);
    } else {
      showSection("home");
    }
  }
}

function logout() {
  token = null;
  currentUser = null;
  localStorage.removeItem("cybernews_token");
  localStorage.removeItem("current_section");
  localStorage.removeItem("current_tab");
  updateAuthUI();
}

function showResult(id, message, type) {
  const box = document.getElementById(id);
  box.className = "result-box show " + type;
  if (typeof message === "object") {
    box.innerHTML = `<pre>${JSON.stringify(message, null, 2)}</pre>`;
  } else {
    box.textContent = message;
  }
}

function clearResult(id) {
  const box = document.getElementById(id);
  box.className = "result-box";
  box.textContent = "";
}

async function api(method, path, body, useFormData) {
  const opts = { method, headers: {} };
  if (token) opts.headers["Authorization"] = "Bearer " + token;

  if (body) {
    if (useFormData) {
      const fd = new URLSearchParams();
      for (const [k, v] of Object.entries(body)) fd.append(k, v);
      opts.body = fd;
      opts.headers["Content-Type"] = "application/x-www-form-urlencoded";
    } else {
      opts.body = JSON.stringify(body);
      opts.headers["Content-Type"] = "application/json";
    }
  }

  const res = await fetch(API + path, opts);
  const text = await res.text();
  let data;
  try {
    data = JSON.parse(text);
  } catch {
    data = text;
  }
  if (!res.ok) throw new Error(data?.detail || data || res.statusText);
  return data;
}

async function handleSignup(e) {
  e.preventDefault();
  clearResult("signup-result");
  const username = document.getElementById("signup-username").value;
  const password = document.getElementById("signup-password").value;
  const email = document.getElementById("signup-email").value || null;
  const body = { username, password };
  if (email) body.email = email;
  try {
    const userId = await api("POST", "/signup", body);
    showResult(
      "signup-result",
      `✦ CHARACTER CREATED!\nID: ${JSON.stringify(userId)}`,
      "success",
    );
    document.getElementById("signup-form").reset();
  } catch (err) {
    showResult("signup-result", "✖ " + err.message, "error");
  }
}

async function handleLogin(e) {
  e.preventDefault();
  clearResult("login-result");
  const username = document.getElementById("login-username").value;
  const password = document.getElementById("login-password").value;
  try {
    const data = await api("POST", "/token", { username, password }, true);
    token = data.access_token;
    localStorage.setItem("cybernews_token", token);
    showResult("login-result", "✦ WELCOME BACK, ADVENTURER!", "success");
    document.getElementById("login-form").reset();
    setTimeout(() => updateAuthUI(), 600);
  } catch (err) {
    showResult("login-result", "✖ " + err.message, "error");
  }
}

async function loadUserInfo() {
  try {
    currentUser = await api("GET", "/users");
    document.getElementById("user-info").innerHTML = `
      <div class="user-info-grid">
        <span class="key">NAME</span><span class="val">${currentUser.username}</span>
        <span class="key">EMAIL</span><span class="val">${currentUser.email || "—"}</span>
        <span class="key">RANK</span><span class="val">${currentUser.is_admin ? "★ ADMIN" : "ADVENTURER"}</span>
      </div>
      <div class="user-id-display">▸ ID: ${currentUser.user_id}</div>`;
  } catch (err) {
    document.getElementById("user-info").textContent = "✖ Failed to load";
  }
}

async function loadFollowing() {
  const el = document.getElementById("following-list");
  try {
    const list = await api("GET", "/users/following");
    if (list.length === 0) {
      el.innerHTML = '<div class="no-following">Not following anyone yet</div>';
      return;
    }
    el.innerHTML = list
      .map(
        (u) =>
          `<span class="follow-item">♥ <span class="follow-name">${escapeHtml(u.username)}</span></span>`,
      )
      .join("");
  } catch {
    el.innerHTML = '<div class="no-following">—</div>';
  }
}

async function loadMyPosts() {
  const listEl = document.getElementById("my-posts-list");
  const countBar = document.getElementById("post-count-bar");
  const countLabel = document.getElementById("post-count-label");
  try {
    const posts = await api("GET", "/posts/mine");
    const count = posts ? posts.length : 0;
    if (countLabel) countLabel.textContent = count;
    if (countBar)
      countBar.style.width = Math.min((count / 20) * 100, 100) + "%";
    if (count === 0) {
      listEl.innerHTML =
        '<div class="no-posts">No scrolls written yet...</div>';
      return;
    }
    listEl.innerHTML = posts
      .reverse()
      .map(
        (p) => `
        <div class="post-item">
          <div class="post-item-title">${escapeHtml(p.title)}</div>
          <div class="post-item-content">${escapeHtml(p.content)}</div>
          <div class="post-item-meta">ID: ${p.post_id}</div>
        </div>`,
      )
      .join("");
  } catch (err) {
    console.error("Load Posts Error:", err);
    listEl.innerHTML =
      '<div class="no-posts">Failed to load: ' + err.message + "</div>";
  }
}

function escapeHtml(text) {
  const d = document.createElement("div");
  d.textContent = text;
  return d.innerHTML;
}

async function handleNewPost(e) {
  e.preventDefault();
  clearResult("post-result");
  const title = document.getElementById("post-title").value;
  const content = document.getElementById("post-content").value;
  try {
    await api("POST", "/posts", { title, content });
    showResult("post-result", "✦ SCROLL PUBLISHED!", "success");
    document.getElementById("post-form").reset();
    loadMyPosts();
  } catch (err) {
    showResult("post-result", "✖ " + err.message, "error");
  }
}

async function handleSubscribe(e) {
  e.preventDefault();
  clearResult("subscribe-result");
  const targetUserId = document.getElementById("subscribe-user-id").value;
  try {
    await api("POST", "/subscribe", { target_user_id: targetUserId });
    showResult("subscribe-result", "✦ FOLLOWING!", "success");
    document.getElementById("subscribe-form").reset();
    loadFollowing();
  } catch (err) {
    showResult("subscribe-result", "✖ " + err.message, "error");
  }
}

async function handleImport(e) {
  e.preventDefault();
  clearResult("import-result");
  const url = document.getElementById("import-url").value;
  try {
    const data = await api("POST", "/posts/import", { url });
    showResult(
      "import-result",
      `✦ LOOT IMPORTED!\nTitle: ${data.title}\nPost ID: ${data.post_id}`,
      "success",
    );
    document.getElementById("import-form").reset();
    loadMyPosts();
  } catch (err) {
    showResult("import-result", "✖ " + err.message, "error");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  document
    .getElementById("signup-form")
    .addEventListener("submit", handleSignup);
  document.getElementById("login-form").addEventListener("submit", handleLogin);
  document
    .getElementById("post-form")
    .addEventListener("submit", handleNewPost);
  document
    .getElementById("subscribe-form")
    .addEventListener("submit", handleSubscribe);
  document
    .getElementById("import-form")
    .addEventListener("submit", handleImport);

  function updateClock() {
    const now = new Date();
    const dateStr = now.toLocaleDateString("en-US", {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
    });
    const timeStr = now.toLocaleTimeString("en-US");
    const el = document.getElementById("live-date");
    if (el) el.textContent = `${dateStr} | ${timeStr}`;
  }
  setInterval(updateClock, 1000);
  updateClock();

  updateAuthUI();
});
