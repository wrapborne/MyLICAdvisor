import React, { useState, useEffect } from "react";
import axios from "axios";

const AdminDashboard = () => {
  const [plans, setPlans] = useState([]);
  const [goals, setGoals] = useState([]);
  const [newPlan, setNewPlan] = useState({ plan_id: "", plan_name: "", min_age: 0, max_age: 0 });
  const [newGoal, setNewGoal] = useState({ goal_id: "", goal_name: "", description: "" });

  const loadPlans = () => {
    axios.get("/api/admin/plans")
      .then(response => setPlans(response.data.plans || []))
      .catch(err => console.error("Failed to load plans:", err));
  };

  const loadGoals = () => {
    axios.get("/api/admin/goals")
      .then(response => setGoals(response.data.goals || []))
      .catch(err => console.error("Failed to load goals:", err));
  };

  useEffect(() => {
    loadPlans();
    loadGoals();
  }, []);

  const handleAddPlan = () => {
    axios.post("/api/admin/plans", newPlan)
      .then(() => {
        loadPlans();
        setNewPlan({ plan_id: "", plan_name: "", min_age: 0, max_age: 0 });
      })
      .catch(err => console.error("Add plan failed:", err));
  };

  const handleDeletePlan = (planId) => {
    axios.delete(`/api/admin/plans/${planId}`)
      .then(() => loadPlans())
      .catch(err => console.error("Delete plan failed:", err));
  };

  const handleAddGoal = () => {
    axios.post("/api/admin/goals", newGoal)
      .then(() => {
        loadGoals();
        setNewGoal({ goal_id: "", goal_name: "", description: "" });
      })
      .catch(err => console.error("Add goal failed:", err));
  };

  const handleDeleteGoal = (goalId) => {
    axios.delete(`/api/admin/goals/${goalId}`)
      .then(() => loadGoals())
      .catch(err => console.error("Delete goal failed:", err));
  };

  return (
    <div>
      <h2>Admin Dashboard</h2>

      <h3>Add New Plan</h3>
      <input placeholder="Plan ID" value={newPlan.plan_id}
        onChange={e => setNewPlan({ ...newPlan, plan_id: e.target.value })} />
      <input placeholder="Plan Name" value={newPlan.plan_name}
        onChange={e => setNewPlan({ ...newPlan, plan_name: e.target.value })} />
      <input type="number" placeholder="Min Age" value={newPlan.min_age}
        onChange={e => setNewPlan({ ...newPlan, min_age: parseInt(e.target.value) })} />
      <input type="number" placeholder="Max Age" value={newPlan.max_age}
        onChange={e => setNewPlan({ ...newPlan, max_age: parseInt(e.target.value) })} />
      <button onClick={handleAddPlan}>Add Plan</button>

      <h3>Plans Management</h3>
      <table border="1">
        <thead>
          <tr>
            <th>Plan ID</th>
            <th>Name</th>
            <th>Min Age</th>
            <th>Max Age</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {plans.map(plan => (
            <tr key={plan.plan_id}>
              <td>{plan.plan_id}</td>
              <td>{plan.plan_name}</td>
              <td>{plan.min_age}</td>
              <td>{plan.max_age}</td>
              <td>
                <button onClick={() => handleDeletePlan(plan.plan_id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <h3>Add New Goal</h3>
      <input placeholder="Goal ID" value={newGoal.goal_id}
        onChange={e => setNewGoal({ ...newGoal, goal_id: e.target.value })} />
      <input placeholder="Goal Name" value={newGoal.goal_name}
        onChange={e => setNewGoal({ ...newGoal, goal_name: e.target.value })} />
      <input pl
