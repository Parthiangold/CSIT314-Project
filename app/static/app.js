const defaultJobs = [
  {
    title: "Junior Software Developer",
    company: "Tech Solutions Australia",
    description: "Build web applications using JavaScript, React, APIs, and database integration.",
    education: "Bachelor Degree",
    skills: "JavaScript, React, SQL",
    experience: 1,
    mode: "Hybrid",
    location: "Sydney, NSW"
  },
  {
    title: "Data Analyst Intern",
    company: "Insight Analytics",
    description: "Analyse business data, create dashboards, clean datasets, and prepare reports.",
    education: "Diploma or Bachelor",
    skills: "Python, Excel, Power BI",
    experience: 0,
    mode: "Remote",
    location: "Melbourne, VIC"
  },
  {
    title: "IT Support Officer",
    company: "CareTech Services",
    description: "Provide technical support, troubleshoot hardware and software issues, and assist users.",
    education: "Certificate or Diploma",
    skills: "Networking, Windows, Customer Support",
    experience: 1,
    mode: "On-site",
    location: "Liverpool, NSW"
  },
  {
    title: "Frontend Developer",
    company: "Creative Web Studio",
    description: "Design and implement responsive user interfaces with HTML, CSS, JavaScript, and React.",
    education: "Bachelor Degree",
    skills: "HTML, CSS, JavaScript, React",
    experience: 2,
    mode: "Hybrid",
    location: "Sydney, NSW"
  },
  {
    title: "Machine Learning Assistant",
    company: "AI Research Lab",
    description: "Support machine learning experiments, data preprocessing, model training, and evaluation.",
    education: "Bachelor Degree",
    skills: "Python, Machine Learning, TensorFlow",
    experience: 1,
    mode: "Remote",
    location: "Australia"
  },
  {
    title: "Backend Developer",
    company: "CloudCore Systems",
    description: "Develop REST APIs, manage server logic, connect databases, and support backend services.",
    education: "Bachelor Degree",
    skills: "Node.js, Python, SQL, APIs",
    experience: 2,
    mode: "Remote",
    location: "Brisbane, QLD"
  },
  {
    title: "Cybersecurity Trainee",
    company: "SecureNet Group",
    description: "Monitor security alerts, learn risk assessment, support incident response, and document threats.",
    education: "Diploma or Bachelor",
    skills: "Networking, Cybersecurity, Risk Management",
    experience: 0,
    mode: "On-site",
    location: "Parramatta, NSW"
  },
  {
    title: "Database Assistant",
    company: "DataWorks",
    description: "Maintain database records, write SQL queries, check data quality, and generate simple reports.",
    education: "Bachelor Degree",
    skills: "SQL, Database Design, Excel",
    experience: 1,
    mode: "Hybrid",
    location: "Wollongong, NSW"
  },
  {
    title: "UI/UX Designer",
    company: "Digital Product House",
    description: "Create wireframes, design user journeys, test interface usability, and improve prototypes.",
    education: "Diploma or Bachelor",
    skills: "Figma, UI Design, Prototyping",
    experience: 1,
    mode: "Remote",
    location: "Australia"
  },
  {
    title: "Graduate Software Engineer",
    company: "Future Apps",
    description: "Work with a development team to build software features, test code, and improve applications.",
    education: "Bachelor Degree",
    skills: "Java, Python, Git",
    experience: 0,
    mode: "Hybrid",
    location: "Sydney, NSW"
  },
  {
    title: "Cloud Support Associate",
    company: "AzureWorks",
    description: "Support cloud applications, monitor deployments, help users, and troubleshoot cloud services.",
    education: "Bachelor Degree",
    skills: "Cloud, Azure, IT Support",
    experience: 1,
    mode: "Hybrid",
    location: "Sydney, NSW"
  }
];

const defaultCandidates = [
  {
    name: "Alex Smith",
    contact: "alex@example.com",
    education: "Bachelor Degree",
    major: "Computer Science",
    experience: 2,
    skills: "JavaScript, React, SQL"
  },
  {
    name: "Mia Johnson",
    contact: "mia@example.com",
    education: "Bachelor Degree",
    major: "Data Science",
    experience: 1,
    skills: "Python, Power BI, Machine Learning"
  },
  {
    name: "Daniel Lee",
    contact: "daniel@example.com",
    education: "Diploma",
    major: "Information Technology",
    experience: 3,
    skills: "Networking, Windows, IT Support"
  },
  {
    name: "Sarah Chen",
    contact: "sarah@example.com",
    education: "Bachelor Degree",
    major: "Software Engineering",
    experience: 2,
    skills: "Java, APIs, SQL"
  },
  {
    name: "Noah Brown",
    contact: "noah@example.com",
    education: "Certificate IV",
    major: "Cybersecurity",
    experience: 1,
    skills: "Cybersecurity, Risk Management, Networking"
  },
  {
    name: "Emily Wilson",
    contact: "emily@example.com",
    education: "Bachelor Degree",
    major: "Information Systems",
    experience: 4,
    skills: "Business Analysis, SQL, Excel"
  },
  {
    name: "Ryan Taylor",
    contact: "ryan@example.com",
    education: "Bachelor Degree",
    major: "Artificial Intelligence",
    experience: 1,
    skills: "Python, TensorFlow, Data Preprocessing"
  },
  {
    name: "Olivia Martin",
    contact: "olivia@example.com",
    education: "Diploma",
    major: "Design",
    experience: 2,
    skills: "Figma, UI Design, Prototyping"
  },
  {
    name: "James White",
    contact: "james@example.com",
    education: "Bachelor Degree",
    major: "Computer Science",
    experience: 0,
    skills: "Java, Python, Git"
  },
  {
    name: "Lily Davis",
    contact: "lily@example.com",
    education: "Bachelor Degree",
    major: "Cloud Computing",
    experience: 1,
    skills: "Azure, Cloud, IT Support"
  },
  {
    name: "Ethan Harris",
    contact: "ethan@example.com",
    education: "Bachelor Degree",
    major: "Software Development",
    experience: 3,
    skills: "React, Node.js, APIs"
  }
];

function getJobs() {
  const savedJobs = JSON.parse(localStorage.getItem("jobs")) || [];
  return savedJobs.concat(defaultJobs);
}

function getCandidates() {
  const savedCandidates = JSON.parse(localStorage.getItem("candidates")) || [];
  return savedCandidates.concat(defaultCandidates);
}

function getCurrentUser() {
  return JSON.parse(localStorage.getItem("currentUser")) || null;
}

function goHome() {
  const currentUser = getCurrentUser();

  if (currentUser === null) {
    showPage("landing");
    return;
  }

  if (currentUser.role === "candidate") {
    showPage("candidateDashboard");
  } else {
    showPage("employerDashboard");
  }
}

function logoutUser() {
  localStorage.removeItem("currentUser");
  showPage("landing");
}

function updateNavbar(pageId) {
  const navLinks = document.getElementById("navLinks");
  const currentUser = getCurrentUser();

  if (currentUser !== null) {
    if (currentUser.role === "candidate") {
      navLinks.innerHTML = `
        <button onclick="showPage('candidateDashboard')">Candidate Dashboard</button>
        <button onclick="showPage('candidateProfile')">Edit Profile</button>
        <button onclick="logoutUser()">Logout</button>
      `;
    } else {
      navLinks.innerHTML = `
        <button onclick="showPage('employerDashboard')">Employer Dashboard</button>
        <button onclick="showPage('employerPostJob')">Create Job Posting</button>
        <button onclick="logoutUser()">Logout</button>
      `;
    }
    return;
  }

  if (pageId === "landing") {
    navLinks.innerHTML = `
      <button onclick="showPage('login')">Login</button>
      <button onclick="showPage('register')">Register</button>
    `;
  } else if (pageId === "login") {
    navLinks.innerHTML = `
      <button onclick="showPage('landing')">Home</button>
      <button onclick="showPage('register')">Register</button>
    `;
  } else if (pageId === "register") {
    navLinks.innerHTML = `
      <button onclick="showPage('landing')">Home</button>
      <button onclick="showPage('login')">Login</button>
    `;
  } else {
    navLinks.innerHTML = `
      <button onclick="showPage('landing')">Home</button>
      <button onclick="showPage('login')">Login</button>
      <button onclick="showPage('register')">Register</button>
    `;
  }
}

function showPage(pageId) {
  const pages = document.querySelectorAll(".page");
  for (let i = 0; i < pages.length; i++) {
    pages[i].classList.remove("active");
  }

  document.getElementById(pageId).classList.add("active");
  updateNavbar(pageId);

  if (pageId === "candidateDashboard") {
    renderJobs();
  }

  if (pageId === "employerDashboard") {
    renderCandidates();
  }

  window.scrollTo(0, 0);
}

function getUsers() {
  return JSON.parse(localStorage.getItem("users")) || [];
}

function saveUsers(users) {
  localStorage.setItem("users", JSON.stringify(users));
}

function loginUser() {
  const email = document.getElementById("loginEmail").value.trim().toLowerCase();
  const password = document.getElementById("loginPassword").value;
  const role = document.getElementById("loginRole").value;

  if (email === "" || password === "") {
    alert("Please enter your email and password.");
    return;
  }

  const users = getUsers();
  let matchedUser = null;

  for (let i = 0; i < users.length; i++) {
    if (
      users[i].email === email &&
      users[i].password === password &&
      users[i].role === role
    ) {
      matchedUser = users[i];
    }
  }

  if (matchedUser === null) {
    alert("Invalid login details. Please check your email, password, and role.");
    return;
  }

  localStorage.setItem("currentUser", JSON.stringify({
    name: matchedUser.name,
    email: matchedUser.email,
    role: matchedUser.role
  }));

  if (matchedUser.role === "candidate") {
    showPage("candidateDashboard");
  } else {
    showPage("employerDashboard");
  }
}

function registerUser() {
  const name = document.getElementById("registerName").value.trim();
  const email = document.getElementById("registerEmail").value.trim().toLowerCase();
  const password = document.getElementById("registerPassword").value;
  const confirmPassword = document.getElementById("confirmPassword").value;
  const role = document.getElementById("registerRole").value;

  if (name === "" || email === "" || password === "") {
    alert("Please complete all registration fields.");
    return;
  }

  if (password !== confirmPassword) {
    alert("Passwords do not match.");
    return;
  }

  const users = getUsers();

  for (let i = 0; i < users.length; i++) {
    if (users[i].email === email && users[i].role === role) {
      alert("An account with this email and role already exists. Please log in instead.");
      return;
    }
  }

  const newUser = {
    name: name,
    email: email,
    password: password,
    role: role
  };

  users.push(newUser);
  saveUsers(users);

  localStorage.setItem("currentUser", JSON.stringify({
    name: name,
    email: email,
    role: role
  }));

  if (role === "candidate") {
    showPage("candidateProfile");
  } else {
    showPage("employerPostJob");
  }
}

function saveCandidateProfile() {
  const candidate = {
    name: document.getElementById("candidateName").value,
    contact: document.getElementById("candidateContact").value,
    education: document.getElementById("candidateEducation").value,
    major: document.getElementById("candidateMajor").value,
    experience: Number(document.getElementById("candidateExperience").value),
    skills: document.getElementById("candidateSkills").value
  };

  if (candidate.name === "" || candidate.contact === "") {
    alert("Please enter at least the candidate name and contact information.");
    return;
  }

  const savedCandidates = JSON.parse(localStorage.getItem("candidates")) || [];
  savedCandidates.unshift(candidate);
  localStorage.setItem("candidates", JSON.stringify(savedCandidates));

  showPage("candidateDashboard");
}

function publishJob() {
  const job = {
    title: document.getElementById("jobTitle").value,
    company: document.getElementById("companyInfo").value,
    description: document.getElementById("jobDescription").value,
    education: document.getElementById("requiredEducation").value,
    skills: document.getElementById("requiredSkills").value,
    experience: Number(document.getElementById("requiredExperience").value),
    mode: document.getElementById("workMode").value,
    location: document.getElementById("jobLocation").value
  };

  if (job.title === "" || job.description === "") {
    alert("Please enter at least the job title and job description.");
    return;
  }

  const savedJobs = JSON.parse(localStorage.getItem("jobs")) || [];
  savedJobs.unshift(job);
  localStorage.setItem("jobs", JSON.stringify(savedJobs));

  showPage("employerDashboard");
}

function renderJobs() {
  const jobs = getJobs();
  const searchText = document.getElementById("jobSearch").value.toLowerCase();
  const jobList = document.getElementById("jobList");
  const recommendedJobs = document.getElementById("recommendedJobs");

  const filteredJobs = [];
  for (let i = 0; i < jobs.length; i++) {
    if (jobs[i].description.toLowerCase().includes(searchText)) {
      filteredJobs.push(jobs[i]);
    }
  }

  recommendedJobs.innerHTML = createJobCards(jobs.slice(0, 10));

  if (filteredJobs.length === 0) {
    jobList.innerHTML = "<div class='empty-message'>No jobs found from the job description search.</div>";
  } else {
    jobList.innerHTML = createJobCards(filteredJobs);
  }
}

function createJobCards(jobs) {
  let html = "";

  for (let i = 0; i < jobs.length; i++) {
    html += `
      <div class="card">
        <h4>${jobs[i].title}</h4>
        <p><strong>Company:</strong> ${jobs[i].company}</p>
        <p><strong>Description:</strong> ${jobs[i].description}</p>
        <p><strong>Education:</strong> ${jobs[i].education}</p>
        <p><strong>Experience:</strong> ${jobs[i].experience} year(s)</p>
        <p><strong>Mode:</strong> ${jobs[i].mode}</p>
        <p><strong>Location:</strong> ${jobs[i].location}</p>
        <div class="badge-row">
          ${createBadges(jobs[i].skills)}
        </div>
      </div>
    `;
  }

  return html;
}

function renderCandidates() {
  const candidates = getCandidates();
  const searchText = document.getElementById("candidateSearch").value.toLowerCase();
  const skillFilter = document.getElementById("skillFilter").value.toLowerCase();
  const educationFilter = document.getElementById("educationFilter").value.toLowerCase();
  const experienceFilterValue = document.getElementById("experienceFilter").value;
  const candidateList = document.getElementById("candidateList");
  const recommendedCandidates = document.getElementById("recommendedCandidates");

  const filteredCandidates = [];

  for (let i = 0; i < candidates.length; i++) {
    const candidateText = `${candidates[i].name} ${candidates[i].education} ${candidates[i].major} ${candidates[i].skills}`.toLowerCase();
    const matchesSearch = candidateText.includes(searchText);
    const matchesSkill = candidates[i].skills.toLowerCase().includes(skillFilter);
    const matchesEducation = candidates[i].education.toLowerCase().includes(educationFilter);

    let matchesExperience = true;
    if (experienceFilterValue !== "") {
      matchesExperience = candidates[i].experience >= Number(experienceFilterValue);
    }

    if (matchesSearch && matchesSkill && matchesEducation && matchesExperience) {
      filteredCandidates.push(candidates[i]);
    }
  }

  recommendedCandidates.innerHTML = createCandidateCards(candidates.slice(0, 10));

  if (filteredCandidates.length === 0) {
    candidateList.innerHTML = "<div class='empty-message'>No candidates match the search or filter.</div>";
  } else {
    candidateList.innerHTML = createCandidateCards(filteredCandidates);
  }
}

function createCandidateCards(candidates) {
  let html = "";

  for (let i = 0; i < candidates.length; i++) {
    html += `
      <div class="card">
        <h4>${candidates[i].name}</h4>
        <p><strong>Contact:</strong> ${candidates[i].contact}</p>
        <p><strong>Education:</strong> ${candidates[i].education}</p>
        <p><strong>Major:</strong> ${candidates[i].major}</p>
        <p><strong>Experience:</strong> ${candidates[i].experience} year(s)</p>
        <div class="badge-row">
          ${createBadges(candidates[i].skills)}
        </div>
      </div>
    `;
  }

  return html;
}

function createBadges(text) {
  const parts = text.split(",");
  let html = "";

  for (let i = 0; i < parts.length; i++) {
    html += `<span class="badge">${parts[i].trim()}</span>`;
  }

  return html;
}

updateNavbar("landing");
renderJobs();
renderCandidates();
