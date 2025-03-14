// Function to get random information based on type
function getRandomInfo(type) {
    const randomData = {
        school: [
            "BI_VGS Oslo is known for its modern facilities and state-of-the-art classrooms.",
            "We offer a wide range of industry-focused programs to prepare students for real-world challenges."
        ],
        mission: [
            "Our mission is to build future-ready professionals who can make impactful contributions to the world.",
            "We aim to provide a dynamic and challenging learning environment that encourages innovation and leadership."
        ],
        values: [
            "Integrity is at the heart of everything we do, ensuring a foundation of trust and accountability.",
            "Innovation and excellence are key drivers in shaping the future of education at BI_VGS."
        ]
    };

    const infoDiv = document.getElementById(`${type}-info`);
    const randomIndex = Math.floor(Math.random() * randomData[type].length);
    infoDiv.innerHTML = `<p>${randomData[type][randomIndex]}</p>`;
}

// Function to show program details based on selected type
function showDetails(programType) {
    const detailsContainer = document.getElementById('program-details');
    const programDetails = {
        business: `
            <h2>Business and Economics</h2>
            <p>Our Business and Economics program equips students with the essential knowledge to understand how businesses operate, the principles of economics, and the world of entrepreneurship. This program prepares students for higher education in business-related fields or careers in economics, finance, and management.</p>
            <ul>
                <li>Introduction to Business Concepts</li>
                <li>Basic Economics and Market Theory</li>
                <li>Entrepreneurship and Innovation</li>
            </ul>
        `,
        technology: `
            <h2>Technology and Computer Science</h2>
            <p>Our Technology and Computer Science program introduces students to the world of IT, programming, and digital technology. Students will develop key skills in coding, system design, and problem-solving, preparing them for further studies in technology and the digital industry.</p>
            <ul>
                <li>Introduction to Programming Languages (Python, JavaScript)</li>
                <li>Basic Web Development and Design</li>
                <li>Cybersecurity and Networking Fundamentals</li>
            </ul>
        `,
        science: `
            <h2>Science and Innovation</h2>
            <p>The Science and Innovation program allows students to explore the world of natural sciences, sustainability, and the cutting-edge research that shapes our future. This program provides hands-on experience with laboratory work and research projects.</p>
            <ul>
                <li>Fundamentals of Biology, Chemistry, and Physics</li>
                <li>Sustainability and Environmental Science</li>
                <li>Introduction to Scientific Research</li>
            </ul>
        `,
        arts: `
            <h2>Arts and Humanities</h2>
            <p>Our Arts and Humanities program helps students develop critical thinking and creativity through the exploration of arts, culture, history, and philosophy. This program is perfect for those who are passionate about the arts and wish to further their education in the creative industries.</p>
            <ul>
                <li>Literature, History, and Philosophy</li>
                <li>Art and Music Theory</li>
                <li>Cultural Studies and Social Anthropology</li>
            </ul>
        `
    };

    detailsContainer.innerHTML = programDetails[programType] || '<p>Select a program to learn more.</p>';
    detailsContainer.style.display = 'block';
}

// Function to populate sections based on selected class level
function populateSections() {
    const classLevel = document.getElementById('classLevel').value;
    const sectionSelect = document.getElementById('section');
    const suggestionBox = document.getElementById('suggestionBox');

    // Reset sections and suggestion box
    sectionSelect.innerHTML = '<option value="">-- Select Section --</option>';
    suggestionBox.value = '';

    if (classLevel) {
        const sections = ['A', 'B', 'C', 'D'].map(letter => `Section ${letter}`);
        const suggestions = {
            3: 'A',
            5: 'B',
            7: 'C',
            8: 'D'
        };

        sections.forEach(section => {
            const option = document.createElement('option');
            option.value = section;
            option.textContent = section;
            sectionSelect.appendChild(option);
        });

        suggestionBox.value = `Suggested Section: ${suggestions[classLevel] || 'D'}`;
    }
}

// Function to validate form data before submission
function validateForm() {
    const fullName = document.getElementById('fullName').value.trim();
    const dob = document.getElementById('dob').value.trim();
    const classLevel = document.getElementById('classLevel').value;
    const section = document.getElementById('section').value;

    // Check if the fields are filled
    if (!fullName || !dob || !classLevel || !section) {
        alert('Please fill out all fields before submitting the application.');
        return false;
    }

    // Calculate age based on date of birth
    const birthDate = new Date(dob);
    const age = new Date().getFullYear() - birthDate.getFullYear();

    // Check if the age fits the class level (this can be adjusted as per school guidelines)
    if (age < 6 || age > 15) {
        alert('Age does not align with the selected class level.');
        return false;
    }

    // Show success message after form submission
    document.getElementById('admissions-form').reset();
    document.getElementById('admissions-form').style.display = 'none';
    document.getElementById('success-message').style.display = 'block';

    return false;
}
