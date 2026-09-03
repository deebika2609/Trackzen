import React from "react";

export default function TaskTable({ tasks }) {
  return (
    <div className="bg-white rounded-xl shadow p-4 overflow-x-auto">
      <h2 className="font-bold text-navy mb-3">Pending Maintenance Requests (synthetic TMS/SMMS/TDMS feed)</h2>
      <table className="w-full text-sm">
        <thead>
          <tr className="text-left text-gray-500 border-b">
            <th className="py-2 pr-4">ID</th>
            <th className="py-2 pr-4">Department</th>
            <th className="py-2 pr-4">Corridor</th>
            <th className="py-2 pr-4">Task</th>
            <th className="py-2 pr-4">Criticality</th>
            <th className="py-2 pr-4">Duration (h)</th>
            <th className="py-2 pr-4">Due (days)</th>
          </tr>
        </thead>
        <tbody>
          {tasks.map((t) => (
            <tr key={t.id} className="border-b last:border-0 hover:bg-gray-50">
              <td className="py-2 pr-4 font-mono text-xs">{t.id}</td>
              <td className="py-2 pr-4">{t.department}</td>
              <td className="py-2 pr-4">{t.corridor}</td>
              <td className="py-2 pr-4">{t.task}</td>
              <td className="py-2 pr-4">{t.criticality}/10</td>
              <td className="py-2 pr-4">{t.duration_hours}</td>
              <td className="py-2 pr-4">{t.due_in_days}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
