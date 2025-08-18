import React, { useState } from "react";

function StudentTable({ students, updateStudent }) {
  const [editingRoll, setEditingRoll] = useState(null);
  const [editData, setEditData] = useState({ name: "", marks: "" });

  const handleEdit = (student) => {
    setEditingRoll(student.roll);
    setEditData({ name: student.name, marks: student.marks });
  };

  const handleSave = (roll) => {
    if (!editData.name || editData.marks === "") return alert("Fill all fields");
    updateStudent(roll, { ...editData, roll, marks: Number(editData.marks) });
    setEditingRoll(null);
  };

  return (
    <table border="1" cellPadding="10" style={{ width: "100%" }}>
      <thead>
        <tr>
          <th>Name</th>
          <th>Roll No</th>
          <th>Marks</th>
          <th>Grade</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {students.map((s) => (
          <tr key={s.roll}>
            <td>
              {editingRoll === s.roll ? (
                <input
                  value={editData.name}
                  onChange={(e) =>
                    setEditData({ ...editData, name: e.target.value })
                  }
                />
              ) : (
                s.name
              )}
            </td>
            <td>{s.roll}</td>
            <td>
              {editingRoll === s.roll ? (
                <input
                  type="number"
                  value={editData.marks}
                  onChange={(e) =>
                    setEditData({ ...editData, marks: e.target.value })
                  }
                />
              ) : (
                s.marks
              )}
            </td>
            <td>{s.grade}</td>
            <td>
              {editingRoll === s.roll ? (
                <button onClick={() => handleSave(s.roll)}>Save</button>
              ) : (
                <button onClick={() => handleEdit(s)}>Edit</button>
              )}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default StudentTable;
