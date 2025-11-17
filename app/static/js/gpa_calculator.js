const gpaModalOverlay = document.getElementById('gpa-modal-overlay');
const semesterTab = document.getElementById('gpa-tab-semester');
const courseTab = document.getElementById('gpa-tab-course');
const semesterContent = document.getElementById('gpa-content-semester');
const courseContent = document.getElementById('gpa-content-course');

function openGpaModal() { gpaModalOverlay.classList.remove('hidden'); }
function closeGpaModal() { gpaModalOverlay.classList.add('hidden'); }

function switchGpaTab(tabName) {
    if (tabName === 'semester') {
        semesterTab.classList.add('active');
        courseTab.classList.remove('active');
        semesterContent.classList.add('active');
        courseContent.classList.remove('active');
    } else {
        semesterTab.classList.remove('active');
        courseTab.classList.add('active');
        semesterContent.classList.remove('active');
        courseContent.classList.add('active');
    }
}

// --- Semester GPA Tab ---
const gpaCourseList = document.getElementById('gpa-course-list');
const gradePoints = { 'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0 };

function addGpaCourseRow() {
    const row = document.createElement('div');
    row.classList.add('grid', 'grid-cols-3', 'gap-3', 'items-center');
    row.innerHTML = `
        <input type="text" placeholder="Course (e.g., COSC 111)" class="gpa-input col-span-2">
        <input type="number" placeholder="Credits" class="gpa-input gpa-credits" min="0" max="5" oninput="calculateSemesterGPA()">
        <select class="gpa-select gpa-grade col-span-1" onchange="calculateSemesterGPA()">
            <option value="">Grade</option>
            <option value="A">A</option><option value="B">B</option>
            <option value="C">C</option><option value="D">D</option>
            <option value="F">F</option>
        </select>
    `;
    gpaCourseList.appendChild(row);
}

function calculateSemesterGPA() {
    let totalPoints = 0;
    let totalCredits = 0;
    const creditInputs = gpaCourseList.querySelectorAll('.gpa-credits');
    const gradeSelects = gpaCourseList.querySelectorAll('.gpa-grade');

    for (let i = 0; i < creditInputs.length; i++) {
        const credits = parseFloat(creditInputs[i].value);
        const grade = gradeSelects[i].value;
        if (!isNaN(credits) && credits > 0 && gradePoints[grade] !== undefined) {
            totalPoints += credits * gradePoints[grade];
            totalCredits += credits;
        }
    }

    const gpa = totalCredits === 0 ? 0 : (totalPoints / totalCredits);
    document.getElementById('semester-gpa-result').textContent = gpa.toFixed(2);
}

// --- Course Grade (What-If) Tab ---
const gpaAssignmentList = document.getElementById('gpa-assignment-list');

function addGpaAssignmentRow() {
    const row = document.createElement('div');
    row.classList.add('grid', 'grid-cols-3', 'gap-3', 'items-center');
    row.innerHTML = `
        <input type="text" placeholder="Assignment (e.g., Midterm)" class="gpa-input col-span-1">
        <input type="number" placeholder="Weight (%)" class="gpa-input gpa-weight" min="0" max="100" oninput="calculateCourseGrade()">
        <input type="number" placeholder="Grade (%)" class="gpa-input gpa-score" min="0" oninput="calculateCourseGrade()">
    `;
    gpaAssignmentList.appendChild(row);
}

function calculateCourseGrade() {
    let totalWeight = 0;
    let achievedScore = 0;
    const weightInputs = gpaAssignmentList.querySelectorAll('.gpa-weight');
    const scoreInputs = gpaAssignmentList.querySelectorAll('.gpa-score');

    for (let i = 0; i < weightInputs.length; i++) {
        const weight = parseFloat(weightInputs[i].value);
        const score = parseFloat(scoreInputs[i].value);
        if (!isNaN(weight) && weight > 0 && !isNaN(score)) {
            totalWeight += weight;
            achievedScore += (score * weight / 100);
        }
    }
    
    const currentGrade = totalWeight === 0 ? 0 : (achievedScore / totalWeight * 100);
    document.getElementById('course-weight-result').textContent = totalWeight.toFixed(0) + '%';
    document.getElementById('course-grade-result').textContent = currentGrade.toFixed(1) + '%';
    return { totalWeight, achievedScore };
}

function calculateFinalExam() {
    const { totalWeight, achievedScore } = calculateCourseGrade();
    const finalWeight = parseFloat(document.getElementById('final-exam-weight').value);
    const desiredGrade = parseFloat(document.getElementById('desired-course-grade').value);
    const resultEl = document.getElementById('final-exam-result');

    if (isNaN(finalWeight) || isNaN(desiredGrade)) {
        resultEl.textContent = "Please enter valid numbers.";
        resultEl.className = "mt-3 text-center font-semibold text-red-600";
        return;
    }

    if (totalWeight + finalWeight > 100) {
        resultEl.textContent = `Error: Weights add up to ${totalWeight + finalWeight}%.`;
        resultEl.className = "mt-3 text-center font-semibold text-red-600";
        return;
    }

    const neededScore = (desiredGrade - achievedScore) / (finalWeight / 100);
    
    if (neededScore > 100) {
        resultEl.textContent = `You need a ${neededScore.toFixed(1)}% on the final. It might be time to ask for extra credit!`;
        resultEl.className = "mt-3 text-center font-semibold text-orange-600";
    } else if (neededScore < 0) {
        resultEl.textContent = `You need a ${neededScore.toFixed(1)}%. You've already passed!`;
        resultEl.className = "mt-3 text-center font-semibold text-green-600";
    } else {
        resultEl.textContent = `You need a ${neededScore.toFixed(1)}% on the final to get a ${desiredGrade}%.`;
        resultEl.className = "mt-3 text-center font-semibold text-blue-600";
    }
}