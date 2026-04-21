const API = "http://127.0.0.1:5000";

console.log("script.js loaded successfully");

// =============================
// Helper: Show Message
// =============================
function showMessage(elementId, message, isError = false) {
    const messageDiv = document.getElementById(elementId);
    if (messageDiv) {
        messageDiv.innerText = message;
        messageDiv.style.display = "block";
        messageDiv.className = "message " + (isError ? "error" : "success");

        // Auto-hide success messages after 3 seconds
        if (!isError && elementId !== "login-message") {
            setTimeout(() => {
                messageDiv.style.display = "none";
            }, 3000);
        }
    }
}

// =============================
// Toggle between Login and Register
// =============================
function toggleRegister() {
    const loginSection = document.getElementById("login-section");
    const registerSection = document.getElementById("register-section");
    const loginMessage = document.getElementById("login-message");
    const registerMessage = document.getElementById("register-message");

    if (!loginSection || !registerSection) {
        console.error("Toggle form sections not found");
        alert("❌ Form sections not found. Please refresh the page.");
        return;
    }

    // Hide messages when toggling
    if (loginMessage) loginMessage.style.display = "none";
    if (registerMessage) registerMessage.style.display = "none";

    if (registerSection.style.display === "none") {
        loginSection.style.display = "none";
        registerSection.style.display = "block";
    } else {
        loginSection.style.display = "block";
        registerSection.style.display = "none";
    }
}

// =============================
// Registration
// =============================
function register() {
    const name = document.getElementById("reg-name");
    const email = document.getElementById("reg-email");
    const password = document.getElementById("reg-password");
    const age = document.getElementById("reg-age");
    const gender = document.getElementById("reg-gender");
    const role = document.getElementById("reg-role");
    const message = document.getElementById("register-message");

    // Check if elements exist
    if (!name || !email || !password || !age || !gender || !role || !message) {
        console.error("Registration form elements not found");
        alert("❌ Form elements not found. Please refresh the page.");
        return;
    }

    if (!name.value || !email.value || !password.value || !age.value || !gender.value || !role.value) {
        showMessage("register-message", "⚠️ All fields are required", true);
        return;
    }

    if (password.value.length < 6) {
        showMessage("register-message", "⚠️ Password must be at least 6 characters", true);
        return;
    }

    fetch(API + "/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                name: name.value,
                email: email.value,
                password: password.value,
                age: parseInt(age.value),
                gender: gender.value,
                role: role.value
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.message) {
                showMessage("register-message", "✅ " + data.message, false);
                // Reset form
                name.value = "";
                email.value = "";
                password.value = "";
                age.value = "";
                gender.value = "";
                role.value = "";

                // Switch back to login after 2 seconds
                setTimeout(() => {
                    toggleRegister();
                }, 2000);
            } else {
                showMessage("register-message", "❌ " + (data.error || "Registration failed"), true);
            }
        })
        .catch(err => {
            showMessage("register-message", "❌ Error: " + err.message, true);
            console.error("Registration error:", err);
        });
}

// =============================
// Login
// =============================
function login() {
    const email = document.getElementById("login-email");
    const password = document.getElementById("login-password");
    const loginRole = document.getElementById("login-role");
    const message = document.getElementById("login-message");

    // Check if elements exist
    if (!email || !password || !loginRole || !message) {
        console.error("Login form elements not found");
        alert("❌ Form elements not found. Please refresh the page.");
        return;
    }

    if (!email.value || !password.value) {
        showMessage("login-message", "⚠️ Please enter email and password", true);
        return;
    }

    if (!loginRole.value) {
        showMessage("login-message", "⚠️ Please select your role", true);
        return;
    }

    fetch(API + "/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                email: email.value,
                password: password.value,
                role: loginRole.value
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.role) {
                localStorage.setItem("role", data.role);
                localStorage.setItem("email", email.value);
                localStorage.setItem("name", data.name);
                showMessage("login-message", "✅ Login successful! Redirecting...", false);
                setTimeout(() => {
                    window.location = "dashboard.html";
                }, 1000);
            } else {
                showMessage("login-message", "❌ " + (data.error || "Login failed"), true);
            }
        })
        .catch(err => {
            showMessage("login-message", "❌ Error: " + err.message, true);
            console.error("Login error:", err);
        });
}

// =============================
// Dashboard - Initialize on load
// =============================
let symptomList = [];

window.onload = function() {
    const role = localStorage.getItem("role");
    const email = localStorage.getItem("email");
    const name = localStorage.getItem("name");

    // Set welcome message
    const welcomeDiv = document.getElementById("welcome-msg");
    if (welcomeDiv) {
        const roleEmoji = role === 'patient' ? '👤' : role === 'doctor' ? '👨‍⚕️' : role === 'nurse' ? '👩‍⚕️' : '👋';
        welcomeDiv.innerText = `${roleEmoji} Welcome, ${name} (${role ? role.toUpperCase() : "GUEST"})`;

    }

    if (role === "patient") {
        const patientSection = document.getElementById("patient-section");
        if (patientSection) {
            patientSection.style.display = "block";
            loadSymptoms();
            loadPatientHistory(email);
        }
    }

    if (role === "doctor") {
        const doctorSection = document.getElementById("doctor-section");
        if (doctorSection) {
            doctorSection.style.display = "block";
            loadDoctorPatients();
        }
    }

    if (role === "nurse") {
        const nurseSection = document.getElementById("nurse-section");
        if (nurseSection) {
            nurseSection.style.display = "block";
            loadNursePatients();
        }
    }
}

// =============================
// Load Symptoms
// =============================
function loadSymptoms() {
    fetch(API + "/symptoms")
        .then(res => res.json())
        .then(data => {
            symptomList = data;
            const dropdown = document.getElementById("symptom-dropdown");
            if (!dropdown) return;

            // Clear existing options
            dropdown.innerHTML = '';

            // Add symptom options with checkboxes
            data.forEach((symptom, index) => {
                const div = document.createElement("div");
                div.className = "symptom-option";
                div.innerHTML = `
                    <input type="checkbox" id="symptom-${index}" value="${symptom}" onchange="updateSymptomDisplay()">
                    <label for="symptom-${index}">${symptom}</label>
                `;
                dropdown.appendChild(div);
            });
        })
        .catch(err => console.error("Error loading symptoms:", err));
}

// =============================
// Toggle Symptom Dropdown
// =============================
function toggleSymptomDropdown() {
    const dropdown = document.getElementById("symptom-dropdown");
    if (dropdown) {
        dropdown.classList.toggle("open");
    }
}

// =============================
// Update Symptom Display
// =============================
function updateSymptomDisplay() {
    const checkboxes = document.querySelectorAll("#symptom-dropdown input[type='checkbox']:checked");
    const selectedNames = Array.from(checkboxes).map(cb => cb.value);
    const displayDiv = document.getElementById("selected-symptoms-display");

    if (displayDiv) {
        if (selectedNames.length === 0) {
            displayDiv.innerHTML = "✅ Selected: <strong>None</strong>";
            displayDiv.style.color = "#666";
        } else {
            displayDiv.innerHTML = "✅ Selected: <strong>" + selectedNames.join(", ") + "</strong>";
            displayDiv.style.color = "#333";
        }
    }
}

// =============================
// Predict Disease
// =============================
async function predict() {
    const email = localStorage.getItem("email");
    const age = document.getElementById("patient-age").value;
    const genderSelect = document.getElementById("patient-gender");
    const genderValue = genderSelect.value;
    const resultDiv = document.getElementById("prediction-result");

    // Get selected symptoms from custom dropdown checkboxes
    const symptomCheckboxes = document.querySelectorAll("#symptom-dropdown input[type='checkbox']:checked");
    const selectedSymptoms = Array.from(symptomCheckboxes).map(cb => cb.value);

    // Validation
    if (!age || age < 1 || age > 120) {
        if (resultDiv) {
            resultDiv.className = "result-box error show";
            resultDiv.innerHTML = "⚠️ Please enter a valid age (1-120)";
        }
        return;
    }

    if (genderValue === "") {
        if (resultDiv) {
            resultDiv.className = "result-box error show";
            resultDiv.innerHTML = "⚠️ Please select your gender";
        }
        return;
    }

    if (selectedSymptoms.length === 0) {
        if (resultDiv) {
            resultDiv.className = "result-box error show";
            resultDiv.innerHTML = "⚠️ Please select at least one symptom";
        }
        return;
    }

    // Show loading message
    if (resultDiv) {
        resultDiv.className = "result-box show";
        resultDiv.innerHTML = "🔄 Analyzing symptoms...";
    }

    try {
        const response = await fetch(API + "/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                age: parseInt(age),
                gender: genderValue,
                symptoms: selectedSymptoms
            })
        });

        const result = await response.json();

        if (result.predicted_disease) {
            if (resultDiv) {
                resultDiv.className = "result-box show";
                resultDiv.innerHTML = `
                    <p><strong>Prediction Result:</strong></p>
                    <p style="font-size: 18px; margin: 10px 0;">
                        <strong>${result.predicted_disease}</strong>
                    </p>
                    <p style="font-size: 12px; color: #666;">
                        This is an AI prediction. Please consult with a healthcare professional for medical advice.
                    </p>
                `;
            }

            // Load updated history
            setTimeout(() => {
                loadPatientHistory(email);
            }, 500);
        } else {
            if (resultDiv) {
                resultDiv.className = "result-box error show";
                resultDiv.innerHTML = "❌ " + (result.error || "Could not generate prediction. Please try again.");
            }
        }
    } catch (error) {
        console.error("Prediction error:", error);
        if (resultDiv) {
            resultDiv.className = "result-box error show";
            resultDiv.innerHTML = "❌ Error: " + error.message;
        }
    }
}

// =============================
// Load Patient History
// =============================
function loadPatientHistory(email) {
    // If email not provided, get from localStorage
    if (!email) {
        email = localStorage.getItem("email");
    }

    if (!email) {
        console.error("No email provided to loadPatientHistory");
        return;
    }

    fetch(`${API}/patient_history/${email}`)
        .then(res => res.json())
        .then(data => {
                const historyDiv = document.getElementById("patient-history-container");
                if (!historyDiv) {
                    console.error("patient-history-container not found");
                    return;
                }

                if (data.history && data.history.length > 0) {
                    let html = "<div style='display:flex; justify-content:flex-end; align-items:center; gap:10px; margin-bottom:10px;'>";
                    html += `<button onclick="clearPatientHistory('${email}')" style='background:#dc3545; color:white; border:none; border-radius:6px; padding:8px 12px; cursor:pointer; font-weight:600;'>🗑️ Clear All History</button>`;
                    html += "</div>";
                    html += "<div style='overflow-x:auto;'>";
                    html += "<table border='1' style='width:100%; border-collapse:collapse; margin-top:10px; table-layout:fixed;'>";
                    html += "<colgroup><col style='width:16%;'><col style='width:14%;'><col style='width:20%;'><col style='width:50%;'></colgroup>";
                    html += "<tr style='background-color:#667eea; color:white;'>";
                    html += "<th style='padding:10px; text-align:left;'>📅 Date & Time</th>";
                    html += "<th style='padding:10px; text-align:left;'>🏥 Disease</th>";
                    html += "<th style='padding:10px; text-align:left;'>🤒 Symptoms</th>";
                    html += "<th style='padding:10px; text-align:left;'>📋 Complete Health Report</th>";
                    html += "</tr>";

                    // Reverse to show latest first
                    const sortedHistory = [...data.history].reverse();

                    sortedHistory.forEach((record, index) => {
                                const bgColor = index % 2 === 0 ? "#f9f9f9" : "#fff";

                                // Generate PDF button or pending message
                                let reportContent = "";
                                if (record.timestamp && (record.health_tips || record.nurse_report)) {
                                    reportContent = `<button onclick="downloadPDFReport('${email}', '${record.timestamp}')" style='background:#28a745; color:white; border:none; border-radius:8px; padding:12px 20px; font-size:14px; cursor:pointer; font-weight:bold; transition:all 0.3s; width:100%; text-align:center;' onmouseover="this.style.background='#218838'" onmouseout="this.style.background='#28a745'">📥 Download PDF Report</button>`;
                                } else {
                                    reportContent = "<span style='color:#999; font-style:italic; display:block; padding:10px; text-align:center;'>⏳ Report pending from healthcare team</span>";
                                }

                                html += `<tr style='background-color:${bgColor}; color:#333;'>
                        <td style='padding:10px; color:#333; vertical-align:top; word-break:break-word;'>${record.timestamp || "N/A"}</td>
                        <td style='padding:10px; color:#333; vertical-align:top; word-break:break-word;'>
                            <div style='display:flex; flex-direction:column; align-items:flex-start; gap:8px;'>
                                <strong>${record.disease || "N/A"}</strong>
                                ${record.timestamp ? `<button onclick="deletePatientHistoryRecord('${email}', '${record.timestamp}')" style='background:#ff4d4f; color:white; border:none; border-radius:5px; padding:5px 10px; font-size:12px; cursor:pointer; min-width:78px; text-align:center;'>Remove</button>` : ""}
                            </div>
                        </td>
                        <td style='padding:10px; color:#333; vertical-align:top; word-break:break-word;'>${Array.isArray(record.symptoms) ? record.symptoms.join(", ") : record.symptoms || "None"}</td>
                        <td style='padding:10px; color:#333; text-align:center; vertical-align:middle; word-break:break-word;'>${reportContent}</td>
                    </tr>`;
                });

                html += "</table></div>";
                historyDiv.innerHTML = html;
            } else {
                historyDiv.innerHTML = "<p style='color: #999; padding: 20px;'>📭 No prediction history yet. Make a prediction to get started.</p>";
            }
        })
        .catch(err => {
            console.error("Error loading history:", err);
            const historyDiv = document.getElementById("patient-history-container");
            if (historyDiv) {
                historyDiv.innerHTML = "<p style='color: red; padding: 20px;'>❌ Error loading history. Please try again.</p>";
            }
        });
}

function deletePatientHistoryRecord(email, predictionTimestamp) {
    if (!email || !predictionTimestamp) {
        alert("⚠️ Unable to remove this record.");
        return;
    }

    const confirmed = confirm("Are you sure you want to remove this disease record from your history?");
    if (!confirmed) {
        return;
    }

    fetch(`${API}/patient_history/${email}/record`, {
            method: "DELETE",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prediction_timestamp: predictionTimestamp })
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            alert("✅ Record removed successfully");
            loadPatientHistory(email);
            if (typeof loadDoctorPatients === "function") {
                loadDoctorPatients();
            }
            if (typeof loadNursePatients === "function") {
                loadNursePatients();
            }
        })
        .catch(err => alert("❌ Error removing record: " + err.message));
}

function clearPatientHistory(email) {
    if (!email) {
        alert("⚠️ No patient email found.");
        return;
    }

    const confirmed = confirm("This will remove all your prediction history permanently. Continue?");
    if (!confirmed) {
        return;
    }

    fetch(`${API}/patient_history/${email}/clear`, {
            method: "DELETE"
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            alert("✅ All patient history cleared");
            loadPatientHistory(email);
            if (typeof loadDoctorPatients === "function") {
                loadDoctorPatients();
            }
            if (typeof loadNursePatients === "function") {
                loadNursePatients();
            }
        })
        .catch(err => alert("❌ Error clearing history: " + err.message));
}

// =============================
// Download PDF Report
// =============================
function downloadPDFReport(email, predictionTimestamp) {
    if (!email || !predictionTimestamp) {
        alert("⚠️ Unable to download this report. Missing information.");
        return;
    }

    // Show loading message
    const loadingMsg = document.createElement('div');
    loadingMsg.textContent = '⏳ Generating PDF report...';
    loadingMsg.style.cssText = 'position:fixed; top:50%; left:50%; transform:translate(-50%, -50%); background:#333; color:white; padding:20px 40px; border-radius:8px; z-index:10000; font-weight:bold;';
    document.body.appendChild(loadingMsg);

    fetch(`${API}/generate_pdf_report/${email}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                prediction_timestamp: predictionTimestamp
            })
        })
        .then(res => {
            if (!res.ok) {
                throw new Error(`HTTP error! status: ${res.status}`);
            }
            return res.blob();
        })
        .then(blob => {
            // Create a temporary download link
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `health_report_${email.split('@')[0]}_${predictionTimestamp.replace(/\\s+/g, '_').replace(/:/g, '-')}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            // Remove loading message
            document.body.removeChild(loadingMsg);
            alert("✅ PDF report downloaded successfully!");
        })
        .catch(err => {
            document.body.removeChild(loadingMsg);
            alert("❌ Error downloading PDF: " + err.message);
        });
}

// =============================
// Load Doctor Patients
// =============================
function loadDoctorPatients() {
    fetch(`${API}/doctor/patients`)
        .then(res => res.json())
        .then(data => {
            const patientsDiv = document.getElementById("patients-container");
            if (!patientsDiv) {
                console.error("patients-container not found");
                return;
            }

            if (data.patients && data.patients.length > 0) {
                let html = "<h4 style='color:#333;'>👥 Patient Records</h4>";
                html += "<table border='1' style='width:100%; border-collapse:collapse; margin-top:10px;'>";
                html += "<tr style='background-color:#667eea; color:white;'>";
                html += "<th>👤 Name</th><th>🎂 Age</th><th>📧 Email</th><th>📜 History</th>";
                html += "</tr>";

                data.patients.forEach((patient, index) => {
                    const bgColor = index % 2 === 0 ? "#f9f9f9" : "#fff";
                    const safeEmail = String(patient.email || "").replace(/'/g, "\\'");
                    const safeName = String(patient.name || "Patient").replace(/'/g, "\\'");

                    html += `<tr style='background-color:${bgColor}; color:#333;'>
                        <td style='padding:10px; color:#333;'>${patient.name || "N/A"}</td>
                        <td style='padding:10px; color:#333;'>${patient.age || "N/A"}</td>
                        <td style='padding:10px; color:#333;'>${patient.email || "N/A"}</td>
                        <td style='padding:10px; text-align:center;'>
                            <button class="btn btn-primary" style="padding:6px 10px; font-size:13px;" onclick="showDoctorPatientHistory('${safeEmail}','${safeName}')">🔗 View History</button>
                        </td>
                    </tr>`;
                });

                html += "</table>";
                patientsDiv.innerHTML = html;
            } else {
                patientsDiv.innerHTML = "<p style='color: #999; padding: 20px;'>📭 No patients registered yet</p>";
            }
        })
        .catch(err => {
            console.error("Error loading doctor patients:", err);
            const patientsDiv = document.getElementById("patients-container");
            if (patientsDiv) {
                patientsDiv.innerHTML = "<p style='color: red; padding: 20px;'>❌ Error loading patients. Please try again.</p>";
            }
        });
}

function showDoctorPatientHistory(email, patientName) {
    fetch(`${API}/patient_history/${email}`)
        .then(res => res.json())
        .then(data => {
            const modal = document.getElementById('patient-history-modal');
            const title = document.getElementById('patient-history-modal-title');
            const content = document.getElementById('patient-history-modal-content');

            if (!modal || !title || !content) {
                alert('❌ History modal not found');
                return;
            }

            title.innerHTML = `<span style='color:#222;'>📜 ${patientName} - Prediction History (Doctor)</span>`;

            const history = Array.isArray(data.history) ? [...data.history].reverse() : [];
            if (history.length === 0) {
                content.innerHTML = "<p style='color:#666; padding:10px;'>No prediction history available.</p>";
            } else {
                let html = "<table border='1' style='width:100%; border-collapse:collapse;'>";
                html += "<tr style='background-color:#667eea; color:white;'>";
                html += "<th style='padding:8px;'>Date</th><th style='padding:8px;'>Disease</th><th style='padding:8px;'>Symptoms</th><th style='padding:8px;'>Health Tips</th><th style='padding:8px;'>Appointment</th><th style='padding:8px;'>Action</th>";
                html += "</tr>";

                history.forEach((record, index) => {
                    const bgColor = index % 2 === 0 ? "#f9f9f9" : "#fff";
                    const safeEmail = String(email || "").replace(/'/g, "\\'");
                    const safeTimestamp = String(record.timestamp || "").replace(/'/g, "\\'");
                    const safePatientName = String(patientName || "Patient").replace(/'/g, "\\'");
                    const encodedDisease = encodeURIComponent(record.disease || "N/A");
                    const symptoms = Array.isArray(record.symptoms) ? record.symptoms.join(', ') : (record.symptoms || 'None');

                    html += `<tr style='background-color:${bgColor}; color:#333;'>
                        <td style='padding:8px;'>${record.timestamp || "N/A"}</td>
                        <td style='padding:8px;'><strong>${record.disease || "N/A"}</strong></td>
                        <td style='padding:8px;'>${symptoms}</td>
                        <td style='padding:8px;'>${record.health_tips || "Pending"}</td>
                        <td style='padding:8px;'>${record.appointment_date || "Not scheduled"}</td>
                        <td style='padding:8px; text-align:center;'>
                            <div style='display:flex; justify-content:center; align-items:center; gap:6px; flex-wrap:wrap;'>
                                <button class="btn btn-primary" style="padding:5px 8px; font-size:12px; min-width:82px;" onclick="showAddTipsFormFromHistory('${safeEmail}','${encodedDisease}','${safeTimestamp}')">➕ Add Tips</button>
                                <button class="btn" style="padding:5px 8px; font-size:12px; min-width:82px; background:#ff4d4f; color:white;" onclick="deleteDoctorHistoryRecord('${safeEmail}','${safeTimestamp}','${safePatientName}')">🗑️ Remove</button>
                            </div>
                        </td>
                    </tr>`;
                });

                html += "</table>";
                content.innerHTML = html;
            }

            modal.classList.add('show');
            modal.style.display = 'flex';
        })
        .catch(err => {
            console.error('Error loading patient history for doctor:', err);
            alert('❌ Failed to load patient history');
        });
}

function deleteDoctorHistoryRecord(email, predictionTimestamp, patientName) {
    if (!email || !predictionTimestamp) {
        alert("⚠️ Unable to remove this record.");
        return;
    }

    const confirmed = confirm("Are you sure you want to remove this disease record from patient history?");
    if (!confirmed) {
        return;
    }

    fetch(`${API}/patient_history/${email}/record`, {
            method: "DELETE",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prediction_timestamp: predictionTimestamp })
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }

            alert("✅ Record removed successfully");
            showDoctorPatientHistory(email, patientName || "Patient");
            if (typeof loadDoctorPatients === "function") {
                loadDoctorPatients();
            }
            if (typeof loadNursePatients === "function") {
                loadNursePatients();
            }
        })
        .catch(err => alert("❌ Error removing record: " + err.message));
}

function closePatientHistoryModal() {
    const modal = document.getElementById('patient-history-modal');
    if (modal) {
        modal.classList.remove('show');
        modal.style.display = 'none';
    }
}

// =============================
// Add Health Tips Form
// =============================
let currentDiseaseForTips = '';
let currentPredictionTimestampForTips = '';

function showAddTipsForm(email, disease) {
    currentDiseaseForTips = disease; // Store for auto-generate
    currentPredictionTimestampForTips = '';
    document.getElementById('tips-modal-email').value = email;
    document.getElementById('tips-modal-disease').value = disease;
    document.getElementById('tips-modal-tips').value = '';
    document.getElementById('tips-modal-appointment').value = '';
    const modal = document.getElementById('tips-modal');
    if (modal) {
        modal.classList.add('show');
        modal.style.display = 'flex';
    }
}

function showAddTipsFormFromHistory(email, encodedDisease, predictionTimestamp) {
    const disease = decodeURIComponent(encodedDisease || 'N/A');
    closePatientHistoryModal();
    currentPredictionTimestampForTips = predictionTimestamp || '';
    showAddTipsForm(email, disease);
    currentPredictionTimestampForTips = predictionTimestamp || '';
}

function autoGenerateHealthTips() {
    const disease = currentDiseaseForTips;

    // Better debugging
    console.log('Auto-generate clicked! Disease:', disease);

    if (!disease || disease === 'N/A' || disease.trim() === '') {
        alert('⚠️ No disease information available for auto-generation');
        return;
    }

    // Show loading state
    const tipsTextarea = document.getElementById('tips-modal-tips');
    if (!tipsTextarea) {
        alert('❌ Error: Tips textarea not found');
        return;
    }

    tipsTextarea.value = '⏳ Loading health recommendations...';
    tipsTextarea.disabled = true;

    const apiUrl = `${API}/health_recommendations/formatted/${encodeURIComponent(disease)}`;
    console.log('Fetching from:', apiUrl);

    // Fetch auto-generated health tips
    fetch(apiUrl)
        .then(res => {
            console.log('Response status:', res.status);
            if (!res.ok) {
                throw new Error(`HTTP error! status: ${res.status}`);
            }
            return res.json();
        })
        .then(data => {
            console.log('Received data:', data);
            if (data.health_tips) {
                tipsTextarea.value = data.health_tips;
                tipsTextarea.disabled = false;
                // Show success only for actual recommendations, not fallback
                if (!data.health_tips.includes('No specific recommendations found')) {
                    alert('✅ Health recommendations generated successfully!');
                } else {
                    alert('ℹ️ Disease not in database. General health tips provided.');
                }
            } else {
                throw new Error('No recommendations found in response');
            }
        })
        .catch(err => {
            console.error('Error fetching health tips:', err);
            // Provide fallback general tips
            tipsTextarea.value = `📋 General Health Tips for ${disease}:\n\n• Follow all prescribed medications as directed\n• Maintain a balanced and nutritious diet\n• Get adequate rest and sleep (7-8 hours per night)\n• Stay well hydrated (drink 8-10 glasses of water daily)\n• Exercise regularly as advised by your healthcare provider\n• Monitor your symptoms and keep a health diary\n• Attend all follow-up appointments without fail\n• Avoid self-medication\n• Report any unusual symptoms immediately\n• Maintain good hygiene practices\n\nℹ️ Please note: These are general recommendations. Consult with a healthcare provider for disease-specific treatment plans.`;
            tipsTextarea.disabled = false;
            alert(`ℹ️ Generated general health tips for "${disease}". You can customize as needed.`);
        });
}

function closeTipsModal() {
    const modal = document.getElementById('tips-modal');
    if (modal) {
        modal.classList.remove('show');
        modal.style.display = 'none';
    }
}

function submitTipsForm() {
    const email = document.getElementById('tips-modal-email').value;
    const disease = document.getElementById('tips-modal-disease').value;
    const doctorName = document.getElementById('tips-modal-doctor-name').value.trim();
    const tips = document.getElementById('tips-modal-tips').value.trim();
    const appointment = document.getElementById('tips-modal-appointment').value.trim();

    if (!doctorName) {
        alert('⚠️ Please enter doctor name');
        return;
    }
    if (!tips) {
        alert('⚠️ Please enter health tips');
        return;
    }
    if (!appointment) {
        alert('⚠️ Please enter appointment date');
        return;
    }

    addHealthTips(email, disease, tips, appointment, currentPredictionTimestampForTips, doctorName);
    closeTipsModal();
}

function addHealthTips(email, disease, tips, appointment, predictionTimestamp = '', doctorName = '') {
    fetch(`${API}/doctor/add_health_tips`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                patient_email: email,
                health_tips: tips,
                appointment_date: appointment,
                prediction_timestamp: predictionTimestamp,
                doctor_name: doctorName
            })
        })
        .then(res => res.json())
        .then(data => {
            alert("✅ " + (data.message || "Health tips added!"));
            loadDoctorPatients();
        })
        .catch(err => alert("❌ Error: " + err.message));
}

// =============================
// Load Nurse Patients
// =============================
function loadNursePatients() {
    fetch(`${API}/nurse/patients`)
        .then(res => res.json())
        .then(data => {
            const patientsDiv = document.getElementById("patient-tracking-container");
            if (!patientsDiv) {
                console.error("patient-tracking-container not found");
                return;
            }

            if (data.patients && data.patients.length > 0) {
                let html = "<table border='1' style='width:100%; border-collapse:collapse; margin-top:10px;'>";
                html += "<tr style='background-color:#667eea; color:white;'>";
                html += "<th>👤 Name</th><th>🎂 Age</th><th>⚧️ Gender</th><th>📧 Email</th><th>📜 History</th><th>🗑️ Actions</th>";
                html += "</tr>";

                data.patients.forEach((patient, index) => {
                    const bgColor = index % 2 === 0 ? "#f9f9f9" : "#fff";
                    const safeEmail = String(patient.email || "").replace(/'/g, "\\'");
                    const safeName = String(patient.name || "Patient").replace(/'/g, "\\'");
                    const safeGender = String(patient.gender || "").replace(/'/g, "\\'");

                    html += `<tr style='background-color:${bgColor}; color:#333;'>
                        <td style='padding:10px; color:#333;'>${patient.name || "N/A"}</td>
                        <td style='padding:10px; color:#333;'>${patient.age || "N/A"}</td>
                        <td style='padding:10px; color:#333;'>${patient.gender || "N/A"}</td>
                        <td style='padding:10px; color:#333;'>${patient.email || "N/A"}</td>
                        <td style='padding:10px; text-align:center;'>
                            <button class="btn btn-primary" style="padding:6px 10px; font-size:13px;" onclick="showNursePatientHistory('${safeEmail}','${safeName}','${safeGender}')">🔗 View History</button>
                        </td>
                        <td style='padding:10px; text-align:center;'>
                            <button class="btn" style="padding:6px 10px; font-size:13px; background:#dc3545; color:white; border:none; border-radius:5px; cursor:pointer;" onclick="removePatientFromNurseView('${safeEmail}', '${safeName}')">🗑️ Remove</button>
                        </td>
                    </tr>`;
                });
                html += "</table>";
                patientsDiv.innerHTML = html;
            } else {
                patientsDiv.innerHTML = "<p style='color: #999; padding: 20px;'>📭 No patients to track</p>";
            }
        })
        .catch(err => {
            console.error("Error loading nurse patients:", err);
            const patientsDiv = document.getElementById("patient-tracking-container");
            if (patientsDiv) {
                patientsDiv.innerHTML = "<p style='color: red; padding: 20px;'>❌ Error loading patients. Please try again.</p>";
            }
        });
}

function showNursePatientHistory(email, patientName, patientGender = 'N/A') {
    fetch(`${API}/patient_history/${email}`)
        .then(res => res.json())
        .then(data => {
            const modal = document.getElementById('patient-history-modal');
            const title = document.getElementById('patient-history-modal-title');
            const content = document.getElementById('patient-history-modal-content');

            if (!modal || !title || !content) {
                alert('❌ History modal not found');
                return;
            }

            title.innerHTML = `<span style='color:#222;'>📜 ${patientName} - Prediction History (Nurse)</span>`;

            const history = Array.isArray(data.history) ? [...data.history].reverse() : [];
            if (history.length === 0) {
                content.innerHTML = "<p style='color:#666; padding:10px;'>No prediction history available.</p>";
            } else {
                let html = "<table border='1' style='width:100%; border-collapse:collapse;'>";
                html += "<tr style='background-color:#667eea; color:white;'>";
                html += "<th style='padding:8px;'>Date</th><th style='padding:8px;'>⚧️ Gender</th><th style='padding:8px;'>Disease</th><th style='padding:8px;'>Symptoms</th><th style='padding:8px;'>Nurse Report</th><th style='padding:8px;'>Action</th>";
                html += "</tr>";

                history.forEach((record, index) => {
                    const bgColor = index % 2 === 0 ? "#f9f9f9" : "#fff";
                    const safeEmail = String(email || "").replace(/'/g, "\\'");
                    const safeTimestamp = String(record.timestamp || "").replace(/'/g, "\\'");
                    const symptoms = Array.isArray(record.symptoms) ? record.symptoms.join(', ') : (record.symptoms || 'None');

                    // Check if report exists for PDF download
                    let nurseReportContent = "";
                    if (record.nurse_report && record.nurse_report.trim() !== "") {
                        nurseReportContent = `<button onclick="downloadPDFReport('${safeEmail}', '${safeTimestamp}')" style='background:#28a745; color:white; border:none; border-radius:5px; padding:6px 12px; font-size:12px; cursor:pointer; font-weight:bold;'>📥 Download Report</button>`;
                    } else {
                        nurseReportContent = "<span style='color:#999; font-style:italic;'>No report generated</span>";
                    }

                    html += `<tr style='background-color:${bgColor}; color:#333;'>
                        <td style='padding:8px;'>${record.timestamp || "N/A"}</td>
                        <td style='padding:8px;'>${patientGender}</td>
                        <td style='padding:8px;'><strong>${record.disease || "N/A"}</strong></td>
                        <td style='padding:8px;'>${symptoms}</td>
                        <td style='padding:8px; text-align:center;'>${nurseReportContent}</td>
                        <td style='padding:8px; text-align:center;'>
                            <button class="btn btn-primary" style="padding:5px 8px; font-size:12px;" onclick="showGenerateReportForm('${safeEmail}','${safeTimestamp}','${record.disease}')">➕ Report</button>
                        </td>
                    </tr>`;
                });

                html += "</table>";
                content.innerHTML = html;
            }

            modal.classList.add('show');
            modal.style.display = 'flex';
        })
        .catch(err => {
            console.error('Error loading patient history for nurse:', err);
            alert('❌ Failed to load patient history');
        });
}

// =============================
// Remove Patient from Nurse View
// =============================
function removePatientFromNurseView(email, patientName) {
    if (!email) {
        alert("⚠️ No patient email found.");
        return;
    }

    const confirmed = confirm(`Are you sure you want to completely remove ${patientName} from the system?\n\nThis will permanently delete:\n• The patient account\n• All prediction history\n• All health and nurse reports\n\nThis action cannot be undone!`);
    if (!confirmed) {
        return;
    }
    // Show loading indicator
    const loadingMsg = document.createElement('div');
    loadingMsg.textContent = '⏳ Removing patient from system...';
    loadingMsg.style.cssText = 'position:fixed; top:50%; left:50%; transform:translate(-50%, -50%); background:#333; color:white; padding:20px 40px; border-radius:8px; z-index:10000; font-weight:bold;';
    document.body.appendChild(loadingMsg);
    fetch(`${API}/remove_patient/${email}`, {
        method: "DELETE"
    })
    .then(res => res.json())
    .then(data => {
        document.body.removeChild(loadingMsg);
        if (data.error) {
            throw new Error(data.error);
        }
        alert(`✅ ${patientName} has been completely removed from the system.`);
        loadNursePatients();
    })
    .catch(err => {
        if (document.body.contains(loadingMsg)) {
            document.body.removeChild(loadingMsg);
        }
        alert("❌ Error removing patient: " + err.message);
    });
}

// =============================
// Generate Nurse Report Form
// =============================
let currentPredictionTimestampForReport = '';
let currentReportDisease = '';

function showGenerateReportForm(email, predictionTimestamp = '', disease = '') {
    closePatientHistoryModal();
    currentPredictionTimestampForReport = predictionTimestamp;
    currentReportDisease = disease;
    document.getElementById('report-modal-email').value = email;
    document.getElementById('report-modal-disease').value = disease || 'Loading...';
    document.getElementById('report-modal-content').value = '';

    // Clear vital signs fields
    document.getElementById('vital-bp').value = '';
    document.getElementById('vital-temp').value = '';
    document.getElementById('vital-hr').value = '';
    document.getElementById('vital-rr').value = '';
    document.getElementById('vital-condition').value = '';
    document.getElementById('vital-followup').value = '';

    const modal = document.getElementById('report-modal');
    if (modal) {
        modal.classList.add('show');
        modal.style.display = 'flex';
    }
}

function closeReportModal() {
    const modal = document.getElementById('report-modal');
    if (modal) {
        modal.classList.remove('show');
        modal.style.display = 'none';
    }
}

function autoGenerateNurseReport() {
    console.log('autoGenerateNurseReport called');
    const disease = currentReportDisease;
    console.log('Auto-generating report for disease:', disease);

    if (!disease) {
        alert('⚠️ No disease information available');
        return;
    }

    // Check if vital signs are filled (optional but recommended)
    const vitalBPElement = document.getElementById('vital-bp');
    const vitalTempElement = document.getElementById('vital-temp');
    const vitalHRElement = document.getElementById('vital-hr');
    const vitalRRElement = document.getElementById('vital-rr');

    const vitalBP = vitalBPElement ? vitalBPElement.value : '';
    const vitalTemp = vitalTempElement ? vitalTempElement.value : '';
    const vitalHR = vitalHRElement ? vitalHRElement.value : '';
    const vitalRR = vitalRRElement ? vitalRRElement.value : '';

    if (!vitalBP && !vitalTemp && !vitalHR && !vitalRR) {
        const proceed = confirm('⚠️ Vital signs are not filled. The report will have "Not recorded" for vital signs.\n\nDo you want to continue anyway?');
        if (!proceed) {
            return;
        }
    }

    // Use raw endpoint to get structured data and format as clinical report
    const url = `${API}/health_recommendations/${encodeURIComponent(disease)}`;
    console.log('Fetching from URL:', url);

    fetch(url)
        .then(res => {
            console.log('Response status:', res.status);
            if (!res.ok) {
                throw new Error(`HTTP error! status: ${res.status}`);
            }
            return res.json();
        })
        .then(data => {
            console.log('Received data:', data);
            const textarea = document.getElementById('report-modal-content');

            if (!textarea) {
                alert('❌ Report textarea not found');
                return;
            }

            // Format as comprehensive clinical report
            let clinicalReport = `=== COMPREHENSIVE CLINICAL REPORT FOR ${disease.toUpperCase()} ===\n\n`;
            clinicalReport += `Report Date: ${new Date().toLocaleDateString()}\n`;
            clinicalReport += `Generated by: Nursing Staff\n\n`;

            if (data.found) {
                // Disease Overview
                if (data.description) {
                    clinicalReport += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
                    clinicalReport += `📋 CLINICAL OVERVIEW\n`;
                    clinicalReport += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
                    clinicalReport += `${data.description}\n\n`;
                }

                // Prescribed Medications
                if (data.medications && data.medications.length > 0) {
                    clinicalReport += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
                    clinicalReport += `💊 PRESCRIBED MEDICATIONS & TREATMENT\n`;
                    clinicalReport += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
                    clinicalReport += `The following medications have been recommended for treatment:\n\n`;
                    data.medications.forEach((med, index) => {
                        clinicalReport += `   ${index + 1}. ${med}\n`;
                    });
                    clinicalReport += `\n⚠️ Note: Take all medications as prescribed by your doctor.\n\n`;
                }

                // Dietary Guidelines
                if (data.diet && data.diet.length > 0) {
                    clinicalReport += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
                    clinicalReport += `🥗 NUTRITIONAL GUIDELINES\n`;
                    clinicalReport += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
                    clinicalReport += `Follow these dietary recommendations:\n\n`;
                    data.diet.forEach((item, index) => {
                        clinicalReport += `   ${index + 1}. ${item}\n`;
                    });
                    clinicalReport += `\n`;
                }

                // Safety Precautions
                if (data.precautions && data.precautions.length > 0) {
                    clinicalReport += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
                    clinicalReport += `⚠️ SAFETY PRECAUTIONS & CARE INSTRUCTIONS\n`;
                    clinicalReport += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
                    clinicalReport += `Important precautions to follow:\n\n`;
                    data.precautions.forEach((item, index) => {
                        clinicalReport += `   ${index + 1}. ${item}\n`;
                    });
                    clinicalReport += `\n`;
                }

                // Exercise & Physical Activity
                if (data.workouts && data.workouts.length > 0) {
                    clinicalReport += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
                    clinicalReport += `💪 EXERCISE & PHYSICAL ACTIVITY PLAN\n`;
                    clinicalReport += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
                    clinicalReport += `Recommended physical activities:\n\n`;
                    data.workouts.forEach((item, index) => {
                        clinicalReport += `   ${index + 1}. ${item}\n`;
                    });
                    clinicalReport += `\n`;
                }

                // Get vital signs from input fields
                const vitalBPEl = document.getElementById('vital-bp');
                const vitalTempEl = document.getElementById('vital-temp');
                const vitalHREl = document.getElementById('vital-hr');
                const vitalRREl = document.getElementById('vital-rr');
                const vitalConditionEl = document.getElementById('vital-condition');
                const vitalFollowupEl = document.getElementById('vital-followup');

                const vitalBP = (vitalBPEl && vitalBPEl.value) || 'Not recorded';
                const vitalTemp = (vitalTempEl && vitalTempEl.value) || 'Not recorded';
                const vitalHR = (vitalHREl && vitalHREl.value) || 'Not recorded';
                const vitalRR = (vitalRREl && vitalRREl.value) || 'Not recorded';
                const vitalCondition = (vitalConditionEl && vitalConditionEl.value) || 'No observations recorded';
                const vitalFollowup = (vitalFollowupEl && vitalFollowupEl.value) || 'No specific recommendations at this time';

                clinicalReport += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
                clinicalReport += `📝 NURSING OBSERVATIONS\n`;
                clinicalReport += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
                clinicalReport += `\nVital Signs:\n`;
                clinicalReport += `• Blood Pressure: ${vitalBP}\n`;
                clinicalReport += `• Temperature: ${vitalTemp}\n`;
                clinicalReport += `• Heart Rate: ${vitalHR}\n`;
                clinicalReport += `• Respiratory Rate: ${vitalRR}\n\n`;
                clinicalReport += `Patient Condition & Response to Treatment:\n`;
                clinicalReport += `${vitalCondition}\n\n`;
                clinicalReport += `Follow-up Recommendations:\n`;
                clinicalReport += `${vitalFollowup}\n\n`;

                clinicalReport += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
                clinicalReport += `⚕️ This report should be reviewed with the patient and physician.\n`;
                clinicalReport += `All treatment plans must be followed as prescribed.\n`;

            } else {
                clinicalReport += `No specific clinical data available in database for "${disease}".\n\n`;

                const vitalBPEl = document.getElementById('vital-bp');
                const vitalTempEl = document.getElementById('vital-temp');
                const vitalHREl = document.getElementById('vital-hr');
                const vitalRREl = document.getElementById('vital-rr');
                const vitalConditionEl = document.getElementById('vital-condition');
                const vitalFollowupEl = document.getElementById('vital-followup');

                const vitalBP = (vitalBPEl && vitalBPEl.value) || 'Not recorded';
                const vitalTemp = (vitalTempEl && vitalTempEl.value) || 'Not recorded';
                const vitalHR = (vitalHREl && vitalHREl.value) || 'Not recorded';
                const vitalRR = (vitalRREl && vitalRREl.value) || 'Not recorded';
                const vitalCondition = (vitalConditionEl && vitalConditionEl.value) || 'No observations recorded';
                const vitalFollowup = (vitalFollowupEl && vitalFollowupEl.value) || 'No specific recommendations at this time';

                clinicalReport += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
                clinicalReport += `📝 NURSING OBSERVATIONS\n`;
                clinicalReport += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
                clinicalReport += `\nVital Signs:\n`;
                clinicalReport += `• Blood Pressure: ${vitalBP}\n`;
                clinicalReport += `• Temperature: ${vitalTemp}\n`;
                clinicalReport += `• Heart Rate: ${vitalHR}\n`;
                clinicalReport += `• Respiratory Rate: ${vitalRR}\n\n`;
                clinicalReport += `Patient Condition & Response to Treatment:\n`;
                clinicalReport += `${vitalCondition}\n\n`;
                clinicalReport += `Follow-up Recommendations:\n`;
                clinicalReport += `${vitalFollowup}\n\n`;

                clinicalReport += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
                clinicalReport += `⚕️ This report should be reviewed with the patient and physician.\n`;
                clinicalReport += `All treatment plans must be followed as prescribed.\n`;
            }

            textarea.value = clinicalReport;
            console.log('Clinical report generated successfully');
        })
        .catch(err => {
            console.error('Error generating report:', err);
            alert('❌ Error: ' + err.message);
        });
}

function submitReportForm() {
    const email = document.getElementById('report-modal-email').value;
    const nurseName = document.getElementById('report-modal-nurse-name').value.trim();
    const report = document.getElementById('report-modal-content').value.trim();

    if (!nurseName) {
        alert('⚠️ Please enter nurse name');
        return;
    }
    if (!report) {
        alert('⚠️ Please enter a report');
        return;
    }

    generateNurseReport(email, report, currentPredictionTimestampForReport, nurseName);
    closeReportModal();
}

function generateNurseReport(email, report, predictionTimestamp = '', nurseName = '') {
    fetch(`${API}/nurse/generate_report`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                patient_email: email,
                report_text: report,
                prediction_timestamp: predictionTimestamp,
                nurse_name: nurseName
            })
        })
        .then(res => res.json())
        .then(data => {
            alert("✅ " + (data.message || "Report generated!"));
            loadNursePatients();
        })
        .catch(err => alert("❌ Error: " + err.message));
}

// =============================
// Logout
// =============================
function logout() {
    localStorage.clear();
    window.location = "index.html";
}