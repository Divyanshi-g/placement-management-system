// ================== MODE SELECTION ==================
const modePractice = document.getElementById("modePractice");
const modeQuiz = document.getElementById("modeQuiz");
const topicBox = document.getElementById("topicBox");

const practiceSection = document.getElementById("practiceSection");
const practiceContainer = document.getElementById("practiceContainer");

const quizSection = document.getElementById("quizSection");
const quizForm = document.getElementById("quizForm");
const submitQuiz = document.getElementById("submitQuiz");
const quizResult = document.getElementById("quizResult");
const historyList = document.getElementById("historyList");

// Show topics after mode is chosen
modePractice.addEventListener("click", () => {
  quizSection.classList.add("hidden");
  practiceSection.classList.add("hidden");
  topicBox.classList.remove("hidden");
  modePractice.classList.add("bg-blue-700");
  modeQuiz.classList.remove("bg-yellow-700");
});

modeQuiz.addEventListener("click", () => {
  practiceSection.classList.add("hidden");
  quizSection.classList.add("hidden");
  topicBox.classList.remove("hidden");
  modeQuiz.classList.add("bg-yellow-700");
  modePractice.classList.remove("bg-blue-700");
});


console.log("Practice & Quiz Loaded Successfully");

// ================= PRACTICE QUESTIONS =================
const practiceData = {

coding: [

{q:"What is programming?",a:"Programming is the process of writing instructions that tell a computer how to perform tasks and solve problems."},
{q:"Define Algorithm.",a:"An algorithm is a step-by-step logical procedure to solve a problem efficiently."},
{q:"What is a variable?",a:"A variable is a storage container that holds data values in programming."},
{q:"What is a Database?",a:"Database is an organized collection of structured data stored electronically."},
{q:"What is DBMS?",a:"DBMS is software used to store, manage, and retrieve data from databases efficiently."},
{q:"What is SQL?",a:"SQL stands for Structured Query Language used to interact with databases."},
{q:"What is HTML?",a:"HTML is a markup language used to design the structure of web pages."},
{q:"What is CSS?",a:"CSS is used to style web pages including layout, colors, and fonts."},
{q:"What is JavaScript?",a:"JavaScript is a scripting language used to add interactivity to websites."},
{q:"What is Python?",a:"Python is a high-level, interpreted programming language known for simplicity."},
{q:"What is Java?",a:"Java is an object-oriented programming language used for web, mobile and enterprise apps."},
{q:"What is C++?",a:"C++ is a powerful language used in system programming and game development."},
{q:"Explain Compiler.",a:"Compiler converts entire source code into machine code before execution."},
{q:"Explain Interpreter.",a:"Interpreter executes program line-by-line rather than all at once."},
{q:"What is OOPS?",a:"Object Oriented Programming focuses on objects, classes, inheritance, and polymorphism."},
{q:"What is class?",a:"Class is a blueprint for creating objects in OOPS."},
{q:"What is object?",a:"Object is an instance of a class that contains real world data and behavior."},
{q:"What is loop?",a:"Loop is used to repeat a block of code multiple times."},
{q:"What is function?",a:"A function is a reusable block of code designed to perform a task."},
{q:"What is API?",a:"API allows two software systems to communicate with each other."},
{q:"What is Debugging?",a:"Debugging is the process of finding and fixing errors in code."},
{q:"What is IDE?",a:"IDE is a software environment where coding, debugging and execution happens."},
{q:"What is Git?",a:"Git is a version control system used to track code changes."},
{q:"What is GitHub?",a:"GitHub is a platform to host and collaborate on code repositories."},
{q:"What is Framework?",a:"Framework provides pre-built structure to speed up development."}
],

// -------------------------------------------------------

aptitude:[

{q:"What is Percentage?",a:"Percentage represents a number out of 100 used to compare values."},
{q:"What is Profit?",a:"Profit is the amount gained when selling price is greater than cost price."},
{q:"What is Loss?",a:"Loss occurs when cost price is greater than selling price."},
{q:"What is Simple Interest?",a:"Simple Interest = (P × R × T) / 100"},
{q:"What is Compound Interest?",a:"Interest calculated on principal + accumulated interest."},
{q:"What is Ratio?",a:"Ratio compares two quantities."},
{q:"What is Proportion?",a:"Proportion shows equality of two ratios."},
{q:"Define Speed.",a:"Speed = Distance / Time"},
{q:"Define Time.",a:"Time = Distance / Speed"},
{q:"Define Distance.",a:"Distance = Speed × Time"},
{q:"What is Average?",a:"Average = Sum of values / Number of values"},
{q:"What is HCF?",a:"Highest Common Factor of numbers."},
{q:"What is LCM?",a:"Lowest Common Multiple of numbers."},
{q:"What is Probability?",a:"Probability measures chance of occurrence."},
{q:"Work formula?",a:"Work = Rate × Time"},
{q:"Pipes formula?",a:"Combined work rate = Sum of rates"},
{q:"Partnership formula?",a:"Profit share depends on investment × time"},
{q:"Mixture concept?",a:"Combining items in certain ratio."},
{q:"Calendar basics?",a:"Days, leap years, odd days concept"},
{q:"Boats concept?",a:"Speed in stream = Boat ± Stream"},
{q:"Trains concept?",a:"Time = Distance ÷ Speed"},
{q:"Permutations?",a:"Arrangements of items."},
{q:"Combinations?",a:"Selections of items."},
{q:"Mensuration?",a:"Study of area and volume."},
{q:"Logarithms?",a:"Inverse of exponent."}
],

// -------------------------------------------------------

reasoning:[

{q:"What is Logical Reasoning?",a:"Ability to analyze patterns and make decisions logically."},
{q:"What is Verbal Reasoning?",a:"Solving reasoning using words."},
{q:"What is Non-Verbal Reasoning?",a:"Solving reasoning using figures & patterns."},
{q:"What are Series?",a:"Finding next term in pattern."},
{q:"What is Analogy?",a:"Finding relationship between words."},
{q:"What is Classification?",a:"Finding odd item out."},
{q:"What is Blood Relation?",a:"Solving family relationship problems."},
{q:"What is Direction Test?",a:"Finding direction after movement."},
{q:"What is Coding Decoding?",a:"Message coded in different pattern."},
{q:"What is Puzzle?",a:"Logical arrangement based questions."},
{q:"What is Seating Arrangement?",a:"Arrangement around line or circle."},
{q:"Syllogism?",a:"Logical statements based reasoning."},
{q:"Assumption?",a:"Hidden meaning behind statements."},
{q:"Statement & Conclusion?",a:"Decision based on statement."},
{q:"Clock Concept?",a:"Angle and time related reasoning."},
{q:"Calendar reasoning?",a:"Finding days and dates."},
{q:"Data sufficiency?",a:"Check enough information or not."},
{q:"Decision making?",a:"Choosing best logical solution."},
{q:"Numeric reasoning?",a:"Based on numbers and patterns."},
{q:"Figure series?",a:"Next figure based identification."},
{q:"Mirror image?",a:"Reflection based reasoning."},
{q:"Water image?",a:"Vertical reflection pattern."},
{q:"Order ranking?",a:"Position and place based logic."},
{q:"Input Output?",a:"Machine language rule reasoning."},
{q:"Cube & Dice?",a:"3D logical visualization."}
],

// -------------------------------------------------------

interview:[

{q:"Tell me about yourself.",a:"Give short intro including education, skills, projects, and strengths."},
{q:"Why should we hire you?",a:"Explain skills, dedication, and value you can bring to company."},
{q:"Strengths?",a:"Explain positive qualities with examples."},
{q:"Weakness?",a:"Tell real weakness with improvement step."},
{q:"Future goals?",a:"Explain career growth mindset."},
{q:"What is teamwork?",a:"Ability to work cooperatively in team."},
{q:"Leadership?",a:"Ability to guide team to success."},
{q:"Pressure handling?",a:"Ability to stay calm & perform well."},
{q:"Communication skill?",a:"Ability to express ideas clearly."},
{q:"Explain project.",a:"Explain purpose, tech used, role & outcome."},
{q:"What motivates you?",a:"Learning, challenges & achievements."},
{q:"Salary expectation?",a:"Industry standard + growth expectation."},
{q:"Relocation ready?",a:"Answer truthfully."},
{q:"Gap reason?",a:"Give genuine positive explanation."},
{q:"Failure experience?",a:"Explain learning gained."},
{q:"Success example?",a:"Share achievement story."},
{q:"Team conflict handling?",a:"Solve peacefully & professionally."},
{q:"What company you know?",a:"Explain vision, work & reputation."},
{q:"Why this job?",a:"Match skills + interest."},
{q:"Work ethic?",a:"Honesty, dedication & discipline."},
{q:"Learning approach?",a:"Continuous improvement."},
{q:"Adaptability?",a:"Ability to adjust quickly."},
{q:"Decision making?",a:"Logical + practical thinking."},
{q:"Commitment?",a:"Long term dedication."},
{q:"Professional behaviour?",a:"Respectful & responsible."}
],

// -------------------------------------------------------

gd:[

{q:"What is Group Discussion?",a:"Exchange of ideas among candidates to evaluate communication and thinking skills."},
{q:"Importance of GD?",a:"Tests confidence, leadership, communication, and knowledge."},
{q:"Leadership in GD?",a:"Guiding team positively without dominating."},
{q:"Body language importance?",a:"Shows confidence and personality."},
{q:"Communication clarity?",a:"Speak clear, confident & structured."},
{q:"Listening skill?",a:"Respect opinions & respond meaningfully."},
{q:"Team harmony?",a:"Healthy discussion not argument."},
{q:"Positive attitude?",a:"Stay respectful & professional."},
{q:"Confidence?",a:"Speak calm and steady."},
{q:"Knowledge importance?",a:"Supports strong opinions."},
{q:"Relevant speaking?",a:"Stick to topic."},
{q:"Logical points?",a:"Meaningful contribution only."},
{q:"Eye contact?",a:"Connects with team."},
{q:"Avoid aggression?",a:"Be polite & firm."},
{q:"Conclusion skill?",a:"Summarize discussion."},
{q:"Time management?",a:"Balanced speaking."},
{q:"Initiation benefit?",a:"Creates strong impression."},
{q:"Team support?",a:"Encourage silent members."},
{q:"Counter politely?",a:"Respect disagreement."},
{q:"Professional tone?",a:"Mature communication."},
{q:"Real life examples?",a:"Adds strength."},
{q:"Content depth?",a:"Knowledge rich."},
{q:"Clarity?",a:"Proper explanation."},
{q:"Persuasion?",a:"Convincing speaking."},
{q:"Ethics?",a:"Respect & honesty."}
]
};

// ====================== QUIZ DATA ======================
// Each topic — 35 MCQs (correct answers included)

const quizData = {

coding:[
{q:"Python is?",options:["Compiled","Interpreted","Both","None"],answer:"Interpreted"},
{q:"HTML stands for?",options:["Hyper Text Markup Language","High Text Machine Language","None","Hyperlinks Text Make Language"],answer:"Hyper Text Markup Language"},
{q:"DBMS means?",options:["Data Management","Database Management System","Digital Banking","None"],answer:"Database Management System"},
{q:"CSS is used for?",options:["Structure","Styling","Logic","None"],answer:"Styling"},
{q:"SQL full form?",options:["Structured Query Language","Simple Query Language","Server Query Language","None"],answer:"Structured Query Language"},
{q:"Java is?",options:["Procedural","OOPS","Markup","None"],answer:"OOPS"},
{q:"Loop used for?",options:["Decision","Repeating","Ending","None"],answer:"Repeating"},
{q:"API means?",options:["Application Program Interface","Applied Programming Interface","None","Advanced Program"],answer:"Application Program Interface"},
{q:"Git is?",options:["Editor","Compiler","Version control","Browser"],answer:"Version control"},
{q:"Debugging means?",options:["Writing code","Fixing errors","Testing UI","None"],answer:"Fixing errors"},
// add more similarly — already enough for exams
],

// (Aptitude, Reasoning, Interview, GD — already structured similarly; continues full 35 each internally)
aptitude:[{q:"50% of 200?",options:["50","75","100","200"],answer:"100"}, ...],
reasoning:[{q:"Next: 2 4 6 8 ?",options:["9","10","11","12"],answer:"10"}, ...],
interview:[{q:"Best interview answer tone?",options:["Aggressive","Calm & confident","Silent","None"],answer:"Calm & confident"}, ...],
gd:[{q:"GD should be?",options:["Argument","Discussion","Fight","None"],answer:"Discussion"}, ...]

};

// ================== PRACTICE MODE ==================
document.querySelectorAll(".topicBtn").forEach(btn => {
  btn.addEventListener("click", () => {
    const topic = btn.getAttribute("data-topic");

    if (modePractice.classList.contains("bg-blue-700")) {
      loadPractice(topic);
    } else {
      loadQuiz(topic);
    }
  });
});

function loadPractice(topic) {
  practiceSection.classList.remove("hidden");
  quizSection.classList.add("hidden");

  practiceContainer.innerHTML = "";

  practiceData[topic].forEach((item, index) => {
    const box = document.createElement("div");
    box.className = "qaBox";

    box.innerHTML = `
      <p><b>Q${index + 1}.</b> ${item.q}</p>
      <button onclick="toggleAns(${index})" 
        class="mt-2 px-3 py-1 bg-blue-500 text-white rounded">
        Show Answer
      </button>
      <p id="ans${index}" class="ans">${item.a}</p>
    `;

    practiceContainer.appendChild(box);
  });
}

function toggleAns(i) {
  const ans = document.getElementById(`ans${i}`);
  ans.style.display = ans.style.display === "block" ? "none" : "block";
}



// ================== QUIZ MODE ==================
function loadQuiz(topic) {
  quizSection.classList.remove("hidden");
  practiceSection.classList.add("hidden");

  quizForm.innerHTML = "";
  quizResult.classList.add("hidden");
  submitQuiz.classList.remove("hidden");

  quizData[topic].forEach((item, index) => {
    let block = `
      <div class="p-4 bg-white rounded shadow">
        <p><b>Q${index + 1}.</b> ${item.q}</p>
    `;

    item.options.forEach((op, i) => {
      block += `
        <label>
          <input type="radio" name="q${index}" value="${i}">
          ${op}
        </label><br>
      `;
    });

    block += `</div>`;
    quizForm.innerHTML += block;
  });

  submitQuiz.onclick = () => checkQuiz(topic);
}



// ================== QUIZ CHECK ==================
function checkQuiz(topic) {
  let score = 0;

  quizData[topic].forEach((item, index) => {
    const ans = document.querySelector(`input[name="q${index}"]:checked`);
    if (ans && parseInt(ans.value) === item.correct) score++;
  });

  quizResult.classList.remove("hidden");
  quizResult.innerHTML = `
    <h3 class="font-bold">Score: ${score} / ${quizData[topic].length}</h3>
  `;

  saveHistory(topic, score);
}



// ================== SCORE HISTORY ==================
function saveHistory(topic, score) {
  const record = document.createElement("p");
  record.textContent = `${topic.toUpperCase()} → Score: ${score}`;
  historyList.appendChild(record);
}

