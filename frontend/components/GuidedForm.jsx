import React, { useState } from "react";
import axios from "axios";

const GuidedForm = () => {
  const [goal, setGoal] = useState("");
  const [suggestions, setSuggestions] = useState([]);

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post("/api/guided_suggestion", { goal })
      .then(response => setSuggestions(response.data.recommended_plans))
      .catch(err => console.error("API error:", err));
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label>Select Your Life Goal</label>
        <select required onChange={(e) => setGoal(e.target.value)} value={goal}>
          <option value="">-- Choose Goal --</option>
          <option value="child_education">Child Education</option>
          <option value="marriage">Marriage Planning</option>
          <option value="retirement">Retirement Planning</option>
          <option value="wealth_creation">Wealth Creation</option>
        </select>
        <button type="submit">Get Suggested Plans</button>
      </form>

      {suggestions.length > 0 && (
        <div>
          <h3>Recommended Plans:</h3>
          <ul>
            {suggestions.map(plan => (
              <li key={plan.plan_id}>
                {plan.plan_name}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default GuidedForm;
