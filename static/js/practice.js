
"use strict";
const coursesData = {
  python: [
    { title: "Python Full Course – Beginner to Advanced", link: "https://www.youtube.com/watch?v=rfscVS0vtbw" },
    { title: "Python OOP Concepts", link: "https://www.youtube.com/watch?v=Ej_02ICOIgs" }
  ],
  dsa: [
    { title: "DSA Full Course", link: "https://www.youtube.com/watch?v=8hly31xKli0" },
    { title: "DSA with Python", link: "https://www.youtube.com/watch?v=pkYVOmU3MgA" }
  ],
  web: [
    { title: "Full Stack Web Development", link: "https://www.youtube.com/watch?v=nu_pCVPKzTk" }
  ]
};

/* PRACTICE QUESTIONS */
const practiceData = {
coding:[
   {
    q: "What is the difference between a programming language and a framework?",
    a: `A programming language is the base tool we use to write logic, such as Python, C, or Java.
A framework is built on top of a language to simplify development, like Django for Python or React for JavaScript.
Languages provide rules and syntax, while frameworks provide pre-built structures.
In simple words: Language = foundation, Framework = ready-made structure to speed up work.`
  },
  {
    q: "What do we mean by compilation and interpretation in programming?",
    a: `Compilation converts the entire code into machine language at once before execution, like C or C++.
Interpretation executes code line-by-line, like Python or JavaScript.
Compiled programs are usually faster because they are converted beforehand.
Interpreted programs are easier to debug but may run slower than compiled ones.`
  },
  {
    q: "What is the importance of variables in programming?",
    a: `Variables are used to store data so the program can remember and process values.
They allow dynamic operations like calculations, decisions, and data handling.
Without variables, we cannot manage user input, database values, or runtime data.
They act like labeled containers where we keep information during program execution.`
  },
  {
    q: "Explain what a function is and why it is used.",
    a: `A function is a block of reusable code designed to perform a specific task.
Instead of writing the same code again and again, we call the function when needed.
It improves code readability, reduces repetition, and makes maintenance easy.
Functions also help in breaking big programs into manageable pieces.`
  },
  {
    q: "What is the difference between frontend and backend development?",
    a: `Frontend is what the user sees and interacts with, like UI, buttons, and design.
Backend works behind the scenes like databases, servers, and application logic.
Frontend focuses on user experience, while backend focuses on data handling and performance.
Together they form a complete working application or website.`
  },
  {
    q: "What is a database and why do applications need it?",
    a: `A database stores structured information like user data, records, and transactions.
Applications need databases to save data permanently instead of losing it after closing.
It helps in retrieving, updating, and managing data efficiently.
Without databases, modern applications like banking, e-commerce, or social media cannot function.`
  },
  {
    q: "What is the meaning of debugging in programming?",
    a: `Debugging means finding and fixing errors in the program.
Errors can be syntax errors, logical mistakes, or runtime issues.
Debugging ensures that the application works correctly and efficiently.
It is one of the most important skills every programmer must develop.`
  },
  {
    q: "What are conditional statements and why are they important?",
    a: `Conditional statements help programs make decisions based on conditions.
Examples include if, else, and switch statements.
They allow programs to react differently for different inputs or situations.
Without conditions, programs would always behave the same way without intelligence.`
  },
  {
    q: "Explain loops and their purpose in programming.",
    a: `Loops allow us to repeat a block of code multiple times automatically.
Common types include for loop, while loop, and do-while loop.
They reduce manual repetition and make code shorter and efficient.
Loops are used in tasks like iterating lists, processing records, and automation.`
  },
  {
    q: "What is an algorithm in programming?",
    a: `An algorithm is a step-by-step solution to solve a particular problem.
It describes how the program should process input to get desired output.
Good algorithms are efficient, clear, and minimize time and memory usage.
They form the backbone of logical programming and problem solving.`
  },
  {
    q: "What is the role of comments in code?",
    a: `Comments are non-executable lines used to explain code meaning.
They help developers understand complex logic or purpose of a function.
Comments improve code readability, especially in large projects.
They are useful for teamwork, maintenance, and learning.`
  },
  {
    q: "What is object-oriented programming (OOP)?",
    a: `OOP is a programming style based on real-world objects and concepts.
It organizes code into classes and objects instead of simple procedures.
Key principles include inheritance, encapsulation, polymorphism, and abstraction.
OOP makes programs more modular, reusable, and easier to manage.`
  },
  {
    q: "Explain what an API is in simple terms.",
    a: `API stands for Application Programming Interface.
It allows two software applications to communicate and share data.
For example, login with Google or payment gateways use APIs.
They help integrate services without exposing internal system details.`
  },
  {
    q: "What is Git and why is it important for developers?",
    a: `Git is a version control system used to track code changes.
It allows multiple developers to work on the same project safely.
You can restore older versions if something goes wrong.
It is essential in teamwork, industry projects, and professional development.`
  },
  {
    q: "What is responsive web design?",
    a: `Responsive design ensures that a website works well on mobiles, tablets, and desktops.
It adjusts layout automatically based on screen size.
Technologies like CSS Flexbox, Grid, and media queries help achieve it.
Without responsiveness, users will face bad experience on different devices.`
  },
  {
    q: "Explain client-server architecture.",
    a: `In client-server architecture, the client requests services and the server provides them.
Client is usually a browser or application, while server stores data and logic.
They communicate over the internet using protocols.
This structure is used in almost every modern application.`
  },
  {
    q: "What is recursion in programming?",
    a: `Recursion is when a function calls itself to solve smaller parts of a problem.
It is useful in problems like tree traversal, factorial, and Fibonacci.
However, it must have a stopping condition to avoid infinite looping.
Recursion simplifies logic but should be used carefully for performance.`
  },
  {
    q: "What is exception handling?",
    a: `Exception handling deals with unexpected errors during program execution.
Instead of crashing, the program handles errors gracefully.
It helps improve stability and user experience.
Try-catch blocks are commonly used to manage exceptions.`
  },
  {
    q: "What is the difference between array and list?",
    a: `Array is a fixed-size collection of similar data types.
List is dynamic and can grow or shrink as needed.
Arrays are faster but less flexible, while lists are easier to use.
Choice depends on the requirement and programming language.`
  },
  {
    q: "What is the purpose of a IDE?",
    a: `IDE stands for Integrated Development Environment.
It provides tools like code editor, debugger, compiler, and testing support.
Popular IDEs include VS Code, PyCharm, Eclipse, and IntelliJ.
IDE makes coding faster, easier, and more productive.`
  },
  {
    q: "What is time complexity in coding?",
    a: `Time complexity measures how fast an algorithm runs as input grows.
It helps compare efficiency of different solutions.
Big-O notation is commonly used like O(n), O(log n), O(n^2).
Better time complexity means faster performance.`
  },
  {
    q: "Explain data structures in simple words.",
    a: `Data structures are organized ways to store and manage data.
Examples include arrays, stacks, queues, linked lists, and trees.
They improve speed and efficiency of operations.
Choosing correct data structure is key to good programming.`
  },
  {
    q: "What is multithreading?",
    a: `Multithreading allows a program to perform multiple tasks simultaneously.
It improves performance especially in heavy processing.
Useful in games, servers, and real-time applications.
However, it requires careful handling to avoid conflicts.`
  },
  {
    q: "What is a library in programming?",
    a: `A library is a collection of pre-written code for common tasks.
Instead of writing everything, developers simply use library functions.
It saves time and reduces complexity.
Examples include NumPy, Pandas, React, STL, etc.`
  },
  {
    q: "Explain what full stack development means.",
    a: `Full stack means working on both frontend and backend.
A full stack developer handles UI, server logic, and database.
They understand complete application workflow.
Such developers are highly valuable in industry.`
  },
  {
    q: "What is a syntax error?",
    a: `Syntax error occurs when code does not follow language rules.
It prevents program from running at all.
Common examples: missing brackets, wrong keywords, or typos.
They are usually easy to identify and fix.`
  },
  {
    q: "What is a logical error?",
    a: `Logical error happens when code runs but produces wrong output.
It occurs due to incorrect logic or wrong approach.
These are harder to find because program doesn’t crash.
Testing helps identify and resolve them.`
  },
  {
    q: "What is runtime error?",
    a: `Runtime error happens while program is running.
It may occur due to invalid input, memory issues, or missing files.
Program stops suddenly when runtime error occurs.
Exception handling helps control such situations.`
  },
  {
    q: "Why is clean code important?",
    a: `Clean code is easy to read, understand, and maintain.
It uses good naming, proper formatting, and structured logic.
Teams can work better on clean code bases.
It reduces bugs and improves project quality.`
  },
  {
    q: "What is deployment in software development?",
    a: `Deployment means making a software available for users.
It moves code from development to live environment.
It includes hosting, configuration, and monitoring.
Without deployment, even a good project cannot reach users.`
  }
],

aptitude:[
  {
    q: "What is aptitude and why is it important in placements?",
    a: "Aptitude measures logical thinking, numerical ability, and problem-solving skills. Companies test aptitude to understand how quickly and smartly a candidate can think in real situations."
  },
  {
    q: "Why do companies give aptitude tests before interviews?",
    a: "Aptitude tests filter candidates based on analytical and reasoning skills. They ensure that selected candidates can learn fast, understand problems, and perform well in dynamic environments."
  },
  {
    q: "What is the difference between aptitude and intelligence?",
    a: "Intelligence is a broad mental ability, while aptitude focuses on specific skills like logic, math, reasoning, and decision-making. Aptitude reflects job readiness and learning capability."
  },
  {
    q: "Why is time management important in aptitude exams?",
    a: "Most aptitude tests are time-bound, so solving fast with accuracy is crucial. Time management helps prioritize easier questions first and improves overall performance."
  },
  {
    q: "What is Numerical Aptitude?",
    a: "Numerical Aptitude tests your ability to work with numbers, calculations, data, and logic. It checks mathematical understanding and speed of solving numeric-based problems."
  },
  {
    q: "What is Logical Reasoning in aptitude?",
    a: "Logical Reasoning tests your thinking pattern, ability to draw conclusions, and analyze situations. It checks how well you understand patterns, sequences, and logical relationships."
  },
  {
    q: "What are Verbal Ability questions in aptitude?",
    a: "Verbal ability tests communication, grammar, comprehension, and sentence understanding. It ensures you can understand instructions and communicate clearly in a workplace."
  },
  {
    q: "Why do aptitude tests include Data Interpretation?",
    a: "Data Interpretation tests your ability to understand graphs, charts, tables, and numerical data. It checks analytical thinking and decision-making abilities in real business situations."
  },
  {
    q: "How does aptitude help in real-life situations?",
    a: "Aptitude improves decision-making, logical thinking, and analytical skills. It helps in solving daily life problems smarter and improves professional performance."
  },
  {
    q: "What are common aptitude test sections?",
    a: "Common sections include Quantitative Aptitude, Logical Reasoning, Verbal Ability, and Data Interpretation. Some exams also add puzzles, probability, and analytical reasoning."
  },
  {
    q: "Is speed more important than accuracy in aptitude?",
    a: "Both are important, but accuracy matters more. Wrong answers reduce score or confidence. First maintain accuracy, then improve speed through practice."
  },
  {
    q: "Why do aptitude exams include puzzles?",
    a: "Puzzles check creativity, problem-solving approach, and structured thinking. They help companies see how candidates handle tricky or confusing situations logically."
  },
  {
    q: "What is the benefit of practicing aptitude daily?",
    a: "Daily practice builds speed, confidence, and thinking ability. It strengthens concepts, improves memory, and helps perform better in real exams."
  },
  {
    q: "Why do aptitude questions include percentages and ratios?",
    a: "Percentages and ratios help evaluate numerical understanding and calculation ability. These topics are commonly used in finance, business, and everyday decision making."
  },
  {
    q: "What is the importance of simplification in aptitude?",
    a: "Simplification helps solve large or complex calculations quickly. It shows how efficiently a candidate can reduce problems and get answers faster."
  },
  {
    q: "What role does practice play in aptitude success?",
    a: "Aptitude is skill-based, so more practice improves speed, accuracy, and confidence. It helps build problem-solving strategies and familiarity with question patterns."
  },
  {
    q: "Why is logical ability important in technical fields?",
    a: "Logical ability helps in coding, debugging, and system thinking. It improves structured thinking, which is essential for solving technical and engineering problems."
  },
  {
    q: "What is the purpose of seating arrangement questions?",
    a: "They test your understanding of positions, arrangements, and logical placements. These questions judge clarity of thinking and ability to handle structured information."
  },
  {
    q: "Why do aptitude exams include probability questions?",
    a: "Probability measures risk analysis and prediction skills. It is useful in finance, analytics, decision-making, and real-life uncertain situations."
  },
  {
    q: "What is the importance of problem-solving skills?",
    a: "Problem-solving helps handle challenges calmly and logically. It improves confidence, creativity, and adaptability in academic and workplace environments."
  },
  {
    q: "What does data sufficiency test in aptitude?",
    a: "Data sufficiency checks whether given information is enough to answer a question. It tests reasoning power, judgment, and analytical decision-making."
  },
  {
    q: "Why is mental calculation speed important?",
    a: "Fast calculation saves time, improves accuracy, and boosts confidence. It reduces dependency on calculators and helps in competitive exams and daily life."
  },
  {
    q: "What does critical thinking mean in aptitude?",
    a: "Critical thinking means analyzing information deeply before concluding. It checks judgment ability, understanding, and smart decision-making power."
  },
  {
    q: "Why are aptitude tests standardized?",
    a: "Standardization ensures fair evaluation for all candidates. It provides equal testing conditions and unbiased measurement of skills."
  },
  {
    q: "What is the purpose of blood relation questions?",
    a: "Blood relation questions test logical understanding of family connections. They check clarity, interpretation skills, and relationship reasoning ability."
  },
  {
    q: "What does direction sense in aptitude measure?",
    a: "Direction sense measures spatial thinking and understanding of directions. It helps test logical visualization and movement-based reasoning."
  },
  {
    q: "Why do aptitude exams include series and pattern questions?",
    a: "Series and patterns check observation skills and logical sequence recognition. They show how well a candidate identifies trends and logical steps."
  },
  {
    q: "How does aptitude reflect career readiness?",
    a: "Strong aptitude shows intelligence, decision ability, and learning capacity. It indicates how quickly a candidate can adapt and perform in professional environments."
  },
  {
    q: "What does reasoning ability show about a person?",
    a: "Reasoning ability shows clarity of thought, logical sense, and stable thinking. It reflects how well a person analyzes and understands situations."
  },
  {
    q: "Why do students fear aptitude and how to overcome it?",
    a: "Students fear aptitude due to lack of practice and confidence. Regular practice, understanding basics, and solving stepwise helps overcome fear easily."
  },
  {
    q: "What is the basic idea of Percentage in Aptitude problems?",
    a: "Percentage represents a value out of 100. It helps in comparing numbers, calculating increases or decreases, and understanding proportions in real scenarios like marks, salary hike, and discounts."
  },
  {
    q: "Why is Ratio & Proportion important in aptitude?",
    a: "Ratio compares two quantities while proportion shows equality of two ratios. It is widely used in mixing problems, population calculations, recipes, and speed–time problems."
  },
  {
    q: "What do Profit and Loss questions generally check?",
    a: "They test understanding of cost price, selling price, profit percentage, and loss percentage. These concepts are practical in business, shopping discounts, and financial decision making."
  },
  {
    q: "What is the main concept of Simple Interest?",
    a: "Simple Interest is calculated only on the principal amount for the entire period. It is useful in bank deposits, loans, and basic financial calculations."
  },
  {
    q: "How is Compound Interest different from Simple Interest?",
    a: "Compound Interest is calculated on principal plus accumulated interest. It grows faster than simple interest and is widely used in banking, investments, and savings."
  },
  {
    q: "What does Time and Work topic mainly deal with?",
    a: "It checks how fast work is completed individually or together. It is based on work rate and helps in understanding teamwork efficiency and resource planning."
  },
  {
    q: "What is the concept behind Time, Speed and Distance problems?",
    a: "These problems relate speed, distance, and time. They help understand travel time, motion, and real-life journey situations effectively."
  },
  {
    q: "Why are Average questions important?",
    a: "Averages help represent data in a simple way. They are useful in calculating marks, performance evaluation, salary analysis, and statistics."
  },
  {
    q: "What do Partnership questions test?",
    a: "They test investment and profit-sharing based on capital and time. These are helpful in business decision-making and understanding financial contributions."
  },
  {
    q: "What is the basic idea behind Age problems?",
    a: "Age problems compare present, past, and future ages using equations. They help build logical and algebraic thinking."
  },
  {
    q: "Why is Data Interpretation important?",
    a: "Data Interpretation tests your ability to understand tables, charts, and graphs. It checks analytical thinking and is highly relevant in business and analytics jobs."
  },
  {
    q: "What do Probability questions measure?",
    a: "Probability measures chances of an event happening. It helps in risk analysis, predictions, games, and decision-making in uncertain situations."
  },
  {
    q: "What is the concept of Permutation?",
    a: "Permutation deals with arrangements where order matters, like seating arrangements, passwords, and rankings."
  },
  {
    q: "What is Combination in aptitude?",
    a: "Combination deals with selections where order does not matter. It is useful in team selections, lottery, and choosing groups from a set."
  },
  {
    q: "What do Number System questions usually test?",
    a: "They focus on divisibility rules, factors, multiples, and remainders. These form the base of many other aptitude topics."
  },
],

reasoning:[
  {q:"What comes next in the series: 2, 4, 8, 16, ?", a:"32", e:"Each number doubles the previous one: 16×2=32."},
  {q:"Find the next number: 1, 4, 9, 16, ?", a:"25", e:"Pattern is perfect squares: 1²,2²,3²,4² → next is 5²=25."},
  {q:"Find the missing number: 2, 5, 10, 17, ?", a:"26", e:"Pattern is n²+1 → 1²+1=2,2²+1=5,3²+1=10,4²+1=17,5²+1=26."},

  // Odd One Out
  {q:"Find the odd one out: 2, 3, 5, 7, 9", a:"9", e:"All others are prime numbers; 9 is not prime."},
  {q:"Which word does not belong: Apple, Banana, Carrot, Mango", a:"Carrot", e:"Carrot is a vegetable, others are fruits."},

  // Analogy
  {q:"Dog : Puppy :: Cat : ?", a:"Kitten", e:"Just like a puppy is a young dog, a kitten is a young cat."},
  {q:"Pen : Write :: Knife : ?", a:"Cut", e:"Pen is used to write, knife is used to cut."},

  // Blood Relation
  {q:"A is father of B, B is mother of C. How is C related to A?", a:"Grandchild", e:"B is A's child, C is B's child → C is A's grandchild."},
  {q:"Pointing to a man, she says, 'He is the son of my grandmother's only daughter.' Who is he?", a:"Brother", e:"Grandmother's only daughter is mother → man is her brother."},

  // Direction Sense
  {q:"If you face north and turn 90° right, which direction do you face?", a:"East", e:"Turning 90° right from north faces east."},
  {q:"A walks 5km north, then 3km east. How far from start?", a:"√(5²+3²)=5.83km", e:"Use Pythagoras theorem: √(5²+3²)=5.83 km."},

  // Seating Arrangement
  {q:"Five people sit in a row. A is left of B, C is right of B, D is at one end, E is left of C. Who is in the middle?", a:"B", e:"Arrange logically: D, A, B, C, E → B is in middle."},
  {q:"Three friends sit in a triangle facing center. Who is opposite to whom?", a:"Depends on arrangement", e:"Visualize positions to find opposite person."},

  // Clock & Calendar
  {q:"Clock shows 3:15. Angle between hour and minute hand?", a:"7.5°", e:"Hour=97.5°, Minute=90° → difference=7.5°."},
  {q:"January 1, 2025 is Wednesday. What day is Jan 7?", a:"Tuesday", e:"Count days: Wednesday=1 Jan → Jan 7 is Tuesday."},

  // Puzzle
  {q:"If 5 people can complete a work in 10 days, how long for 10 people?", a:"5 days", e:"Work is inversely proportional to number of people → 5×10=10×x → x=5 days."},
  {q:"Three friends share ₹120 in ratio 2:3:5. How much for each?", a:"24,36,60", e:"Sum of ratio=10 → share=2/10*120,3/10*120,5/10*120."},

  // Statement & Conclusion
  {q:"All cats are animals. Some animals are dogs. Is some cats are dogs?", a:"Cannot say", e:"Cannot conclude because cats and dogs may not overlap."},
  {q:"All roses are flowers. Some flowers are red. Are all roses red?", a:"Cannot say", e:"Only some flowers are red; cannot conclude for roses."},

  // Assumptions
  {q:"If a statement says 'All students must submit assignment', what is implied?", a:"Students are required to submit", e:"Assumes every student has an assignment."},
  {q:"If 'Traffic signal is red, stop', what is assumption?", a:"Red means stop", e:"Assumes red color signals stopping."},

  // Misc Logical
  {q:"If 2 pencils cost ₹10, 5 pencils?", a:"₹25", e:"Cost per pencil=5 → 5 pencils=5×5=25."},
  {q:"Find the missing: 101, 103, 107, 109, ?", a:"113", e:"Series of consecutive prime numbers → next is 113."},
  {q:"In a code, A=1,B=2...,CAT=?", a:"24", e:"C=3,A=1,T=20 → sum=24."},
  {q:"If '+' means ×, '-' means +, 2+3-4=?", a:"10", e:"Replace symbols: 2×3+4=10."},
  {q:"Find next in pattern: 1,2,6,24, ?", a:"120", e:"Factorial series: 1!,2!,3!,4!,5!=120."},
  {q:"Which number is multiple of both 4 and 6 under 50?", a:"12", e:"LCM of 4 and 6 is 12."},
  {q:"If a cube has 6 faces, how many edges?", a:"12", e:"Cube has 12 unique edges."},
  {q:"Find the missing: 2,3,5,7,11, ?", a:"13", e:"Series of prime numbers → next is 13."},
  {q:"Seating puzzle: A,B,C,D,E sit in circle, B opposite D, C left of A. Who is right of E?", a:"A", e:"Logical arrangement of circular seating."},
  {q:"Which is odd in: 21,34,55,89,100?", a:"100", e:"All others are Fibonacci numbers; 100 is not."}

],

interview:[
 {q:"Tell me about yourself.", a:"Give a brief introduction.", e:"Mention your education, skills, projects, and key strengths clearly and confidently."},
  {q:"What are your strengths?", a:"Highlight 2–3 key skills.", e:"Focus on skills that relate to the job and give examples of how you applied them."},
  {q:"What are your weaknesses?", a:"Be honest but positive.", e:"Mention a weakness you are improving on and steps you are taking to overcome it."},
  {q:"Why should we hire you?", a:"Show value you bring.", e:"Explain your skills, experience, and enthusiasm that make you a good fit for the role."},
  {q:"Where do you see yourself in 5 years?", a:"Discuss career growth.", e:"Talk about learning, improving skills, and contributing to the company."},
  {q:"Describe a challenging situation.", a:"Explain problem-solving.", e:"Mention a problem you faced, actions you took, and positive outcome achieved."},
  {q:"How do you handle stress?", a:"Demonstrate coping skills.", e:"Explain methods like planning, prioritizing, and staying calm under pressure."},
  {q:"Describe a team conflict you faced.", a:"Show conflict resolution.", e:"Explain the situation, your approach, and how it was resolved peacefully."},
  {q:"How do you handle criticism?", a:"Be open to feedback.", e:"Take feedback positively and show willingness to improve."},
  {q:"Tell me about a project you led.", a:"Explain leadership.", e:"Describe your role, responsibilities, challenges, and successful results."},
  {q:"How do you prioritize tasks?", a:"Time management skills.", e:"Explain how you organize work by importance and deadlines."},
  {q:"Do you prefer working alone or in a team?", a:"Show flexibility.", e:"Explain both approaches and give examples of success in team collaboration."},
  {q:"Tell me about a failure you faced.", a:"Demonstrate learning.", e:"Explain the situation, what went wrong, and lessons learned."},
  {q:"How do you motivate yourself?", a:"Self-motivation techniques.", e:"Describe goal-setting, planning, and staying positive."},
  {q:"Why do you want this job?", a:"Show interest.", e:"Relate your skills and career goals to the company and role."},
  {q:"How do you handle tight deadlines?", a:"Demonstrate efficiency.", e:"Explain your method of prioritization and focused execution."},
  {q:"What is your leadership style?", a:"Describe approach.", e:"Provide examples of guiding a team, delegating, and achieving results."},
  {q:"How do you resolve disagreements in a team?", a:"Conflict resolution.", e:"Emphasize listening, compromise, and solution-focused discussion."},
  {q:"What motivates you at work?", a:"Intrinsic motivation.", e:"Learning, achieving goals, recognition, and making impact."},
  {q:"How do you handle repetitive tasks?", a:"Show patience & focus.", e:"Explain keeping quality, finding efficiency, and staying engaged."},
  {q:"Tell me about a decision you made.", a:"Decision-making skills.", e:"Describe situation, options considered, and outcome achieved."},
  {q:"How do you stay updated in your field?", a:"Continuous learning.", e:"Mention courses, news, webinars, and practical applications."},
  {q:"Have you ever disagreed with a manager?", a:"Professional handling.", e:"Explain disagreement respectfully, and how you worked towards compromise."},
  {q:"How do you manage multiple projects?", a:"Organization skills.", e:"Use planning tools, prioritize tasks, and communicate clearly."},
  {q:"What are your career goals?", a:"Short-term and long-term.", e:"Show ambition and alignment with the company’s growth."},
  {q:"How do you handle unexpected problems?", a:"Problem-solving.", e:"Stay calm, analyze situation, and implement effective solution."},
  {q:"Tell me about a time you showed initiative.", a:"Proactivity.", e:"Describe a situation where you took action beyond your responsibilities."},
  {q:"How do you adapt to changes?", a:"Flexibility.", e:"Explain embracing change positively and adjusting work strategy."},
  {q:"What is your approach to learning new skills?", a:"Learning ability.", e:"Demonstrate curiosity, practice, and applying knowledge effectively."},
  {q:"How do you ensure quality in your work?", a:"Attention to detail.", e:"Explain reviewing, checking, and improving outcomes consistently."},
  {q:"Why should we select you over others?", a:"Unique value.", e:"Highlight your strengths, experience, and commitment that set you apart."}
],

gd:[
{q:"What is a Group Discussion (GD)?", a:"GD is a structured discussion among candidates.", e:"A Group Discussion is a process where a group of people discuss a topic to evaluate their communication, thinking, and teamwork skills. It helps assess confidence, knowledge, and leadership potential in a professional setting."},
{q:"Why is GD conducted in interviews?", a:"To evaluate skills beyond academics.", e:"GD is conducted to analyze a candidate's problem-solving ability, communication skills, team participation, and ability to handle pressure. Employers use it to identify potential leaders and collaborative team members."},
{q:"How is GD different from a debate?", a:"Focus is on collaboration, not winning.", e:"Unlike debates, GDs are not about winning an argument but discussing ideas constructively. Participants are expected to present opinions, listen actively, and reach logical conclusions as a group."},
{q:"What skills are evaluated in GD?", a:"Communication, confidence, leadership, and knowledge.", e:"During a GD, evaluators observe how candidates articulate their thoughts, interact with others, maintain body language, show listening skills, and contribute meaningful points relevant to the topic."},
{q:"What role does body language play in GD?", a:"Important for expressing confidence.", e:"Positive body language like eye contact, upright posture, gestures, and attentiveness shows confidence and professionalism. Poor body language can convey disinterest or lack of engagement."},
{q:"What is the importance of listening in GD?", a:"Active listening is crucial.", e:"Participants must carefully listen to others’ points before responding. Listening ensures meaningful contributions, prevents repetition, and shows respect for different opinions."},
{q:"How to initiate a GD?", a:"Start with a clear, concise opening.", e:"The first participant sets the tone by briefly summarizing the topic, providing context, and presenting their viewpoint confidently. A strong start demonstrates leadership and clarity of thought."},
{q:"How to handle interruptions in GD?", a:"Politely assert your point.", e:"If interrupted, stay calm, acknowledge others, and continue your point respectfully. Maintaining composure shows maturity and effective communication skills."},
{q:"What is the ideal number of points to present?", a:"3–4 strong points.", e:"Focus on quality over quantity. Presenting a few well-structured points with examples is more impactful than listing many ideas superficially."},
{q:"How to conclude a GD?", a:"Summarize key points.", e:"The conclusion should briefly recap the discussion, highlight consensus or diverse viewpoints, and end on a professional note. A good conclusion leaves a positive impression on evaluators."},
{q:"What topics are common in GD?", a:"Current affairs, technology, business, and social issues.", e:"Topics may include climate change, digital transformation, work-from-home trends, ethical dilemmas, or societal challenges. Candidates should stay informed to contribute effectively."},
{q:"How to handle disagreement?", a:"Respectfully present counterpoints.", e:"Disagree politely by providing logical reasoning. Avoid arguments or dominating the discussion. Respecting others’ opinions is crucial for professional interaction."},
{q:"What is the role of a moderator in GD?", a:"Guides and evaluates the discussion.", e:"Moderators may introduce the topic, manage time, and ensure smooth flow. They also observe participant skills like communication, leadership, and teamwork."},
{q:"Can you participate without speaking much?", a:"Active listening counts but speaking is essential.", e:"While listening is important, active participation is required to demonstrate communication and analytical skills. Contribute at least 2–3 meaningful points."},
{q:"How to use examples in GD?", a:"Support points with real-life examples.", e:"Using examples from current events, studies, or personal experiences strengthens your argument, shows awareness, and makes contributions more convincing."},
{q:"Is interrupting allowed in GD?", a:"No, but assert politely when needed.", e:"Avoid cutting others off unnecessarily. You may interject only to clarify or add value, always maintaining a respectful tone."},
{q:"What is the time limit in GD?", a:"Typically 10–15 minutes.", e:"Most GDs last around 10–15 minutes for 8–10 participants. Each participant should manage their time to contribute effectively without monopolizing the discussion."},
{q:"How to stay relevant in GD?", a:"Stick to the topic.", e:"Avoid straying from the subject. Ensure your points relate directly to the topic and add value to the overall discussion."},
{q:"Can humor be used in GD?", a:"Use cautiously.", e:"A light, relevant humor can engage participants but avoid jokes that may offend or distract. Professionalism is key."},
{q:"How to deal with dominant speakers?", a:"Stay confident and assert politely.", e:"Do not get intimidated. Wait for a natural pause, then present your point clearly. Respectful assertiveness is valued."},
{q:"What is the ideal tone in GD?", a:"Calm, confident, and polite.", e:"Maintain a steady voice, clarity in words, and friendly demeanor. Aggressive or loud tone can negatively impact perception."},
{q:"How to prepare for GD?", a:"Research and practice.", e:"Read current affairs, trending topics, and common GD scenarios. Practice expressing points concisely with friends or mentors."},
{q:"What is the importance of teamwork in GD?", a:"Collaboration is key.", e:"Show ability to work with others, support ideas, build on points, and help reach a common understanding."},
{q:"How to handle nervousness?", a:"Practice and focus.", e:"Take deep breaths, focus on your points, and maintain eye contact. Confidence grows with preparation."},
{q:"Is prior knowledge necessary?", a:"Helpful but not mandatory.", e:"Having background information improves contribution quality. However, logical reasoning and communication skills also matter."},
{q:"How to balance speaking and listening?", a:"Ensure fair participation.", e:"Speak clearly when you have points, but also listen actively. Avoid dominating or staying silent entirely."},
{q:"How to present a unique idea?", a:"Be innovative but relevant.", e:"Introduce original viewpoints backed with reasoning or examples. Creativity is appreciated if it aligns with the topic."},
{q:"What role does ethics play in GD?", a:"High importance.", e:"Avoid unethical arguments, personal attacks, or biased statements. Professional behavior and respect are crucial in GD evaluation."},
{q:"Topic: Corporate Ethics", a:"Moral principles in business.", e:"Corporate ethics involves fairness, transparency, and responsibility in business practices. GD topics can cover whistleblowing, sustainability, and employee treatment. Demonstrating understanding of ethical dilemmas shows maturity and professional insight."},

{q:"Topic: Work-Life Balance", a:"Healthy balance between work and personal life.", e:"Work-life balance ensures productivity while maintaining well-being. In GDs, candidates can discuss flexible hours, remote work, and stress management. Presenting practical solutions shows empathy, planning skills, and awareness of workplace dynamics."},

{q:"Topic: Leadership Skills", a:"Ability to guide a team.", e:"Leadership involves motivating, guiding, and supporting a team to achieve goals. GD discussions can cover traits of good leaders, challenges, and real-life examples. Explaining leadership with practical examples reflects understanding and self-awareness."},

{q:"Topic: Cybersecurity", a:"Protecting digital assets.", e:"Cybersecurity is the practice of protecting computers and networks from threats. GDs may discuss phishing, data leaks, and preventive measures. Presenting solutions and awareness shows analytical thinking and technical literacy."},

{q:"Topic: Environmental Pollution", a:"Contamination of natural resources.", e:"Pollution affects air, water, and soil quality, impacting health and ecosystems. GD participants can discuss causes, effects, and mitigation strategies. Well-structured arguments show understanding of global challenges and problem-solving abilities."},

{q:"Topic: Sustainable Development", a:"Development without harming the environment.", e:"Sustainable development ensures economic growth while protecting resources. In GDs, discussing renewable energy, responsible consumption, and policy suggestions highlights awareness and responsibility. Explaining long-term benefits demonstrates maturity."},

{q:"Topic: Artificial Intelligence Ethics", a:"Responsible use of AI.", e:"AI ethics deals with fairness, transparency, and accountability in automated systems. GD discussions can include bias in AI, privacy concerns, and societal impact. Offering balanced perspectives shows critical thinking and awareness of technological consequences."},

{q:"Topic: Gender Equality", a:"Equal opportunities for all genders.", e:"GD discussions on gender equality cover workplace opportunities, pay gaps, and societal norms. Proposing solutions and acknowledging challenges demonstrates awareness, empathy, and leadership potential."},

{q:"Topic: Startups and Entrepreneurship", a:"Building new businesses.", e:"Entrepreneurship involves innovation, risk-taking, and business planning. In GDs, topics can include funding challenges, market analysis, and startup culture. Sharing examples shows knowledge of current trends and problem-solving skills."},

{q:"Topic: Artificial Intelligence in Healthcare", a:"AI applications for health.", e:"AI can help diagnose diseases, manage patient records, and suggest treatments. GD discussions can focus on benefits, risks, and ethical concerns. Explaining with examples shows understanding of technology's societal impact."},

{q:"Topic: Renewable Energy", a:"Clean energy sources.", e:"Topics include solar, wind, and hydro energy. In GDs, participants can discuss benefits, feasibility, and policies. Using statistics or real-life examples shows research and analytical skills."},

{q:"Topic: Work From Home Challenges", a:"Difficulties in remote work.", e:"Challenges include communication gaps, time management, and team collaboration. GD discussions can propose solutions like tools or strategies. Practical points reflect problem-solving and awareness."},

{q:"Topic: Mental Health in Workplace", a:"Employee well-being.", e:"Stress, burnout, and motivation affect productivity. GD discussions can suggest wellness programs, support systems, and awareness campaigns. Thoughtful explanations show empathy and professional maturity."},

{q:"Topic: Corporate Social Responsibility (CSR)", a:"Company's social impact.", e:"CSR initiatives include education, healthcare, and environmental projects. In GDs, discussing CSR strategies demonstrates understanding of business ethics and societal contribution."},

{q:"Topic: Future of Work", a:"Evolving workplace trends.", e:"Topics include AI automation, hybrid work, and skill development. GD participants should discuss adaptability, challenges, and solutions. Well-reasoned points show foresight and critical thinking."},

{q:"Topic: Digital Transformation", a:"Use of digital tech in business.", e:"Digital transformation involves adopting new technologies for efficiency. GD discussions can cover benefits, challenges, and strategy. Explaining with examples shows knowledge of modern business trends."},

{q:"Topic: Corporate Leadership Styles", a:"Different ways to lead.", e:"Leadership styles include democratic, autocratic, and transformational. GD discussions can evaluate effectiveness in different situations. Understanding these concepts shows awareness of management principles."},

{q:"Topic: Innovation in Education", a:"New methods to teach and learn.", e:"GD discussions can cover online learning, AI tutoring, skill-based programs, and reforms. Offering solutions or ideas shows creativity, knowledge, and problem-solving ability."},

{q:"Topic: Global Economic Trends", a:"International economic patterns.", e:"Topics can include recession, inflation, trade, and market shifts. GD discussions require analysis, examples, and understanding of impacts. Logical reasoning and awareness make points stronger."}
]
};


/* QUIZ DATA */
const quizData = {

coding:[
  {
    q: "Which data structure uses LIFO (Last In First Out)?",
    options: ["Queue", "Stack", "Array", "Linked List"],
    answer: "Stack"
  },
  {
    q: "Which language is primarily used for web page styling?",
    options: ["HTML", "Python", "CSS", "C"],
    answer: "CSS"
  },
  {
    q: "Which keyword is used to define a function in Python?",
    options: ["func", "def", "function", "declare"],
    answer: "def"
  },
  {
    q: "What does HTML stand for?",
    options: [
      "Hyper Trainer Marking Language",
      "Hyper Text Markup Language",
      "High Text Machine Language",
      "Hyper Text Management Language"
    ],
    answer: "Hyper Text Markup Language"
  },
  {
    q: "Which symbol is used for comments in C?",
    options: ["//", "#", "--", "/* */"],
    answer: "//"
  },
  {
    q: "Which of the following is NOT an OOPS concept?",
    options: ["Inheritance", "Encapsulation", "Polymorphism", "Compilation"],
    answer: "Compilation"
  },
  {
    q: "Which SQL command is used to fetch data?",
    options: ["GET", "SELECT", "FETCH", "TAKE"],
    answer: "SELECT"
  },
 {
    q:"Python is?",
    options:["Compiled","Interpreted","Both","None"],
    answer: "Compiled"
 },
  {
    q: "Which operator is used for equality check in JavaScript?",
    options: ["=", "==", "===", "!=="],
    answer: "==="
  },
  {
    q: "Which loop executes at least once?",
    options: ["for loop", "while loop", "do while loop", "foreach loop"],
    answer: "do while loop"
  },
  {
    q: "What is the time complexity of binary search?",
    options: ["O(n)", "O(log n)", "O(n²)", "O(1)"],
    answer: "O(log n)"
  },
  {
    q: "Which is the correct file extension for Python files?",
    options: [".pt", ".pyt", ".py", ".python"],
    answer: ".py"
  },
  {
    q: "Which method is used to print output in Java?",
    options: ["print()", "System.out.println()", "echo()", "cout<<"],
    answer: "System.out.println()"
  },
  {
    q: "Which data type stores true/false values?",
    options: ["int", "bool", "float", "char"],
    answer: "bool"
  },
  {
    q: "Which is used to create a database?",
    options: ["CREATE DATABASE", "MAKE DATABASE", "NEW DB", "INIT DATABASE"],
    answer: "CREATE DATABASE"
  },
  {
    q: "Which CSS property changes text color?",
    options: ["font-color", "color", "text-color", "foreground"],
    answer: "color"
  },
  {
    q: "Which programming language is known as platform independent?",
    options: ["C", "C++", "Java", "Assembly"],
    answer: "Java"
  },
  {
    q: "Who is known as the father of C language?",
    options: ["Guido van Rossum", "James Gosling", "Dennis Ritchie", "Bjarne Stroustrup"],
    answer: "Dennis Ritchie"
  },
  {
    q: "Which of the following is used to connect database in backend?",
    options: ["JDBC", "HTML", "CSS", "Bootstrap"],
    answer: "JDBC"
  },
  {
    q: "Which data structure is used in BFS?",
    options: ["Stack", "Queue", "Tree", "Array"],
    answer: "Queue"
  },
  {
    q: "Which of the following is a relational database?",
    options: ["MongoDB", "Firebase", "MySQL", "Cassandra"],
    answer: "MySQL"
  },
  {
     q:"SQL full form?",
     options:["Structured Query Language","Simple Query Language","Server Query Language","None"],
     answer: "Structured Query Language"
  },

  {
    q: "Which keyword is used for inheritance in Java?",
    options: ["extends", "inherits", "derives", "from"],
    answer: "extends"
  },
  {
    q: "Which of these is a frontend framework?",
    options: ["React", "Django", "Flask", "Node.js"],
    answer: "React"
  },
  {
    q: "What does CSS stand for?",
    options: [
      "Cascading Style Sheets",
      "Creative Style System",
      "Color Styling Sheet",
      "Computer Style Syntax"
    ],
    answer: "Cascading Style Sheets"
  },
  {
    q: "Which keyword is used to stop loop execution?",
    options: ["stop", "exit", "break", "end"],
    answer: "break"
  },
  {
    q: "Which memory stores function call details?",
    options: ["Heap", "Cache", "Stack", "CPU"],
    answer: "Stack"
  },
  {
    q: "A function that calls itself is called?",
    options: ["Loop", "Recursive", "Inline", "Nested"],
    answer: "Recursive"
  },
  {
    q: "Which command deletes a table in SQL?",
    options: ["DELETE TABLE", "REMOVE TABLE", "DROP TABLE", "CLEAR TABLE"],
    answer: "DROP TABLE"
  },
  {
    q: "Which JavaScript method is used to convert string to integer?",
    options: ["parseInt()", "int()", "convert()", "toNumber()"],
    answer: "parseInt()"
  },
  {
    q: "Which of the following is NOT a programming language?",
    options: ["Python", "HTML", "Java", "C++"],
    answer: "HTML"
  },
  {
    q: "Which algorithm is used for sorting efficiently?",
    options: ["Bubble Sort", "Selection Sort", "Quick Sort", "Linear Sort"],
    answer: "Quick Sort"
  },
  {
    q: "Which concept hides internal details?",
    options: ["Abstraction", "Inheritance", "Polymorphism", "Overloading"],
    answer: "Abstraction"
  },
  {
    q: "What is the correct example of framework?",
    options: ["Html", "Django", "Java", "Flask"],
    answer: "Django"
  },
  {
    q: "What does DBMS stand for?",
    options: [
      "Database Managing System",
      "Data Base Management System",
      "Data Based Maintain System",
      "Database Monitoring Service"
    ],
    answer: "Data Base Management System"
  },
  
],

aptitude:[
 {q:"What is Aptitude in placements?",options:["Subject Knowledge","Natural Ability to Solve Problems","Communication Skill","Programming Skill"],correct:1},
{q:"Which topic checks business understanding?",options:["Profit & Loss","Shapes","GK","Chemistry"],correct:0},
{q:"Why is Percentage important?",options:["Used in daily life decisions","Only for exams","Only for shops","Not important"],correct:0},
{q:"Difference between aptitude & reasoning?",options:["Both same","Aptitude = Maths + Logic, Reasoning = Logical Thinking","Reasoning = Only Maths","No difference"],correct:1},
{q:"Data Interpretation is used in?",options:["Cooking","Business Reports & Analytics","Dancing","Driving"],correct:1},
{q:"Reason companies avoid only marks?",options:["Marks don't show thinking ability","Marks are everything","Marks show talent fully","They don’t check thinking"],correct:0},
{q:"If salary increases from 20k to 25k, what skill required?",options:["Coding","Percentage","Chemistry","History"],correct:1},
{q:"Time-Speed-Distance helps in?",options:["Travelling decisions","Sleeping schedule","Food","Nothing"],correct:0},
{q:"Logical puzzles improve?",options:["Humor","Brain processing power","Typing","Drawing"],correct:1},
{q:"Companies want aptitude because employee must?",options:["Work without thinking","Take quick right decisions","Just follow orders","Only code"],correct:1},
{q:"Data Interpretation mainly requires?",options:["Guessing","Observation & logic","Speaking","Acting"],correct:1},
{q:"Which improves exam time management?",options:["Watching movies","Aptitude solving","Sleeping","Gaming"],correct:1},
  {
    q: "If the cost price of a pen is ₹50 and it is sold for ₹75, what is the profit percentage?",
    options: ["25%", "30%", "40%", "50%"],
    answer: "50%"
  },
  {
    q: "What will be 25% of 480?",
    options: ["90", "100", "110", "120"],
    answer: "120"
  },
  {
    q: "A train 200m long crosses a pole in 10 seconds. What is its speed?",
    options: ["10 m/s", "20 m/s", "25 m/s", "30 m/s"],
    answer: "20 m/s"
  },
  {
    q: "What is the next number in the sequence: 2, 6, 12, 20, ?",
    options: ["28", "30", "32", "36"],
    answer: "30"
  },
  {
    q: "The average of 10, 20, 30, 40 and 50 is?",
    options: ["20", "25", "30", "35"],
    answer: "30"
  },
  {
    q: "If a person covers 60 km in 2 hours, what is his speed?",
    options: ["20 km/hr", "25 km/hr", "30 km/hr", "35 km/hr"],
    answer: "30 km/hr"
  },
  {
    q: "If 12 workers finish a work in 8 days, in how many days will 6 workers finish it?",
    options: ["8 days", "12 days", "14 days", "16 days"],
    answer: "16 days"
  },
  {
    q: "What is 15% of 200?",
    options: ["20", "25", "30", "35"],
    answer: "30"
  },
  {
    q: "If x = 10, what is the value of 3x + 5?",
    options: ["25", "30", "35", "40"],
    answer: "35"
  },
  {
    q: "If 20% of a number is 40, what is the number?",
    options: ["100", "150", "180", "200"],
    answer: "200"
  },
  {
    q: "The simple interest on ₹1000 at 10% per annum for 2 years is?",
    options: ["₹100", "₹150", "₹180", "₹200"],
    answer: "₹200"
  },
  {
    q: "A man walks 4 km north and then 3 km east. How far is he from the starting point?",
    options: ["5 km", "6 km", "7 km", "4 km"],
    answer: "5 km"
  },
  {
    q: "If 8 pencils cost ₹40, what is the cost of 1 pencil?",
    options: ["₹3", "₹4", "₹5", "₹6"],
    answer: "₹5"
  },
  {
    q: "What is the HCF of 18 and 24?",
    options: ["2", "3", "6", "12"],
    answer: "6"
  },
  {
    q: "Convert 3/4 into percentage:",
    options: ["50%", "60%", "70%", "75%"],
    answer: "75%"
  },
  {
    q: "A car travels 240 km in 4 hours. What is the speed?",
    options: ["40 km/hr", "50 km/hr", "60 km/hr", "70 km/hr"],
    answer: "60 km/hr"
  },
  {
    q: "The next number in series: 11, 22, 44, 88, ?",
    options: ["100", "110", "130", "176"],
    answer: "176"
  },
  {
    q: "If the perimeter of a square is 40 cm, what is the side length?",
    options: ["5 cm", "8 cm", "10 cm", "12 cm"],
    answer: "10 cm"
  },
  {
    q: "What is 3/5 of 200?",
    options: ["80", "100", "110", "120"],
    answer: "120"
  },
  {
    q: "If 5 notebooks cost ₹75, what is the cost of 1 notebook?",
    options: ["₹10", "₹12", "₹15", "₹20"],
    answer: "₹15"
  },
  {
    q: "Find the missing number: 7, 14, 21, 28, ?",
    options: ["30", "32", "35", "40"],
    answer: "35"
  },
  {
    q: "The sum of angles in a triangle is?",
    options: ["90°", "120°", "150°", "180°"],
    answer: "180°"
  },
  {
    q: "What is the least even prime number?",
    options: ["1", "2", "3", "5"],
    answer: "2"
  },
  {
    q: "If CP is ₹800 and profit is 25%, SP is?",
    options: ["₹900", "₹950", "₹1000", "₹1200"],
    answer: "₹1000"
  },
  {
    q: "What is the reciprocal of 5/9?",
    options: ["5/9", "9/5", "1/5", "1/9"],
    answer: "9/5"
  },
  {
    q: "The average of 5, 15 and 25 is?",
    options: ["10", "12", "15", "20"],
    answer: "15"
  },
  {
    q: "If 10 workers complete a task in 5 days, how many days for 5 workers?",
    options: ["5", "8", "10", "15"],
    answer: "10"
  },
{q:"Why ratio & proportion are useful?",options:["In recipes, salary splits, comparisons","Only exams","Nothing","Only maths class"],correct:0},
],

reasoning:[
 {
    question: "1. What is reasoning and why is it important in competitive exams?",
    options: [
      "It tests physical strength only",
      "It helps measure logical thinking and problem-solving ability",
      "It is used only in interviews",
      "It is used only for memory testing"
    ],
    answer: "It helps measure logical thinking and problem-solving ability"
  },
  {
    question: "2. If A is the brother of B, B is the sister of C, and C is the father of D, what is A to D?",
    options: ["Uncle", "Father", "Brother", "Cousin"],
    answer: "Uncle"
  },
  {
    question: "3. Find the odd one out: Apple, Mango, Banana, Carrot",
    options: ["Apple", "Mango", "Banana", "Carrot"],
    answer: "Carrot"
  },
  {
    question: "4. Which direction will a person face if they turn right from East and then left?",
    options: ["North", "South", "East", "West"],
    answer: "South"
  },
  {
    question: "5. Complete the series: A, C, E, G, ?",
    options: ["H", "I", "J", "K"],
    answer: "I"
  },
  {
    question: "6. If CAT is coded as DBU, how will DOG be coded?",
    options: ["EPH", "EOG", "FPG", "EOF"],
    answer: "EPH"
  },
  {
    question: "7. What does logical reasoning mainly test?",
    options: ["Guessing ability", "Logical and analytical skills", "Speaking skills", "Memory only"],
    answer: "Logical and analytical skills"
  },
  {
    question: "8. If P is mother of Q and Q is father of R, what is P to R?",
    options: ["Mother", "Grandmother", "Aunt", "Sister"],
    answer: "Grandmother"
  },
  {
    question: "9. Choose the correct analogy: Bird : Nest :: Lion : ?",
    options: ["Cave", "Forest", "Zoo", "Den"],
    answer: "Den"
  },
  {
    question: "10. Which one does not belong to the group? Circle, Square, Triangle, Cube",
    options: ["Circle", "Square", "Triangle", "Cube"],
    answer: "Cube"
  },
  {
    question: "11. A person walks 5 km North, then 3 km East. Which direction is he from starting point?",
    options: ["North-East", "South-East", "North-West", "West"],
    answer: "North-East"
  },
  {
    question: "12. If ALL = BMM, then YES will be coded as?",
    options: ["ZFT", "ZFR", "ZES", "ZFS"],
    answer: "ZFT"
  },
  {
    question: "13. Which type of questions measure decision-making ability?",
    options: [
      "Blood relation questions",
      "Direction sense questions",
      "Logical assumption questions",
      "Alphabet series questions"
    ],
    answer: "Logical assumption questions"
  },
  {
    question: "14. In a row of students, A is 7th from left and 10th from right. How many students are there?",
    options: ["15", "16", "17", "18"],
    answer: "16"
  },
  {
    question: "15. Find the odd one out: Pen, Pencil, Eraser, Paper, Computer",
    options: ["Pen", "Pencil", "Paper", "Computer"],
    answer: "Computer"
  },
  {
    question: "16. If 'FLOWER' is written as 'FKPVFQ', what is the pattern?",
    options: [
      "Each letter +2",
      "Each letter -2",
      "Alternate +1 and -1",
      "Reverse alphabet rule"
    ],
    answer: "Each letter -1"
  },
  {
    question: "17. Syllogism tests mainly help in understanding what?",
    options: [
      "Verbal speaking",
      "Logical conclusion from given statements",
      "Mathematical solving",
      "Memory strength"
    ],
    answer: "Logical conclusion from given statements"
  },
  {
    question: "18. If all squares are rectangles and all rectangles are shapes, then what is true?",
    options: [
      "All shapes are squares",
      "All squares are shapes",
      "No square is shape",
      "Square and shapes are unrelated"
    ],
    answer: "All squares are shapes"
  },
  {
    question: "19. Which skill improves the most through reasoning practice?",
    options: [
      "Physical skill",
      "Emotional strength",
      "Logical thinking and accuracy",
      "Handwriting"
    ],
    answer: "Logical thinking and accuracy"
  },
  {
    question: "20. Why do companies test reasoning in interviews?",
    options: [
      "To check English fluency",
      "To check academic marks",
      "To test real-time problem solving",
      "To test physical energy"
    ],
    answer: "To test real-time problem solving"
  }, 
  {
    question: "21. Which of the following best defines Non-Verbal Reasoning?",
    options: [
      "Reasoning based on spoken language",
      "Reasoning without using numbers",
      "Reasoning based on figures, patterns, and visuals",
      "Reasoning based only on memory"
    ],
    answer: "Reasoning based on figures, patterns, and visuals"
  },
  {
    question: "22. If TODAY is coded as UPEBZ, how is INDIA coded?",
    options: ["JOEJB", "JOEIB", "HMCJZ", "JNEJB"],
    answer: "JOEJB"
  },
  {
    question: "23. Find the odd one out: Dog, Tiger, Lion, Cow",
    options: ["Dog", "Tiger", "Lion", "Cow"],
    answer: "Dog"
  },
  {
    question: "24. In a certain language, SCHOOL is written as OCHSLO. How is COLLEGE written?",
    options: ["OCLLEGE", "ELLOGEC", "OCLEGEL", "EGCOLLO"],
    answer: "OCLEGEL"
  },
  {
    question: "25. Which of these topics mainly checks common-sense decision ability?",
    options: [
      "Blood Relations",
      "Logical Assumptions",
      "Alphabet Series",
      "Direction Sense"
    ],
    answer: "Logical Assumptions"
  },
  {
    question: "26. A person travels 4 km North, then 4 km West, then 4 km South. Where is he from the starting point?",
    options: ["Back to start", "4 km East", "4 km West", "4 km North"],
    answer: "4 km West"
  },
  {
    question: "27. Find the analogy: Hand : Glove :: Foot : ?",
    options: ["Shoe", "Socks", "Leg", "Boot"],
    answer: "Shoe"
  },
  {
    question: "28. Which reasoning topic helps in solving corporate case studies?",
    options: [
      "Alphabet Reasoning",
      "Syllogism",
      "Coding-Decoding",
      "Statement and Conclusion"
    ],
    answer: "Statement and Conclusion"
  },
  {
    question: "29. Which of the following improves by practicing reasoning regularly?",
    options: [
      "Only memory",
      "Only vocabulary",
      "Logical thinking and accuracy",
      "Physical stamina"
    ],
    answer: "Logical thinking and accuracy"
  },
  {
    question: "30. Why do exams include reasoning questions?",
    options: [
      "To increase exam length",
      "To judge logical ability and decision-making",
      "To confuse students",
      "To check handwriting"
    ],
    answer: "To judge logical ability and decision-making"
  },
{
  question: "31. Which reasoning topic mainly helps in real-life judgment and decision making?",
  options: [
    "Coding-Decoding",
    "Blood Relation",
    "Syllogism",
    "Statement–Assumption"
  ],
  answer: "Statement–Assumption"
},
{
  question: "32. If CAT = DBU, DOG = EPH then FISH = ?",
  options: ["GJTI", "GJTI", "GJSI", "GJUI"],
  answer: "GJTI"
},
{
  question: "33. In a class, Riya is 10th from the top and 15th from the bottom. How many students are in the class?",
  options: ["23", "24", "25", "26"],
  answer: "24"
},
{
  question: "34. Which topic checks whether a conclusion logically follows from given facts?",
  options: [
    "Direction Sense",
    "Blood Relations",
    "Syllogism",
    "Number Series"
  ],
  answer: "Syllogism"
},
{
  question: "35. Find the odd one out: Circle, Square, Triangle, Cube",
  options: ["Circle", "Square", "Triangle", "Cube"],
  answer: "Cube"
},
{
  question: "36. Which reasoning topic improves quick thinking during interviews and GD?",
  options: [
    "Logical Reasoning",
    "Mathematics",
    "General Knowledge",
    "Vocabulary"
  ],
  answer: "Logical Reasoning"
},
{
  question: "37. If NORTH is coded as MROQS, how is SOUTH coded?",
  options: ["QNRGT", "QNRHT", "QNRFT", "QNRGS"],
  answer: "QNRGS"
},
{
  question: "38. Which reasoning area deals with directions like left, right, east, west?",
  options: [
    "Blood Relation",
    "Direction Sense",
    "Non-Verbal Reasoning",
    "Alphabet Test"
  ],
  answer: "Direction Sense"
},
{
  question: "39. Reasoning in exams mainly tests:",
  options: [
    "Grammar knowledge",
    "Physical ability",
    "Logical and analytical skills",
    "Programming skills"
  ],
  answer: "Logical and analytical skills"
},
{
  question: "40. Why is reasoning important in placements?",
  options: [
    "It helps only in exams",
    "It improves logical problem solving in real work",
    "It is just formality",
    "It is used only by engineers"
  ],
  answer: "It improves logical problem solving in real work"
}
],

interview:[
  {
question: "1. What is the primary purpose of an interview in placements?",
options: [
"To check coding only",
"To judge personality, skills and suitability",
"To see confidence only",
"To check English only"
],
answer: "To judge personality, skills and suitability"
},
{
question: "2. What should be your first response when interviewer says 'Tell me about yourself'?",
options: [
"Start with family background",
"Start with school memories",
"Start with professional/academic profile",
"Start with hobbies"
],
answer: "Start with professional/academic profile"
},
{
question: "3. Which of the following creates the FIRST impression in interview?",
options: [
"Resume",
"Handshake",
"Answer accuracy",
"Marks"
],
answer: "Resume"
},
{
question: "4. What should you avoid while answering questions?",
options: [
"Clear explanation",
"Confidence",
"Honesty",
"Over exaggeration and lying"
],
answer: "Over exaggeration and lying"
},
{
question: "5. What is HR round mainly for?",
options: [
"Technical skills",
"Behavior, attitude and communication",
"Coding skills",
"Mathematical skills"
],
answer: "Behavior, attitude and communication"
},
{
question: "6. Which dress code is ideal for interviews?",
options: [
"Casual wear",
"Party wear",
"Formal wear",
"Sports wear"
],
answer: "Formal wear"
},
{
question: "7. What should you do if you don’t know an answer?",
options: [
"Guess randomly",
"Stay silent",
"Accept calmly and explain willingness to learn",
"Change topic"
],
answer: "Accept calmly and explain willingness to learn"
},
{
question: "8. What is the best tone while answering?",
options: [
"Aggressive",
"Too soft",
"Confident and polite",
"Loud"
],
answer: "Confident and polite"
},
{
question: "9. Which skill is MOST evaluated?",
options: [
"Communication",
"Attitude",
"Problem solving",
"All of the above"
],
answer: "All of the above"
},
{
question: "10. Which round checks technical knowledge?",
options: [
"HR round",
"Managerial round",
"Technical round",
"Final round only"
],
answer: "Technical round"
},
{
question: "11. What should be the ideal resume length for freshers?",
options: ["1 page", "3 pages", "5 pages", "No limit"],
answer: "1 page"
},
{
question: "12. What should you do before attending interview?",
options: [
"Nothing",
"Memorize answers only",
"Research about company and role",
"Ask friends only"
],
answer: "Research about company and role"
},
{
question: "13. Which is most important in introduction?",
options: [
"Family details",
"Marks only",
"Skills + Strength + Career goal",
"Hobbies only"
],
answer: "Skills + Strength + Career goal"
},
{
question: "14. What is STAR method used for?",
options: [
"Technical solving",
"Story telling",
"Answering behavioral questions",
"Resume formatting"
],
answer: "Answering behavioral questions"
},
{
question: "15. What shows professionalism?",
options: [
"Arriving late",
"Not maintaining eye contact",
"Proper posture and discipline",
"Arguing with interviewer"
],
answer: "Proper posture and discipline"
},
{
question: "16. What does Group Discussion mainly test?",
options: [
"Shouting ability",
"English fluency only",
"Leadership, clarity and teamwork",
"Memory"
],
answer: "Leadership, clarity and teamwork"
},
{
question: "17. What is the best way to end an interview?",
options: [
"Leave silently",
"Say thank you confidently",
"Argue last point",
"Ask personal questions"
],
answer: "Say thank you confidently"
},
{
question: "18. What is most important in HR answers?",
options: [
"Lengthy answers",
"Truthfulness and clarity",
"Fancy English",
"Jokes"
],
answer: "Truthfulness and clarity"
},
{
question: "19. What should you NOT mention as weakness?",
options: [
"Overthinking sometimes",
"Public speaking fear",
"Being too honest",
"Negative attitude or laziness"
],
answer: "Negative attitude or laziness"
},
{
question: "20. If interviewer asks salary expectation?",
options: [
"Demand highest amount",
"Say no idea",
"Ask for company standard range",
"Refuse to answer"
],
answer: "Ask for company standard range"
},
{
question: "21. Eye contact in interview should be?",
options: [
"None",
"Staring continuously",
"Balanced and natural",
"Looking down"
],
answer: "Balanced and natural"
},
{
question: "22. What should your body language show?",
options: [
"Nervousness",
"Arrogance",
"Confidence and calmness",
"Carelessness"
],
answer: "Confidence and calmness"
},
{
question: "23. Why do interviewers ask 'Why this company?'",
options: [
"To test luck",
"Time pass",
"To test interest and motivation",
"To confuse candidate"
],
answer: "To test interest and motivation"
},
{
question: "24. What should be your tone while disagreeing?",
options: [
"Rude",
"Aggressive",
"Respectful and logical",
"Silent"
],
answer: "Respectful and logical"
},
{
question: "25. What must a fresher highlight the most?",
options: [
"Past jobs",
"Family background",
"Skills, projects, internships",
"Friends support"
],
answer: "Skills, projects, internships"
},
{
question: "26. What should you do if interviewer interrupts?",
options: [
"Keep talking",
"Argue",
"Listen patiently and respond",
"Stop interview"
],
answer: "Listen patiently and respond"
},
{
question: "27. When asked 'Where do you see yourself in 5 years?'",
options: [
"Say CEO",
"Say no idea",
"Show growth mindset and learning goal",
"Joke"
],
answer: "Show growth mindset and learning goal"
},
{
question: "28. What should be honest always?",
options: [
"Marks",
"Skills",
"Experience",
"All of these"
],
answer: "All of these"
},
{
question: "29. What is most important in virtual interview?",
options: [
"Noise background",
"Unstable internet",
"Good lighting + internet + posture",
"Camera off"
],
answer: "Good lighting + internet + posture"
},
{
question: "30. What helps reduce nervousness?",
options: [
"Panicking",
"No preparation",
"Practicing mock interviews",
"Sleeping during interview"
],
answer: "Practicing mock interviews"
},
{
question: "31. What should you highlight when asked strengths?",
options: [
"Negative habits",
"Non relevant things",
"Skills relevant to job",
"Random topics"
],
answer: "Skills relevant to job"
},
{
question: "32. Why do companies ask behavioral questions?",
options: [
"Fun only",
"Time pass",
"To test real-life handling ability",
"To check marks"
],
answer: "To test real-life handling ability"
},
{
question: "33. What should be avoided in resume?",
options: [
"Achievements",
"Accurate skills",
"Fake information",
"Education details"
],
answer: "Fake information"
},
{
question: "34. Which of these is GOOD to ask in interview?",
options: [
"Salary first",
"Personal life questions",
"Growth opportunities and role details",
"Office gossip"
],
answer: "Growth opportunities and role details"
},
{
question: "35. What shows lack of confidence?",
options: [
"Straight sitting",
"Clear voice",
"Continuous shaking and fumbling",
"Calm tone"
],
answer: "Continuous shaking and fumbling"
},
{
question: "36. What is the best attitude in interviews?",
options: [
"Over confident",
"Fearful",
"Humble and confident",
"Casual"
],
answer: "Humble and confident"
},
{
question: "37. What does interviewer check in communication?",
options: [
"Grammar only",
"Accent only",
"Clarity, confidence and understanding",
"Speed only"
],
answer: "Clarity, confidence and understanding"
},
{
question: "38. What should you do after interview?",
options: [
"Forget it",
"Complain",
"Send a thank you message/email",
"Call repeatedly"
],
answer: "Send a thank you message/email"
},
{
question: "39. Which is MOST important quality?",
options: [
"Arrogance",
"Learning attitude",
"Laziness",
"Ego"
],
answer: "Learning attitude"
},
{
question: "40. Why are interviews important?",
options: [
"Just formality",
"Only for marks",
"They help select best suitable candidates",
"Time pass for companies"
],
answer: "They help select best suitable candidates"
}
],

gd:[
  {
question: "1. What is the main purpose of Group Discussion in placements?",
options: [
"To fight and win",
"To judge communication and teamwork",
"To memorize theory",
"To check coding"
],
answer: "To judge communication and teamwork"
},
{
question: "2. GD mainly evaluates?",
options: [
"Voice loudness",
"Marks and CGPA",
"Communication, confidence, thinking ability",
"Dress only"
],
answer: "Communication, confidence, thinking ability"
},
{
question: "3. What is the ideal way to start a GD?",
options: [
"Shout to dominate",
"Stay silent",
"Give a structured opening with clear understanding",
"Attack others' opinions"
],
answer: "Give a structured opening with clear understanding"
},
{
question: "4. What is MOST important in GD?",
options: [
"Talking continuously",
"Listening and speaking logically",
"Speaking English fast",
"Arguing"
],
answer: "Listening and speaking logically"
},
{
question: "5. What should you do if others are not allowing you to speak?",
options: [
"Shout louder",
"Get angry",
"Wait for pause and politely enter",
"Leave GD"
],
answer: "Wait for pause and politely enter"
},
{
question: "6. What should NOT be done in GD?",
options: [
"Respecting views",
"Maintaining calm tone",
"Personal attacks",
"Logical arguments"
],
answer: "Personal attacks"
},
{
question: "7. Which of the following helps to score better in GD?",
options: [
"Reading newspapers",
"Staying silent",
"Memorizing answers",
"Copying others"
],
answer: "Reading newspapers"
},
{
question: "8. What shows leadership in GD?",
options: [
"Dominating",
"Helping group reach conclusion",
"Shouting",
"Interrupting everyone"
],
answer: "Helping group reach conclusion"
},
{
question: "9. What is the best posture in GD?",
options: [
"Sleeping posture",
"Arms folded angrily",
"Straight, confident and active",
"Looking down"
],
answer: "Straight, confident and active"
},
{
question: "10. If topic is unknown, what should you do?",
options: [
"Stay silent completely",
"Give wrong facts confidently",
"Listen first then contribute logically",
"Leave GD"
],
answer: "Listen first then contribute logically"
},
{
question: "11. What is most valued in GD?",
options: [
"Facts and clarity",
"Background music",
"Jokes",
"Arguments only"
],
answer: "Facts and clarity"
},
{
question: "12. Good participant should be?",
options: [
"Silent",
"Aggressive",
"Balanced speaker & listener",
"Always arguing"
],
answer: "Balanced speaker & listener"
},
{
question: "13. What is the role of examples in GD?",
options: [
"Confuse others",
"Make topic funny",
"Support and strengthen points",
"Time pass"
],
answer: "Support and strengthen points"
},
{
question: "14. What should be avoided completely?",
options: [
"Eye contact",
"Confidence",
"Logical reasoning",
"Rude behavior"
],
answer: "Rude behavior"
},
{
question: "15. What should body language show?",
options: [
"Fear",
"Ego",
"Confidence and openness",
"Aggression"
],
answer: "Confidence and openness"
},
{
question: "16. What is MOST dangerous mistake in GD?",
options: [
"Speaking clearly",
"Disagreeing politely",
"Wrong facts & rude tone",
"Sharing ideas"
],
answer: "Wrong facts & rude tone"
},
{
question: "17. What helps to contribute better?",
options: [
"Talking nonstop",
"Only disagreeing",
"Listening and analysing first",
"Copying others"
],
answer: "Listening and analysing first"
},
{
question: "18. What is the ideal speech style in GD?",
options: [
"Fast and unclear",
"Slow and boring",
"Loud shouting",
"Clear, confident and meaningful"
],
answer: "Clear, confident and meaningful"
},
{
question: "19. What do evaluators observe the MOST?",
options: [
"Clothes only",
"English accent only",
"Overall thinking + communication + attitude",
"Hair style"
],
answer: "Overall thinking + communication + attitude"
},
{
question: "20. What should you do if GD becomes heated?",
options: [
"Fight",
"Enjoy chaos",
"Calm everyone and bring discussion back",
"Stay silent"
],
answer: "Calm everyone and bring discussion back"
},
{
question: "21. A good GD participant is?",
options: [
"Aggressive",
"Silent watcher",
"Supportive and logical speaker",
"Argument king"
],
answer: "Supportive and logical speaker"
},
{
question: "22. What should opening speaker do?",
options: [
"Give conclusion",
"Talk randomly",
"Set direction and define topic",
"Start argument"
],
answer: "Set direction and define topic"
},
{
question: "23. What is important in conclusion?",
options: [
"Fight summary",
"Personal opinions only",
"Summarize key points logically",
"Shout loudly"
],
answer: "Summarize key points logically"
},
{
question: "24. What helps improve GD performance?",
options: [
"Watching movies",
"Random talking",
"Regular practice and reading",
"Not participating"
],
answer: "Regular practice and reading"
},
{
question: "25. Which attitude is best in GD?",
options: [
"Egoistic",
"Aggressive",
"Respectful and confident",
"Fearful"
],
answer: "Respectful and confident"
},
{
question: "26. Why do companies conduct GD?",
options: [
"Time pass",
"For fun",
"To check real-world communication skills",
"To reject students"
],
answer: "To check real-world communication skills"
},
{
question: "27. What should you maintain throughout GD?",
options: [
"Anger",
"Silence",
"Positive & professional attitude",
"Ego"
],
answer: "Positive & professional attitude"
},
{
question: "28. Which of these weakens your point?",
options: [
"Facts",
"Proper examples",
"Emotional shouting",
"Logic"
],
answer: "Emotional shouting"
},
{
question: "29. What must be avoided while interrupting?",
options: [
"Polite entry",
"Using excuse me",
"Respectful timing",
"Cutting mid-sentence aggressively"
],
answer: "Cutting mid-sentence aggressively"
},
{
question: "30. What should be done if topic is controversial?",
options: [
"Fight",
"Take extreme sides",
"Speak balanced and mature",
"Stay rude"
],
answer: "Speak balanced and mature"
},
{
question: "31. What shows leadership quality?",
options: [
"Insulting others",
"Taking control forcefully",
"Helping group reach meaningful decision",
"Talking most"
],
answer: "Helping group reach meaningful decision"
},
{
question: "32. Which skill is MOST checked?",
options: [
"Memory",
"Drawing",
"Critical thinking and clarity",
"Dancing"
],
answer: "Critical thinking and clarity"
},
{
question: "33. What should hand movement be?",
options: [
"Too much waving",
"No movement at all",
"Natural and controlled",
"Aggressive pointing"
],
answer: "Natural and controlled"
},
{
question: "34. What helps you stand out?",
options: [
"Shouting",
"Repeating others",
"Unique logical inputs",
"Staying silent"
],
answer: "Unique logical inputs"
},
{
question: "35. What happens if you speak too much?",
options: [
"Positive impression",
"Shows domination",
"Wastes time and reduces impact",
"Best leadership"
],
answer: "Wastes time and reduces impact"
},
{
question: "36. What is best use of data or facts?",
options: [
"To insult others",
"To confuse group",
"To support points strongly",
"Not needed"
],
answer: "To support points strongly"
},
{
question: "37. What should be your reaction if someone disagrees?",
options: [
"Fight back",
"Ignore",
"Respectfully counter with logic",
"Get angry"
],
answer: "Respectfully counter with logic"
},
{
question: "38. GD gives companies idea about?",
options: [
"Marks only",
"Family background",
"Professional behavior and mindset",
"Hobbies only"
],
answer: "Professional behavior and mindset"
},
{
question: "39. When is silence acceptable?",
options: [
"Full GD",
"Never speak",
"When thinking / giving others chance",
"When sleeping"
],
answer: "When thinking / giving others chance"
},
{
question: "40. What is the final success key in GD?",
options: [
"Loud voice",
"Aggression",
"Confidence + Clarity + Respect",
"Luck"
],
answer: "Confidence + Clarity + Respect"
}
]
};


/* UI ELEMENTS */
const topicBox = document.getElementById("topicBox");
const practiceSection = document.getElementById("practiceSection");
const quizSection = document.getElementById("quizSection");

const practiceContainer = document.getElementById("practiceContainer");
const quizForm = document.getElementById("quizForm");
const quizResult = document.getElementById("quizResult");
const submitQuiz = document.getElementById("submitQuiz");


/* MODE */
document.getElementById("modePractice").onclick = () => {
 topicBox.classList.remove("hidden");
 practiceSection.classList.remove("hidden");
 quizSection.classList.add("hidden");
};

document.getElementById("modeQuiz").onclick = () => {
 topicBox.classList.remove("hidden");
 quizSection.classList.remove("hidden");
 practiceSection.classList.add("hidden");
};


/* TOPIC SELECT */
document.querySelectorAll(".topicBtn").forEach(btn=>{
 btn.addEventListener("click",()=>{
 let topic = btn.dataset.topic;
 renderPractice(topic);
 startQuiz(topic);
 });
});


/* PRACTICE */
function renderPractice(topic){

 practiceContainer.innerHTML = "";

 if(!practiceData[topic] || practiceData[topic].length===0){
  practiceContainer.innerHTML=
 `<div class='p-4 bg-red-200 text-red-700 rounded'>❌ No Practice Questions</div>`;
  return;
 }

 practiceData[topic].forEach((x,i)=>{
  let box=document.createElement("div");
  box.className="qaBox";

  box.innerHTML=
 `<b>${i+1}. ${x.q}</b>
 <br>
 <button class='mt-2 px-3 py-1 bg-blue-500 text-white rounded'>Show Answer</button>
 <div class='ans mt-2'><b>Answer:</b> ${x.a}</div>`;

 let ans=box.querySelector(".ans");
 let btn=box.querySelector("button");
 let explanation = x.e ? x.e.replace(/\n/g, "<br>") : "";
    ans.innerHTML = `<b>Answer:</b> ${x.a}<br>${explanation}`;
 btn.onclick=()=> ans.style.display = ans.style.display==="block"?"none":"block";

 practiceContainer.appendChild(box);
 });
}


/* QUIZ */
let activeQuiz=[];

function startQuiz(topic){

 quizForm.innerHTML="";

 if(!quizData[topic] || quizData[topic].length===0){
  quizForm.innerHTML=
 `<div class='p-4 bg-red-200 text-red-700 rounded'>❌ Quiz Exists But No Questions</div>`;
  submitQuiz.classList.add("hidden");
  return;
 }

 activeQuiz = quizData[topic];

 activeQuiz.forEach((q,i)=>{

 let opts = q.options.map(o=>`
 <label class='block cursor-pointer'>
 <input type='radio' name='q${i}' value='${o}'> ${o}
 </label>
 `).join("");

 quizForm.innerHTML +=
 `<div class='qaBox'>
  <b>Q${i+1}. ${q.q || q.question}</b>
  ${opts}
 </div>`;
 });

 submitQuiz.classList.remove("hidden");
}


/* SUBMIT RESULT */
submitQuiz.onclick = () => {

 let score = 0, attempted = 0;

 activeQuiz.forEach((q, i) => {
    let ans = document.querySelector(`input[name='q${i}']:checked`);

    if (ans) {
        attempted++;
        if (ans.value === q.answer) score++;
    }

    // ==== Highlighting Logic ====
    let options = document.querySelectorAll(`input[name='q${i}']`);

    options.forEach(opt => {
        let parent = opt.parentElement;

        parent.classList.remove("bg-green-200","bg-red-200","border","border-green-600","border-red-600");

        // correct answer => GREEN
        if (opt.value === q.answer) {
            parent.classList.add("bg-green-200","border","border-green-600");
        }

        // selected wrong answer => RED
        if (ans && opt === ans && opt.value !== q.answer) {
            parent.classList.add("bg-red-200","border","border-red-600");
        }

        opt.disabled = true; // lock after submit
    });
 });

 let wrong = activeQuiz.length - score;
 let notAttempt = activeQuiz.length - attempted;

 document.getElementById("correctCount").innerText = score;
 document.getElementById("wrongCount").innerText = wrong;
 document.getElementById("notAttempt").innerText = notAttempt;

 let emoji = "🙂";
 if (score <= 1) emoji = "😢";
 else if (score <= 3) emoji = "🙂";
 else emoji = "🔥";

 document.getElementById("emojiResult").innerText = emoji;

 quizResult.classList.remove("hidden");

 saveHistory(score);
};


/* HISTORY PANEL */
const openHistory=document.getElementById("openHistory");
const closeHistory=document.getElementById("closeHistory");
const historyPanel=document.getElementById("historyPanel");

openHistory.onclick=()=>{
 historyPanel.classList.remove("hidden");
 showHistory();
};

closeHistory.onclick=()=>{
 historyPanel.classList.add("hidden");
};


/* SAVE HISTORY */
function saveHistory(score){
 let history=JSON.parse(localStorage.getItem("quizHistory")||"[]");

 history.push({
 score:score,
 total:activeQuiz.length,
 time:new Date().toLocaleString()
 });

 localStorage.setItem("quizHistory",JSON.stringify(history));
}


/* SHOW HISTORY */
function showHistory(){

 let box=document.getElementById("historyList");
 let history=JSON.parse(localStorage.getItem("quizHistory")||"[]");

 if(history.length===0){
 box.innerHTML="No previous attempts yet...";
 return;
 }

 box.innerHTML = history.map((h,i)=>`
 <div class='p-2 border rounded mb-2'>
 Attempt ${i+1} → Score: ${h.score}/${h.total}<br>
 📅 ${h.time}
 </div>
 `).join("");
}
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".deleteAttempt").forEach(btn => {
    btn.addEventListener("click", async () => {
      const attemptId = btn.getAttribute("data-id");

      if (!confirm("Are you sure you want to delete this attempt?")) return;

      try {
        const response = await fetch("/delete-attempt", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ id: attemptId })
        });

        const data = await response.json();
        if (data.success) {
          // Remove attempt from DOM
          btn.closest("div").remove();
        } else {
          alert("Failed to delete attempt.");
        }
      } catch (err) {
        console.error(err);
        alert("Error deleting attempt.");
      }
    });
  });
});
/* ================= COURSES BUTTON HANDLING ================= */
const coursesSection = document.getElementById("coursesSection");
const courseButtonsBox = document.getElementById("courseButtons");
const videoListBox = document.getElementById("videoList");

document.querySelectorAll(".topicBtn").forEach(btn => {
  btn.addEventListener("click", () => {
    const topic = btn.dataset.topic;

    // Hide other sections
    document.getElementById("practiceSection").classList.add("hidden");
    document.getElementById("quizSection").classList.add("hidden");

    if (topic === "courses") {
      coursesSection.classList.remove("hidden");
      loadCourses();
    }
  });
});

/* ================= LOAD COURSES ================= */
function loadCourses() {
  courseButtonsBox.innerHTML = "";
  videoListBox.innerHTML = "<p class='text-gray-500'>Select a course to see videos</p>";

  Object.keys(coursesData).forEach(course => {
    const btn = document.createElement("button");
    btn.className = "topicBtn bg-blue-600";
    btn.textContent = course.toUpperCase();

    btn.onclick = () => loadVideos(course);
    courseButtonsBox.appendChild(btn);
  });
}

/* ================= LOAD VIDEOS ================= */
function loadVideos(course) {
  videoListBox.innerHTML = "";

  coursesData[course].forEach(video => {
    const div = document.createElement("div");
    div.className = "bg-gray-50 p-3 rounded-lg shadow hover:bg-blue-50 transition cursor-pointer";
    div.innerHTML = `<strong>▶ ${video.title}</strong>`;

    div.onclick = () => window.open(video.link, "_blank");
    videoListBox.appendChild(div);
  });
}
