import React, { useEffect, useState } from "react";
import axios from "axios";
import StudentForm from "./components/StudentForm";
import StudentTable from "./components/StudentTable";

function App() {
  const [students, setStudents] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchStudents();
  }, []);

  const fetchStudents = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:5000/students");
      setStudents(res.data);
      setError("");
    } catch (err) {
      setError("Failed to fetch students.");
    }
  };

  const addStudent = async (student) => {
    try {
      await axios.post("http://127.0.0.1:5000/students", student);
      fetchStudents();
    } catch (err) {
      setError(err.response?.data?.error || "Error adding student");
    }
  };

  const updateStudent = async (roll, student) => {
    try {
      await axios.put(`http://127.0.0.1:5000/students/${roll}`, student);
      fetchStudents();
    } catch (err) {
      setError(err.response?.data?.error || "Error updating student");
    }
  };

  const exportCSV = () => {
    try {
      window.open("http://127.0.0.1:5000/export", "_blank");
    } catch {
      setError("Error exporting CSV");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Student Records</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <button onClick={exportCSV} style={{ marginBottom: "10px" }}>
        ⬇ Export CSV
      </button>
      <StudentForm addStudent={addStudent} />
      <StudentTable students={students} updateStudent={updateStudent} />
    </div>
  );
}

export default App;
