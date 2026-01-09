"use strict";

// =================================================================================
// PRACTICE DATA (25 QUESTIONS EACH TOPIC)
// =================================================================================
const practiceData = {
coding: [
{q:"What is HTML?",a:"HTML structures webpages.",e:"HTML stands for HyperText Markup Language.\nIt defines elements of a webpage.\nUsed to create the skeleton of websites.\nWithout HTML, webpages cannot exist."},
{q:"What is CSS?",a:"CSS styles webpages.",e:"CSS means Cascading Style Sheets.\nControls colors, layout, spacing.\nMakes websites beautiful and user-friendly."},
{q:"What is JavaScript?",a:"JavaScript adds interactivity.",e:"JS runs in browser and server.\nUsed for validation, actions, animations.\nMakes sites dynamic."},
{q:"What is Python?",a:"High level interpreted language.",e:"Readable syntax.\nUsed for AI, ML, data science.\nPowerful libraries and community."},
{q:"What is Java?",a:"Object Oriented Language.",e:"Runs on JVM.\nWrite Once Run Anywhere concept.\nUsed in Android and enterprise."},
{q:"What is C?",a:"Procedural language.",e:"Very fast.\nUsed in OS and embedded.\nFoundation of many languages."},
{q:"What is C++?",a:"Supports OOP + Procedural.",e:"Used in gaming & system programming.\nSupports classes & objects."},
{q:"What is DBMS?",a:"Database management system.",e:"Stores and manages data.\nEnsures security and efficiency.\nExamples MySQL, Oracle."},
{q:"What is SQL?",a:"Database query language.",e:"Used for CRUD operations.\nVery important in backend."},
{q:"What is API?",a:"System communication bridge.",e:"Allows applications to talk.\nUsed in login, payment, weather."},
{q:"Frontend vs Backend?",a:"Frontend = UI, Backend = Logic.",e:"Frontend user sees\nBackend handles processing."},
{q:"What is React?",a:"JS library for UI.",e:"Used for SPA.\nFast performance."},
{q:"What is Bootstrap?",a:"CSS framework.",e:"Ready-made UI components."},
{q:"What is Git?",a:"Version control system.",e:"Tracks code changes."},
{q:"What is GitHub?",a:"Cloud repo hosting.",e:"Team collaboration."},
{q:"What is JSON?",a:"Data exchange format.",e:"Lightweight, easy to parse."},
{q:"What is Hosting?",a:"Publishing website online.",e:"Accessible globally."},
{q:"What is IDE?",a:"Code editor tool.",e:"Helps writing programs."},
{q:"What is Compiler?",a:"Converts code to machine.",e:"Executes faster."},
{q:"What is Interpreter?",a:"Executes line by line.",e:"Used in Python & JS."},
{q:"What is Algorithm?",a:"Step by step solution.",e:"Solves problem logically."},
{q:"What is Flowchart?",a:"Graphical algorithm.",e:"Improves understanding."},
{q:"What is Variable?",a:"Storage container.",e:"Stores values."},
{q:"What is Function?",a:"Reusable code block.",e:"Reduces repetition."},
{q:"What is OOP?",a:"Object based programming.",e:"Encapsulation, Inheritance, Polymorphism."}
],

aptitude:[
{q:"50% of 200?",a:"100",e:"50% means half.\nHalf of 200 = 100."},
{q:"Average of 10,20,30?",a:"20",e:"Sum=60\nDivide by 3=20"},
{q:"Speed formula?",a:"Distance/Time",e:"Basic physics formula."},
{q:"Profit?",a:"SP-CP",e:"If SP>CP Profit"},
{q:"Loss?",a:"CP-SP",e:"If CP>SP Loss"},
{q:"SI Formula?",a:"(P×R×T)/100",e:"Used in banking"},
{q:"Highest prime under 10?",a:"7",e:"Prime means / only 1 & itself"},
{q:"Square of 12?",a:"144",e:"12×12=144"},
{q:"Cube of 3?",a:"27",e:"3×3×3"},
{q:"√81 ?",a:"9",e:"Square root"},
{q:"% means?",a:"Per hundred",e:"Out of 100"},
{q:"HCF meaning?",a:"Highest common factor",e:"Greatest divisor"},
{q:"LCM meaning?",a:"Least common multiple",e:"Smallest common multiple"},
{q:"1 dozen?",a:"12",e:"Standard quantity"},
{q:"Leap year days?",a:"366",e:"Feb=29"},
{q:"24 hrs = ?",a:"1 day",e:"Time measure"},
{q:"1000m = ?",a:"1km",e:"Unit conversion"},
{q:"Opposite of Profit?",a:"Loss",e:"Business maths"},
{q:"Work formula?",a:"Work = Rate × Time",e:"Basic math"},
{q:"Even no ends?",a:"0,2,4,6,8",e:"Easy trick"},
{q:"Odd no ends?",a:"1,3,5,7,9",e:"Easy trick"},
{q:"% of 100 always?",a:"Same number",e:"100% rule"},
{q:"Simple maths base?",a:"BODMAS",e:"Order of operations"},
{q:"Perimeter square?",a:"4a",e:"a=side"},
{q:"Area square?",a:"a²",e:"Formula based"}
],

reasoning:[
{q:"2,4,6,8,?",a:"10",e:"+2 pattern"},
{q:"Opposite of Hot?",a:"Cold",e:"Antonym"},
{q:"Animal baby of Dog?",a:"Puppy",e:"Relation"},
{q:"Sun rises from?",a:"East",e:"Fact"},
{q:"Tallest mammal?",a:"Giraffe",e:"Reality"},
{q:"Human has ___ senses",a:"5",e:"Touch Taste Hear See Smell"},
{q:"Square has ___ sides",a:"4",e:"Shape property"},
{q:"Triangle has ___ sides",a:"3",e:"Geometry"},
{q:"Clock shows?",a:"Time",e:"Reasoning logic"},
{q:"Car runs on?",a:"Road",e:"Relation"},
{q:"Birds ___",a:"Fly",e:"Common logic"},
{q:"Fish ___",a:"Swim",e:"Natural reasoning"},
{q:"Eyes used to ___",a:"See",e:"Sense logic"},
{q:"Ear used to ___",a:"Hear",e:"Sense logic"},
{q:"Brain used to ___",a:"Think",e:"Reasoning"},
{q:"Fire is ___",a:"Hot",e:"Fact"},
{q:"Ice is ___",a:"Cold",e:"Fact"},
{q:"Train runs on ___",a:"Track",e:"Relation"},
{q:"Cow gives ___",a:"Milk",e:"Fact"},
{q:"Tree gives ___",a:"Oxygen",e:"Reality"},
{q:"Apple is a ___",a:"Fruit",e:"Category"},
{q:"Rose is a ___",a:"Flower",e:"Category"},
{q:"Dog is a ___",a:"Animal",e:"Category"},
{q:"Sky is ___",a:"Blue",e:"Common fact"},
{q:"Grass is ___",a:"Green",e:"Fact"}
],

interview:[
{q:"Should you lie?",a:"No",e:"Honesty = trust"},
{q:"Speak tone?",a:"Calm",e:"Shows confidence"},
{q:"If don't know answer?",a:"Say honestly",e:"Shows maturity"},
{q:"Dress code?",a:"Formal",e:"Creates impression"},
{q:"Eye contact?",a:"Yes",e:"Shows confidence"},
{q:"Resume truth?",a:"Must be true",e:"Ethics"},
{q:"Communication?",a:"Clear",e:"Professionalism"},
{q:"Confidence?",a:"Very important",e:"Judgment factor"},
{q:"Body language?",a:"Positive",e:"Major selection role"},
{q:"Punctual?",a:"Yes",e:"Shows respect"},
{q:"Ask questions?",a:"Yes",e:"Shows interest"},
{q:"Blame old company?",a:"No",e:"Bad attitude"},
{q:"Salary talk?",a:"Politely",e:"Smart handling"},
{q:"Mobile usage?",a:"Avoid",e:"Professional behavior"},
{q:"Smile?",a:"Yes",e:"Friendly impression"},
{q:"Be honest?",a:"Always",e:"Core requirement"},
{q:"Teamwork?",a:"Supportive",e:"Corporate need"},
{q:"Leadership?",a:"Responsible",e:"Good trait"},
{q:"Knowledge?",a:"Relevant",e:"Shows preparation"},
{q:"Mistake?",a:"Accept & improve",e:"Shows learning"},
{q:"Confidence vs overconfidence?",a:"Balance",e:"Smart approach"},
{q:"Respect HR?",a:"Yes",e:"Professional ethics"},
{q:"Follow up?",a:"Yes",e:"Shows interest"},
{q:"Be polite?",a:"Always",e:"Professional"},
{q:"Learn attitude?",a:"Must",e:"Company expects"}
],

gd:[
{q:"GD should be?",a:"Discussion",e:"Not argument"},
{q:"Tone?",a:"Calm",e:"Shows maturity"},
{q:"Respect?",a:"Yes",e:"Shows professionalism"},
{q:"Shouting allowed?",a:"No",e:"Shows immaturity"},
{q:"Team focus?",a:"Yes",e:"Shows leadership"},
{q:"Listen others?",a:"Yes",e:"Shows respect"},
{q:"Interrupt?",a:"No",e:"Bad behavior"},
{q:"Stay logical?",a:"Yes",e:"Strong point"},
{q:"Be clear?",a:"Yes",e:"Good communication"},
{q:"Dominate?",a:"No",e:"Be balanced"},
{q:"Give chance?",a:"Yes",e:"Team spirit"},
{q:"Be confident?",a:"Yes",e:"Important"},
{q:"Eye contact?",a:"Yes",e:"Confidence"},
{q:"Stick to topic?",a:"Yes",e:"Relevance"},
{q:"Avoid personal points?",a:"Yes",e:"Professional"},
{q:"Don't get emotional?",a:"Yes",e:"Maturity"},
{q:"Be logical?",a:"Always",e:"Winning factor"},
{q:"Positive body language?",a:"Yes",e:"Influence"},
{q:"Conclusion?",a:"Strong",e:"Final impact"},
{q:"Learn attitude?",a:"Must",e:"Corporate culture"},
{q:"Be polite?",a:"Yes",e:"Respect"},
{q:"Encourage others?",a:"Yes",e:"Leader quality"},
{q:"Stay factual?",a:"Yes",e:"Credibility"},
{q:"Avoid rumors?",a:"Yes",e:"Professional"},
{q:"Be supportive?",a:"Yes",e:"Teamwork"}
]
};

// =================================================================================
// QUIZ DATA (35 QUESTIONS EACH)
// =================================================================================
const quizData = {
coding: [],
aptitude: [],
reasoning: [],
interview: [],
gd: []
};

// ---------------- Filling quiz 35 Questions each ------------------
function fillQuiz(topic,labelA,labelB,labelC,labelD,correctIndex){
for(let i=1;i<=35;i++){
quizData[topic].push({
q:`${topic.toUpperCase()} Question ${i}`,
options:[labelA,labelB,labelC,labelD],
correct:correctIndex
});
}
}

fillQuiz("coding","Option A","Option B","Option C","Option D",0);
fillQuiz("aptitude","10","20","30","40",2);
fillQuiz("reasoning","Yes","No","Maybe","None",1);
fillQuiz("interview","Good","Better","Best","Bad",2);
fillQuiz("gd","Agree","Disagree","Neutral","None",2);

// =================================================================================
// UI CONTROL
// =================================================================================
const topicBox=document.getElementById("topicBox");
const practiceSection=document.getElementById("practiceSection");
const quizSection=document.getElementById("quizSection");
const practiceContainer=document.getElementById("practiceContainer");
const quizForm=document.getElementById("quizForm");
const quizResult=document.getElementById("quizResult");
const submitQuiz=document.getElementById("submitQuiz");

document.getElementById("modePractice").onclick=()=>{
topicBox.classList.remove("hidden");
practiceSection.classList.remove("hidden");
quizSection.classList.add("hidden");
};

document.getElementById("modeQuiz").onclick=()=>{
topicBox.classList.remove("hidden");
quizSection.classList.remove("hidden");
practiceSection.classList.add("hidden");
};

document.querySelectorAll(".topicBtn").forEach(btn=>{
btn.addEventListener("click",()=>{
let topic=btn.dataset.topic;
renderPractice(topic);
startQuiz(topic);
});
});

// =================================================================================
// PRACTICE LOGIC
// =================================================================================
function renderPractice(topic){
practiceContainer.innerHTML="";
practiceData[topic].forEach((x,i)=>{
let box=document.createElement("div");
box.className="qaBox";
box.innerHTML=
`<b>${i+1}. ${x.q}</b><br>
<button onclick="toggleAns('${topic}${i}')">Show Answer</button>
<div id="${topic}${i}" class="ans">
<b>Answer:</b> ${x.a}<br>
${x.e.replace(/\n/g,"<br>")}
</div>`;
practiceContainer.appendChild(box);
});
}

window.toggleAns=function(id){
let x=document.getElementById(id);
x.style.display = x.style.display==="none" || x.style.display==="" ? "block":"none";
};

// =================================================================================
// QUIZ LOGIC
// =================================================================================
let activeQuiz=[];

function startQuiz(topic){
activeQuiz=quizData[topic];
quizForm.innerHTML="";
activeQuiz.forEach((q,i)=>{
let optionsHTML=q.options.map((o,idx)=>`
<label>
<input type="radio" name="q${i}" value="${idx}">
${o}
</label><br>`).join("");

quizForm.innerHTML+=
`<div class="qaBox">
<b>Q${i+1}. ${q.q}</b><br>${optionsHTML}
</div>`;
});

submitQuiz.classList.remove("hidden");
}

submitQuiz.onclick=()=>{
let score=0;
activeQuiz.forEach((q,i)=>{
let ans=document.querySelector(`input[name='q${i}']:checked`);
if(ans && parseInt(ans.value)===q.correct) score++;
});

let level = score<=10?"Good":score<=25?"Better":"Best";
quizResult.classList.remove("hidden");
quizResult.innerHTML=
`<h3>Your Score: ${score} / ${activeQuiz.length}</h3>
<h2>Performance: ${level}</h2>`;
};

