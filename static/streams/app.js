(() => {
  const $ = (selector) => document.querySelector(selector);
  const $$ = (selector) => [...document.querySelectorAll(selector)];
  const sampleCode = $("#code-editor").value;
  const state = { title: "", goal: "", output: "", questions: [], explanations: [] };

  const toast = (message) => {
    const node = $("#toast");
    node.textContent = message;
    node.classList.add("show");
    window.setTimeout(() => node.classList.remove("show"), 2200);
  };

  const api = async (path, payload) => {
    const response = await fetch(path, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRFToken": window.SCISTREAM.csrfToken },
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    if (!response.ok || !data.ok) throw new Error(data.error || "Something went wrong.");
    return data;
  };

  const addTimeline = (label) => {
    const item = document.createElement("li");
    item.innerHTML = `<span></span><div><b></b><small>Just now</small></div>`;
    item.querySelector("b").textContent = label;
    $("#timeline").prepend(item);
  };

  $$('[data-open-setup]').forEach((button) => button.addEventListener("click", () => $("#setup-dialog").showModal()));
  $('[data-close-modal]').addEventListener("click", () => $("#setup-dialog").close());
  $('[data-close-summary]').addEventListener("click", () => $("#summary-dialog").close());

  $("#setup-form").addEventListener("submit", (event) => {
    event.preventDefault();
    const title = $("#session-title").value.trim();
    const goal = $("#session-goal").value.trim();
    if (!title || !goal) {
      $("#setup-error").textContent = "Add both a session title and research question.";
      return;
    }
    state.title = title;
    state.goal = goal;
    $("#room-title").textContent = title;
    $("#room-goal").textContent = goal;
    $("#landing").classList.add("hidden");
    $("#room").classList.remove("hidden");
    $("#setup-dialog").close();
    document.title = `${title} — SciStream`;
    window.scrollTo(0, 0);
    toast("Research room opened");
  });

  $("#leave-room").addEventListener("click", () => {
    $("#room").classList.add("hidden");
    $("#landing").classList.remove("hidden");
    document.title = "SciStream — Live research, documented";
  });

  $("#reset-code").addEventListener("click", () => {
    $("#code-editor").value = sampleCode;
    toast("Sample experiment restored");
  });

  $("#run-code").addEventListener("click", async () => {
    const button = $("#run-code");
    const code = $("#code-editor").value;
    button.disabled = true;
    button.textContent = "Running…";
    try {
      const result = await api("/api/execute/", { code });
      state.output = `${result.stdout}\n\n${result.important_output}`;
      $("#output-empty").classList.add("hidden");
      $("#output-result").classList.remove("hidden");
      $("#stdout").textContent = result.stdout;
      $("#important-output").textContent = result.important_output;
      $("#result-chart").replaceChildren(...result.chart.map((point) => {
        const column = document.createElement("div");
        column.className = "chart-column";
        column.innerHTML = `<i></i><span></span>`;
        column.querySelector("i").style.height = `${point.remaining}%`;
        column.querySelector("span").textContent = `${point.time}h`;
        return column;
      }));
      addTimeline("Code cell executed");
      toast("Experiment complete");
    } catch (error) {
      state.output = `Error: ${error.message}`;
      toast(error.message);
    } finally {
      button.disabled = false;
      button.innerHTML = "<span>▶</span> Run cell";
    }
  });

  $("#chat-form").addEventListener("submit", (event) => {
    event.preventDefault();
    const input = $("#chat-input");
    const question = input.value.trim();
    if (!question) return;
    state.questions.push(question);
    const message = document.createElement("div");
    message.className = "message";
    message.innerHTML = '<div class="avatar green">Y</div><div><p><b>You</b><time>now</time></p><span></span></div>';
    message.querySelector("span").textContent = question;
    $("#chat-messages").append(message);
    $("#chat-messages").scrollTop = $("#chat-messages").scrollHeight;
    input.value = "";
    addTimeline("Participant question received");
  });

  $$('[data-ai-action]').forEach((button) => button.addEventListener("click", async () => {
    const action = button.dataset.aiAction;
    button.disabled = true;
    const original = button.textContent;
    button.textContent = "Thinking…";
    try {
      const result = await api("/api/assistant/", {
        action,
        context: { title: state.title, goal: state.goal, code: $("#code-editor").value, output: state.output, question: state.questions.at(-1) || "" },
      });
      state.explanations.push(result.message);
      $("#ai-mode").textContent = result.mode.toUpperCase();
      const response = document.createElement("div");
      response.className = "ai-response";
      response.textContent = result.message;
      $("#ai-messages").append(response);
      $("#ai-messages").scrollTop = $("#ai-messages").scrollHeight;
      addTimeline("AI explanation added");
    } catch (error) {
      toast(error.message);
    } finally {
      button.disabled = false;
      button.textContent = original;
    }
  }));

  $("#generate-summary").addEventListener("click", async () => {
    const button = $("#generate-summary");
    button.disabled = true;
    button.textContent = "Generating…";
    try {
      const result = await api("/api/summary/", { title: state.title, goal: state.goal, code: $("#code-editor").value, output: state.output || "No code output was captured.", questions: state.questions, explanations: state.explanations });
      $("#summary-text").value = result.markdown;
      $("#summary-dialog").showModal();
      addTimeline("Markdown summary generated");
    } catch (error) {
      toast(error.message);
    } finally {
      button.disabled = false;
      button.textContent = "Generate summary";
    }
  });

  $("#copy-summary").addEventListener("click", async () => {
    await navigator.clipboard.writeText($("#summary-text").value);
    $("#summary-status").textContent = "Copied to clipboard.";
  });

  $("#download-summary").addEventListener("click", () => {
    const blob = new Blob([$("#summary-text").value], { type: "text/markdown" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `${(state.title || "scistream-session").toLowerCase().replace(/[^a-z0-9]+/g, "-")}.md`;
    link.click();
    URL.revokeObjectURL(link.href);
    $("#summary-status").textContent = "Markdown downloaded.";
  });
})();
