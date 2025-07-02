import React, { useEffect, useState } from "react";
import axios from "../axiosConfig";

const ManualForm = () => {
  const [schema, setSchema] = useState([]);
  const [formData, setFormData] = useState({});

  useEffect(() => {
    axios.get("/schemas/input_schema.json")
      .then(response => setSchema(response.data))
      .catch(err => console.error("Failed to load schema:", err));
  }, []);

  const handleChange = (key, value) => {
    setFormData(prev => ({ ...prev, [key]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post("/api/manual_suggestion", formData)
      .then(response => console.log("Suggested plans:", response.data))
      .catch(err => console.error("API error:", err));
  };

  const renderField = (field) => {
    if (field.type === "integer" || field.type === "float") {
      return (
        <input
          type="number"
          min={field.min !== null ? field.min : undefined}
          max={field.max !== null ? field.max : undefined}
          required={field.required}
          onChange={e => handleChange(field.key, parseFloat(e.target.value))}
          placeholder={field.label}
        />
      );
    }

    if (field.type === "enum") {
      return (
        <select required={field.required} onChange={e => handleChange(field.key, e.target.value)}>
          <option value="">Select {field.label}</option>
          {field.choices.map(choice => (
            <option key={choice} value={choice}>{choice}</option>
          ))}
        </select>
      );
    }

    if (field.type === "multi-select") {
      return (
        <div>
          <label>{field.label}</label>
          {field.choices.map(choice => (
            <label key={choice.id}>
              <input
                type="checkbox"
                value={choice.id}
                onChange={e => {
                  const prev = formData[field.key] || [];
                  const newValues = e.target.checked
                    ? [...prev, choice.id]
                    : prev.filter(v => v !== choice.id);
                  handleChange(field.key, newValues);
                }}
              />
              {choice.name}
            </label>
          ))}
        </div>
      );
    }

    return null;
  };

  return (
    <form onSubmit={handleSubmit}>
      {schema.map(field => (
        <div key={field.key} className="form-group">
          <label>{field.label}</label>
          {renderField(field)}
        </div>
      ))}
      <button type="submit">Get Suggested Plans</button>
    </form>
  );
};

export default ManualForm;
