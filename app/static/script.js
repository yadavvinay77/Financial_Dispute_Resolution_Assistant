let caseId = "";

async function processInput() {
    try {
        const fileEl = document.getElementById("pdf-file");
        const textEl = document.getElementById("manual-text");

        const file = fileEl?.files[0];
        const text = textEl?.value.trim();

        let res;

        if (file) {
            const form = new FormData();
            form.append("file", file);
            res = await fetch("/api/upload", { method: "POST", body: form });
        } else if (text) {
            res = await fetch("/api/ingest_text", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text })
            });
        } else {
            alert("Upload a PDF or paste text.");
            return;
        }

        if (!res.ok) throw new Error("Ingestion failed");

        const data = await res.json();
        caseId = data.case_id;

        document.getElementById("pdf-viewer").innerText =
            data.extracted_text || "No text extracted.";

        document.getElementById("ingest-status").innerText =
            "✅ Document processed. You may now ask questions.";

        console.log("Ingested:", data);

    } catch (err) {
        console.error(err);
        alert("Document processing failed. Check console.");
    }
}

function askStream() {
    const question = document.getElementById("question-box").value;
    const answerBox = document.getElementById("answer-box");
    const askBtn = document.getElementById("ask-btn");
    const typing = document.getElementById("typing-indicator");

    if (!caseId || !question) {
        alert("Process document first.");
        return;
    }

    answerBox.innerHTML = "";
    if (typing) {
        typing.classList.remove("hidden");
        answerBox.appendChild(typing);
    }

    askBtn.disabled = true;

    const evt = new EventSource(
        `/api/ask_stream?case_id=${caseId}&question=${encodeURIComponent(question)}`
    );

    evt.onmessage = async (e) => {
        // 🔴 HANDLE STREAM COMPLETION
        if (e.data === "[DONE]") {
            evt.close();
            askBtn.disabled = false;

            // 🚀 Trigger structured analysis
            await loadAnalysis(question);
            return;
        }

        // Normal token
        if (typing) typing.remove();
        answerBox.innerHTML += e.data;
        answerBox.scrollTop = answerBox.scrollHeight;
    };

    evt.onerror = () => {
        evt.close();
        askBtn.disabled = false;
    };
}

async function loadAnalysis(question) {
    try {
        const res = await fetch("/api/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                case_id: caseId,
                question: question
            })
        });

        if (!res.ok) {
            console.error("Structured ask failed");
            return;
        }

        const data = await res.json();

        // Classification
        document.getElementById("llm-class").innerText = data.classification_llm || "-";
        document.getElementById("ml-class").innerText = data.classification_ml || "-";
        document.getElementById("ml-confidence").innerText =
            Math.round((data.ml_confidence || 0) * 100) + "%";
        document.getElementById("severity").innerText =
            Math.round((data.severity || 0) * 100) + "%";

        // Evidence
        const evidenceBox = document.getElementById("evidence-box");
        evidenceBox.innerHTML = "";
        (data.evidence || []).forEach(chunk => {
            const p = document.createElement("p");
            p.innerText = chunk;
            evidenceBox.appendChild(p);
        });

        // Recommendations
        const stepsBox = document.getElementById("steps-box");
        stepsBox.innerHTML = "";
        (data.recommendations || []).forEach(step => {
            const li = document.createElement("li");
            li.innerText = step;
            stepsBox.appendChild(li);
        });

    } catch (err) {
        console.error("loadAnalysis error:", err);
    }
}
