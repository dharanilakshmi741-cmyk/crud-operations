let editId = null;

function showMessage(msg) {
    document.getElementById("message").innerText = msg;
}

async function loadStudents() {

    const response = await fetch("/students");
    const students = await response.json();

    const table = document.getElementById("studentTable");

    table.innerHTML = "";

    students.forEach((student, index) => {

        table.innerHTML += `
        <tr>
            <td>${index + 1}</td>
            <td>${student.name}</td>
            <td>${student.age}</td>
            <td>${student.course}</td>
            <td>
                <button onclick="
                    editStudent(
                    ${student.id},
                    '${student.name}',
                    ${student.age},
                    '${student.course}'
                    )">
                    Edit
                </button>

                <button onclick="
                    deleteStudent(${student.id})">
                    Delete
                </button>
            </td>
        </tr>
        `;
    });
}

async function saveStudent() {

    const student = {
        name: document.getElementById("name").value,
        age: document.getElementById("age").value,
        course: document.getElementById("course").value
    };

    if (editId === null) {

        await fetch("/students", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(student)
        });

        showMessage("Student Added Successfully");

    } else {

        await fetch(`/students/${editId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(student)
        });

        showMessage("Student Updated Successfully");

        editId = null;

        document.getElementById("saveBtn").innerText =
        "Add Student";
    }

    clearForm();
    loadStudents();
}

function editStudent(id, name, age, course) {

    editId = id;

    document.getElementById("name").value = name;
    document.getElementById("age").value = age;
    document.getElementById("course").value = course;

    document.getElementById("saveBtn").innerText =
    "Update Student";
}

async function deleteStudent(id) {

    await fetch(`/students/${id}`, {
        method: "DELETE"
    });

    showMessage("Student Deleted Successfully");

    loadStudents();
}

function clearForm() {

    document.getElementById("name").value = "";
    document.getElementById("age").value = "";
    document.getElementById("course").value = "";
}

loadStudents();
