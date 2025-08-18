import React, { useState } from "react";

function StudentForm({ addStudent }) {
  const [name, setName] = useState("");
  const [roll, setRoll] = useState("");
  const [marks, setMarks] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!name || !roll || !marks) return;
    addStudent({ name, roll, marks: Number(marks) });
    setName("");
    setRoll("");
    setMarks("");
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
      <input placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
      <input placeholder="Roll No" value={roll} onChange={(e) => setRoll(e.target.value)} />
      <input placeholder="Marks" type="number" value={marks} onChange={(e) => setMarks(e.target.value)} />
      <button type="submit">Add Student</button>
    </form>
  );
}

export default StudentForm;
